# Bug Report: `connection.start_listening()` Blocks Indefinitely

## Summary

The `start_listening()` method in all socket clients **blocks indefinitely** and never returns until the websocket connection is closed. This prevents any code after the call from executing, which is not clearly documented and contradicts the examples shown in the documentation.

## Root Cause

The `start_listening()` method contains a blocking loop that iterates over websocket messages:

### Synchronous Version (e.g., `src/deepgram/listen/v1/socket_client.py:159-180`)

```python
def start_listening(self):
    self._emit(EventType.OPEN, None)
    try:
        for raw_message in self._websocket:  # ⚠️ BLOCKS HERE - never returns
            parsed, is_binary = self._process_message(raw_message)
            self._emit(EventType.MESSAGE, parsed)
    except (websockets.WebSocketException, JSONDecodeError) as exc:
        if not isinstance(exc, websockets.exceptions.ConnectionClosedOK):
            self._emit(EventType.ERROR, exc)
    finally:
        self._emit(EventType.CLOSE, None)
```

### Async Version (e.g., `src/deepgram/listen/v1/socket_client.py:69-90`)

```python
async def start_listening(self):
    await self._emit_async(EventType.OPEN, None)
    try:
        async for raw_message in self._websocket:  # ⚠️ BLOCKS HERE - never returns
            parsed, is_binary = self._process_message(raw_message)
            await self._emit_async(EventType.MESSAGE, parsed)
    except (websockets.WebSocketException, JSONDecodeError) as exc:
        if not isinstance(exc, websockets.exceptions.ConnectionClosedOK):
            await self._emit_async(EventType.ERROR, exc)
    finally:
        await self._emit_async(EventType.CLOSE, None)
```

## Affected Files

- `src/deepgram/listen/v1/socket_client.py` (lines 69-90, 159-180)
- `src/deepgram/listen/v2/socket_client.py` (lines 67-88, 157-178)
- `src/deepgram/speak/v1/socket_client.py` (lines 70-91, 161-182)
- `src/deepgram/agent/v1/socket_client.py` (lines 103-124, 218-239)

## Documentation Inconsistencies

### ❌ Incorrect Examples (Code That Will Never Work)

**websockets-reference.md:52**
```python
connection.start_listening()  # This blocks forever!

# This code below will NEVER execute:
connection.send_media(ListenV1MediaMessage(audio_bytes))
connection.send_control(ListenV1ControlMessage(type="KeepAlive"))
```

**README.md:62**
```python
connection.start_listening()  # This blocks forever!
# Any code here will never run
```

### ✅ Correct Usage (What Actually Works)

**Synchronous (examples/listen/v1/connect/main.py:28)**
```python
# Must use threading to avoid blocking
threading.Thread(target=connection.start_listening, daemon=True).start()
# Now subsequent code can execute
```

**Async (examples/listen/v1/connect/async.py:28)**
```python
# Must use asyncio.create_task() to avoid blocking
listen_task = asyncio.create_task(connection.start_listening())
# Now subsequent code can execute
```

## User Impact

When users follow the documentation examples in `websockets-reference.md` or `README.md`, they write code like:

```python
connection.start_listening()
print("I've started listening!")  # ❌ NEVER PRINTS
```

The message is never printed because `start_listening()` blocks forever in the loop.

## Recommendations

### Option 1: Fix Documentation (Quick Fix)

Update `websockets-reference.md` and `README.md` to show the correct usage:

**For Sync:**
```python
import threading

# Start listening in background thread
threading.Thread(target=connection.start_listening, daemon=True).start()

# Now you can send messages
connection.send_media(audio_bytes)
```

**For Async:**
```python
import asyncio

# Start listening as a task
listen_task = asyncio.create_task(connection.start_listening())

# Now you can send messages
await connection.send_media(audio_bytes)
```

### Option 2: Add Non-Blocking Alternative (Better UX)

Create a new method that doesn't block:

```python
def start_listening_background(self):
    """Start listening in a background thread (non-blocking)."""
    import threading
    threading.Thread(target=self.start_listening, daemon=True).start()

async def start_listening_task(self):
    """Start listening as an asyncio task (non-blocking)."""
    import asyncio
    return asyncio.create_task(self.start_listening())
```

### Option 3: Rename Current Method (Most Clear)

Rename `start_listening()` to `listen_until_closed()` to make the blocking behavior explicit, and add a non-blocking `start_listening()` wrapper.

## Related Files

All sync examples correctly use threading:
- `examples/listen/v1/connect/main.py:28`
- `examples/listen/v2/connect/main.py:28`
- `examples/speak/v1/connect/main.py:32`
- `examples/agent/v1/connect/main.py:79`

All async examples correctly use tasks:
- `examples/listen/v1/connect/async.py:28`
- `examples/listen/v2/connect/async.py:28`
- `examples/speak/v1/connect/async.py:31`
- `examples/agent/v1/connect/async.py:77`

But the documentation doesn't reflect this requirement!
