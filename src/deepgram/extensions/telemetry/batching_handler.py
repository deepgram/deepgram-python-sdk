from __future__ import annotations

import atexit
import base64
import os
import queue
import threading
import time
import traceback
import typing
import zlib
from collections import Counter
from typing import List

import httpx
from .handler import TelemetryHandler


class BatchingTelemetryHandler(TelemetryHandler):
    """
    Non-blocking telemetry handler that batches events and flushes in the background.

    - Enqueues events quickly; never blocks request path
    - Flushes when batch size or max interval is reached
    - Errors trigger an immediate flush attempt
    - Best-effort delivery; drops on full queue rather than blocking
    """

    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str | None = None,
        batch_size: int = 20,
        max_interval_seconds: float = 5.0,
        max_queue_size: int = 1000,
        client: typing.Optional[httpx.Client] = None,
        encode_batch: typing.Optional[typing.Callable[..., bytes]] = None,
        encode_batch_iter: typing.Optional[typing.Callable[..., typing.Iterator[bytes]]] = None,
        content_type: str = "application/x-protobuf",
        context_provider: typing.Optional[typing.Callable[[], typing.Mapping[str, typing.Any]]] = None,
        max_consecutive_failures: int = 5,
        synchronous: bool = False,
    ) -> None:
        self._endpoint = endpoint
        self._api_key = api_key
        self._batch_size = max(1, batch_size)
        self._max_interval = max(0.25, max_interval_seconds)
        self._client = client or httpx.Client(timeout=5.0)
        self._encode_batch = encode_batch
        self._encode_batch_iter = encode_batch_iter
        # Always protobuf by default
        self._content_type = content_type
        self._context_provider = context_provider or (lambda: {})
        self._debug = str(os.getenv("DEEPGRAM_DEBUG", "")).lower() in ("1", "true")
        self._max_consecutive_failures = max(1, max_consecutive_failures)
        self._consecutive_failures = 0
        self._disabled = False
        self._synchronous = bool(synchronous)
        if self._synchronous:
            # In synchronous mode, we do not spin a worker; we stage events locally
            self._buffer_sync: List[dict] = []
        else:
            self._queue: queue.Queue[dict] = queue.Queue(maxsize=max_queue_size)
            self._stop_event = threading.Event()
            self._flush_event = threading.Event()
            self._worker = threading.Thread(target=self._run, name="dg-telemetry-worker", daemon=True)
            self._worker.start()
            # Ensure we flush at process exit so short-lived scripts still send (or surface errors in debug)
            atexit.register(self.close)

    # --- TelemetryHandler interface ---

    def on_http_request(
        self, 
        *, 
        method: str, 
        url: str, 
        headers: typing.Mapping[str, str] | None, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        event = {
            "type": "http_request",
            "ts": time.time(),
            "method": method,
            "url": url,
        }
        # Extract request_id from request_details for server-side correlation
        if request_details and "request_id" in request_details:
            event["request_id"] = request_details["request_id"]
        if extras:
            event["extras"] = dict(extras)
        if request_details:
            event["request_details"] = dict(request_details)
        self._enqueue(event)

    def on_http_response(
        self,
        *,
        method: str,
        url: str,
        status_code: int,
        duration_ms: float,
        headers: typing.Mapping[str, str] | None,
        extras: typing.Mapping[str, str] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        event = {
            "type": "http_response",
            "ts": time.time(),
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_ms": duration_ms,
        }
        # Extract request_id from response_details for server-side correlation
        if response_details and "request_id" in response_details:
            event["request_id"] = response_details["request_id"]
        if extras:
            event["extras"] = dict(extras)
        if response_details:
            event["response_details"] = dict(response_details)
        self._enqueue(event)
        # Only promote 5XX server errors to ErrorEvent (not 4XX client errors)
        try:
            if int(status_code) >= 500:
                self._enqueue({
                    "type": "http_error",
                    "ts": time.time(),
                    "method": method,
                    "url": url,
                    "error": f"HTTP_{status_code}",
                    "status_code": status_code,
                    "handled": True,
                }, force_flush=True)
        except Exception:
            pass

    def on_http_error(
        self, 
        *, 
        method: str, 
        url: str, 
        error: BaseException, 
        duration_ms: float,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        # Filter out 4XX client errors - only capture 5XX server errors and unhandled exceptions
        if response_details:
            status_code = response_details.get('status_code')
            if status_code and isinstance(status_code, int) and 400 <= status_code < 500:
                # Skip 4XX client errors (auth failures, bad requests, etc.)
                return
        
        stack: str = ""
        try:
            stack = "".join(traceback.format_exception(type(error), error, getattr(error, "__traceback__", None)))
        except Exception:
            pass
        
        event = {
            "type": "http_error",
            "ts": time.time(),
            "method": method,
            "url": url,
            "error": type(error).__name__,
            "message": str(error),
            "stack_trace": stack,
            "handled": False,
            "duration_ms": duration_ms,
        }
        
        # Extract request_id for server-side correlation
        if response_details and "request_id" in response_details:
            event["request_id"] = response_details["request_id"]
        elif request_details and "request_id" in request_details:
            event["request_id"] = request_details["request_id"]
        
        # Add comprehensive error context
        if request_details:
            event["request_details"] = dict(request_details)
        if response_details:
            event["response_details"] = dict(response_details)
            
        self._enqueue(event, force_flush=True)

    # --- Optional WebSocket signals -> mapped to telemetry ---
    def on_ws_connect(
        self, 
        *, 
        url: str, 
        headers: typing.Mapping[str, str] | None, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        event = {
            "type": "ws_connect",
            "ts": time.time(),
            "url": url,
        }
        if extras:
            event["extras"] = dict(extras)
        if request_details:
            event["request_details"] = dict(request_details)
        self._enqueue(event)


    def on_ws_error(
        self, 
        *, 
        url: str, 
        error: BaseException, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        # Use stack trace from response_details if available, otherwise generate it
        stack: str = ""
        if response_details and response_details.get("stack_trace"):
            stack = response_details["stack_trace"]
        else:
            try:
                stack = "".join(traceback.format_exception(type(error), error, getattr(error, "__traceback__", None)))
            except Exception:
                pass
        
        event = {
            "type": "ws_error",
            "ts": time.time(),
            "url": url,
            "error": type(error).__name__,
            "message": str(error),
            "stack_trace": stack,
            "handled": False,
        }
        
        # Add comprehensive error context from response_details
        if response_details:
            event["response_details"] = dict(response_details)
            # Extract specific error details to event level for easier access
            if "error_type" in response_details:
                event["error_type"] = response_details["error_type"]
            if "error_message" in response_details:
                event["error_message"] = response_details["error_message"]
            if "function_name" in response_details:
                event["function_name"] = response_details["function_name"]
            if "duration_ms" in response_details:
                event["duration_ms"] = response_details["duration_ms"]
            if "timeout_occurred" in response_details:
                event["timeout_occurred"] = response_details["timeout_occurred"]
            if "handshake_response_headers" in response_details:
                event["handshake_response_headers"] = response_details["handshake_response_headers"]
            if "handshake_status_code" in response_details:
                event["handshake_status_code"] = response_details["handshake_status_code"]
            if "handshake_reason_phrase" in response_details:
                event["handshake_reason_phrase"] = response_details["handshake_reason_phrase"]
            if "handshake_error_type" in response_details:
                event["handshake_error_type"] = response_details["handshake_error_type"]
        
        # Add request context
        if request_details:
            event["request_details"] = dict(request_details)
            # Extract specific request details for easier access
            if "function_name" in request_details:
                event["sdk_function"] = request_details["function_name"]
            if "connection_kwargs" in request_details:
                event["connection_params"] = request_details["connection_kwargs"]
        
        # Build comprehensive extras with all enhanced telemetry details
        enhanced_extras = dict(extras) if extras else {}
        
        # Add all response details to extras
        if response_details:
            for key, value in response_details.items():
                if key not in enhanced_extras and value is not None:
                    enhanced_extras[key] = value
        
        # Add all request details to extras
        if request_details:
            for key, value in request_details.items():
                if key not in enhanced_extras and value is not None:
                    enhanced_extras[key] = value
        
        # Add all event-level details to extras
        event_extras = {
            "error_type": event.get("error_type"),
            "error_message": event.get("error_message"),
            "function_name": event.get("function_name"),
            "sdk_function": event.get("sdk_function"),
            "duration_ms": event.get("duration_ms"),
            "timeout_occurred": event.get("timeout_occurred"),
            "handshake_status_code": event.get("handshake_status_code"),
            "handshake_reason_phrase": event.get("handshake_reason_phrase"),
            "handshake_error_type": event.get("handshake_error_type"),
            "connection_params": event.get("connection_params"),
        }
        
        # Add handshake response headers to extras
        handshake_headers = event.get("handshake_response_headers")
        if handshake_headers and hasattr(handshake_headers, 'items'):
            for header_name, header_value in handshake_headers.items():  # type: ignore[attr-defined]
                safe_header_name = header_name.lower().replace('-', '_')
                enhanced_extras[f"handshake_{safe_header_name}"] = str(header_value)
        
        # Merge event extras, excluding None values
        for key, value in event_extras.items():
            if value is not None:
                enhanced_extras[key] = value
        
        # Store the comprehensive extras
        if enhanced_extras:
            event["extras"] = enhanced_extras
            
        self._enqueue(event, force_flush=True)

    def on_ws_close(
        self, 
        *, 
        url: str,
    ) -> None:
        # Close should force a final flush so debug printing happens during short-lived runs
        event = {
            "type": "ws_close",
            "ts": time.time(),
            "url": url,
        }
        self._enqueue(event, force_flush=True)

    # Optional: uncaught errors from external hooks
    def on_uncaught_error(self, *, error: BaseException) -> None:
        stack: str = ""
        try:
            stack = "".join(traceback.format_exception(type(error), error, getattr(error, "__traceback__", None)))
        except Exception:
            pass
        self._enqueue({
            "type": "uncaught_error",
            "ts": time.time(),
            "error": type(error).__name__,
            "message": str(error),
            "stack_trace": stack,
            "handled": False,
        }, force_flush=True)

    # --- Internal batching ---

    def _enqueue(self, event: dict, *, force_flush: bool = False) -> None:
        if self._disabled:
            return
        if self._synchronous:
            # Stage locally and flush according to thresholds immediately in caller thread
            self._buffer_sync.append(event)  # type: ignore[attr-defined]
            if len(self._buffer_sync) >= self._batch_size or force_flush:  # type: ignore[attr-defined]
                try:
                    self._flush(self._buffer_sync)  # type: ignore[attr-defined]
                finally:
                    self._buffer_sync = []  # type: ignore[attr-defined]
            return
        try:
            self._queue.put_nowait(event)
        except queue.Full:
            # Best-effort: drop rather than blocking request path
            return
        # Wake worker if we hit batch size or need immediate flush
        if self._queue.qsize() >= self._batch_size or force_flush:
            self._flush_event.set()

    def _run(self) -> None:
        last_flush = time.time()
        buffer: List[dict] = []
        while not self._stop_event.is_set():
            if self._disabled:
                break
            timeout = max(0.0, self._max_interval - (time.time() - last_flush))
            try:
                item = self._queue.get(timeout=timeout)
                buffer.append(item)
            except queue.Empty:
                pass

            # Conditions to flush: batch size, interval elapsed, or explicit signal
            should_flush = (
                len(buffer) >= self._batch_size
                or (time.time() - last_flush) >= self._max_interval
                or self._flush_event.is_set()
            )
            if should_flush and buffer:
                self._flush(buffer)
                buffer = []
                last_flush = time.time()
                self._flush_event.clear()

        # Drain on shutdown
        if buffer:
            self._flush(buffer)

    def _flush(self, batch: List[dict]) -> None:
        try:
            # Choose streaming iterator if provided; otherwise bytes encoder.
            # If no encoder provided, drop silently to avoid memory use.
            context = self._context_provider() or {}
            
            # Extract enhanced telemetry details from events and add to context extras
            enhanced_extras = {}
            for event in batch:
                # Merge event extras
                event_extras = event.get("extras", {})
                if event_extras:
                    for key, value in event_extras.items():
                        if value is not None:
                            enhanced_extras[key] = value
                
                # Merge request_details (privacy-focused request structure)
                request_details = event.get("request_details", {})
                if request_details:
                    for key, value in request_details.items():
                        if value is not None:
                            enhanced_extras[f"request_{key}"] = value
                
                # Merge response_details (privacy-focused response structure)
                response_details = event.get("response_details", {})
                if response_details:
                    for key, value in response_details.items():
                        if value is not None:
                            enhanced_extras[f"response_{key}"] = value
            
            # Add enhanced extras to context
            if enhanced_extras:
                context = dict(context)  # Make a copy
                context["extras"] = enhanced_extras
            if self._encode_batch_iter is not None:
                try:
                    plain_iter = self._encode_batch_iter(batch, context)  # type: ignore[misc]
                except TypeError:
                    plain_iter = self._encode_batch_iter(batch)  # type: ignore[misc]
            elif self._encode_batch is not None:
                try:
                    data = self._encode_batch(batch, context)  # type: ignore[misc]
                except TypeError:
                    data = self._encode_batch(batch)  # type: ignore[misc]
                plain_iter = iter([data])
            else:
                # Use built-in protobuf encoder when none provided
                from .proto_encoder import encode_telemetry_batch_iter

                try:
                    plain_iter = encode_telemetry_batch_iter(batch, context)
                except Exception:
                    if self._debug:
                        raise
                    return

            headers = {"content-type": self._content_type, "content-encoding": "gzip"}
            if self._api_key:
                headers["authorization"] = f"Bearer {self._api_key}"
            if self._debug:
                # Mask sensitive headers for debug output
                dbg_headers = dict(headers)
                if "authorization" in dbg_headers:
                    dbg_headers["authorization"] = "Bearer ***"
                # Summarize event types and include a compact context view
                try:
                    type_counts = dict(Counter(str(e.get("type", "unknown")) for e in batch))
                except Exception:
                    type_counts = {}
                ctx_view = {}
                try:
                    # Show a stable subset of context keys if present
                    for k in (
                        "sdk_name",
                        "sdk_version",
                        "language",
                        "runtime_version",
                        "os",
                        "arch",
                        "session_id",
                        "app_name",
                        "app_version",
                        "environment",
                        "project_id",
                    ):
                        v = context.get(k)
                        if v:
                            ctx_view[k] = v
                except Exception:
                    pass
                # Compute full bodies in debug mode to print exact payload
                # Determine uncompressed bytes for the batch
                try:
                    if self._encode_batch_iter is not None:
                        raw_body = b"".join(plain_iter)
                    elif self._encode_batch is not None:
                        # "data" exists from above branch
                        raw_body = data
                    else:
                        from .proto_encoder import encode_telemetry_batch

                        raw_body = encode_telemetry_batch(batch, context)
                except Exception:
                    raw_body = b""
                # Gzip-compress to match actual wire payload
                try:
                    compressor = zlib.compressobj(wbits=31)
                    compressed_body = compressor.compress(raw_body) + compressor.flush()
                except Exception:
                    compressed_body = b""
                # Print full payload (compressed, base64) and sizes
                print(
                    f"[deepgram][telemetry] POST {self._endpoint} "
                    f"events={len(batch)} headers={dbg_headers} types={type_counts} context={ctx_view}"
                )
                try:
                    b64 = base64.b64encode(compressed_body).decode("ascii") if compressed_body else ""
                except Exception:
                    b64 = ""
                print(
                    f"[deepgram][telemetry] body.compressed.b64={b64} "
                    f"size={len(compressed_body)}B raw={len(raw_body)}B"
                )
            try:
                if self._debug:
                    # Send pre-built compressed body in debug mode
                    resp = self._client.post(self._endpoint, content=compressed_body, headers=headers)
                else:
                    # Stream in normal mode
                    resp = self._client.post(self._endpoint, content=self._gzip_iter(plain_iter), headers=headers)
                if self._debug:
                    try:
                        status = getattr(resp, "status_code", "unknown")
                        print(f"[deepgram][telemetry] -> {status}")
                    except Exception:
                        pass
            except Exception as exc:
                # Log the error in debug mode instead of raising from a worker thread
                if self._debug:
                    try:
                        print(f"[deepgram][telemetry] -> error: {type(exc).__name__}: {exc}")
                    except Exception:
                        pass
                # Re-raise to outer handler to count failure/disable logic
                raise
            # Success: reset failure count
            self._consecutive_failures = 0
        except Exception:
            # Swallow errors; telemetry is best-effort
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._max_consecutive_failures:
                self._disable()

    def close(self) -> None:
        if self._debug:
            print("[deepgram][telemetry] close() called")
            
        if self._synchronous:
            # Flush any staged events synchronously
            buf = getattr(self, "_buffer_sync", [])
            if buf:
                if self._debug:
                    print(f"[deepgram][telemetry] flushing {len(buf)} staged events on close")
                try:
                    self._flush(buf)
                finally:
                    self._buffer_sync = []  # type: ignore[attr-defined]
            elif self._debug:
                print("[deepgram][telemetry] no staged events to flush")
            try:
                self._client.close()
            except Exception:
                pass
            return
        # First, try to flush any pending events
        if self._debug:
            print(f"[deepgram][telemetry] flushing pending events, queue size: {self._queue.qsize()}")
        try:
            self.flush()
        except Exception:
            if self._debug:
                raise
        
        self._stop_event.set()
        # Drain any remaining events synchronously to ensure a final flush
        drain: List[dict] = []
        try:
            while True:
                drain.append(self._queue.get_nowait())
        except queue.Empty:
            pass
        if drain:
            if self._debug:
                print(f"[deepgram][telemetry] draining {len(drain)} remaining events on close")
            try:
                self._flush(drain)
            except Exception:
                if self._debug:
                    raise
        elif self._debug:
            print("[deepgram][telemetry] no remaining events to drain")
        # Give the worker a moment to exit cleanly
        self._worker.join(timeout=1.0)
        try:
            self._client.close()
        except Exception:
            pass

    def flush(self) -> None:
        """
        Force a synchronous flush of any staged or queued events.

        - In synchronous mode, this flushes the local buffer immediately.
        - In background mode, this drains the queue and flushes in the caller thread.
          Note: this does not capture items already pulled into the worker's internal buffer.
        """
        if self._disabled:
            return
        if self._synchronous:
            buf = getattr(self, "_buffer_sync", [])
            if buf:
                try:
                    self._flush(buf)
                finally:
                    self._buffer_sync = []  # type: ignore[attr-defined]
            return
        drain: List[dict] = []
        try:
            while True:
                drain.append(self._queue.get_nowait())
        except queue.Empty:
            pass
        if drain:
            self._flush(drain)

    @staticmethod
    def _gzip_iter(data_iter: typing.Iterator[bytes]) -> typing.Iterator[bytes]:
        compressor = zlib.compressobj(wbits=31)
        for chunk in data_iter:
            if not isinstance(chunk, (bytes, bytearray)):
                chunk = bytes(chunk)
            if chunk:
                out = compressor.compress(chunk)
                if out:
                    yield out
        tail = compressor.flush()
        if tail:
            yield tail

    def _disable(self) -> None:
        # Toggle off for this session: drop all future events, stop worker, clear queue fast
        self._disabled = True
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass
        self._stop_event.set()


