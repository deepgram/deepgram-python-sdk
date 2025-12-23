#!/usr/bin/env python3
"""
Post-generation script to patch auto-generated client files.

Replaces websockets imports with our wrapper module.
"""

import re
import sys
from pathlib import Path


# Pattern to find websockets sync client imports
WEBSOCKETS_SYNC_IMPORT_PATTERN = r"import websockets\.sync\.client as websockets_sync_client"

# Pattern to find websockets async client imports
WEBSOCKETS_ASYNC_IMPORT_PATTERN = r"from websockets\.legacy\.client import connect as websockets_client_connect|from websockets import connect as websockets_client_connect"

# Pattern to find websockets module imports
WEBSOCKETS_MODULE_PATTERN = r"^import websockets$"

# Pattern to find websockets sync connection imports
WEBSOCKETS_SYNC_CONNECTION_PATTERN = r"import websockets\.sync\.connection as websockets_sync_connection"

# Pattern to find WebSocketClientProtocol imports
WEBSOCKETS_PROTOCOL_PATTERN = (
    r"from websockets\.legacy\.client import WebSocketClientProtocol|from websockets import WebSocketClientProtocol"
)


def has_patch_already(content: str) -> bool:
    """Check if file already has our patch."""
    return (
        "from ...core.websocket_wrapper import" in content or "from deepgram.core.websocket_wrapper import" in content
    )


def patch_file(file_path: Path) -> bool:
    """Patch a single file if it needs patching."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return False

    # Skip if already patched
    if has_patch_already(content):
        return False

    # Check if file has websockets imports
    has_sync_import = bool(re.search(WEBSOCKETS_SYNC_IMPORT_PATTERN, content))
    has_async_import = bool(re.search(WEBSOCKETS_ASYNC_IMPORT_PATTERN, content))
    has_module_import = bool(re.search(WEBSOCKETS_MODULE_PATTERN, content, re.MULTILINE))
    has_sync_connection = bool(re.search(WEBSOCKETS_SYNC_CONNECTION_PATTERN, content))
    has_protocol_import = bool(re.search(WEBSOCKETS_PROTOCOL_PATTERN, content))

    if not (has_sync_import or has_async_import or has_module_import or has_sync_connection or has_protocol_import):
        return False

    modified = False
    lines = content.split("\n")

    # Determine relative import depth
    # Files are in listen/v1/, speak/v1/, agent/v1/, etc.
    # They use ...core.api_error (3 dots), which means 3 package levels up
    # From agent/v1/client.py: ... = deepgram package, so ...core = deepgram.core
    # So we always use 3 dots to match existing imports
    relative_import = "...core.websocket_wrapper"

    # Patch websockets module import
    for i, line in enumerate(lines):
        if re.search(WEBSOCKETS_MODULE_PATTERN, line):
            # Replace: import websockets
            # With: from ...core.websocket_wrapper import websockets
            indent = re.match(r"(\s*)", line).group(1) if re.match(r"(\s*)", line) else ""
            lines[i] = f"{indent}from {relative_import} import websockets  # noqa: E402"
            modified = True
            break

    # Patch websockets.exceptions import
    for i, line in enumerate(lines):
        if "import websockets.exceptions" in line:
            # Replace: import websockets.exceptions
            # With: from ...core.websocket_wrapper import websockets
            # Note: websockets.exceptions is accessible via websockets.exceptions
            indent = re.match(r"(\s*)", line).group(1) if re.match(r"(\s*)", line) else ""
            # We'll import websockets which includes exceptions, so we can remove this line
            # or keep it for clarity - let's replace it
            lines[i] = f"{indent}from {relative_import} import websockets  # noqa: E402"
            modified = True
            break

    # Patch sync connection import
    for i, line in enumerate(lines):
        if re.search(WEBSOCKETS_SYNC_CONNECTION_PATTERN, line):
            # Replace: import websockets.sync.connection as websockets_sync_connection
            # With: from ...core.websocket_wrapper import websockets_sync_connection
            indent = re.match(r"(\s*)", line).group(1) if re.match(r"(\s*)", line) else ""
            lines[i] = f"{indent}from {relative_import} import websockets_sync_connection  # noqa: E402"
            modified = True
            break

    # Patch sync import - replace the import line
    for i, line in enumerate(lines):
        if re.search(WEBSOCKETS_SYNC_IMPORT_PATTERN, line):
            # Replace: import websockets.sync.client as websockets_sync_client
            # With: from ...core.websocket_wrapper import websockets_sync_client
            indent = re.match(r"(\s*)", line).group(1) if re.match(r"(\s*)", line) else ""
            lines[i] = f"{indent}from {relative_import} import websockets_sync_client  # noqa: E402"
            modified = True
            break

    # Patch async import - handle try/except block for connect
    try_block_start = None
    for i, line in enumerate(lines):
        if "try:" in line and i + 1 < len(lines) and re.search(WEBSOCKETS_ASYNC_IMPORT_PATTERN, lines[i + 1]):
            try_block_start = i
            break

    if try_block_start is not None:
        # Replace the try branch import
        indent = (
            re.match(r"(\s*)", lines[try_block_start + 1]).group(1)
            if re.match(r"(\s*)", lines[try_block_start + 1])
            else ""
        )
        lines[try_block_start + 1] = f"{indent}from {relative_import} import websockets_client_connect  # noqa: E402"

        # Replace the except branch import if it exists
        if try_block_start + 2 < len(lines) and "except ImportError:" in lines[try_block_start + 2]:
            if try_block_start + 3 < len(lines):
                except_indent = (
                    re.match(r"(\s*)", lines[try_block_start + 3]).group(1)
                    if re.match(r"(\s*)", lines[try_block_start + 3])
                    else indent
                )
                lines[try_block_start + 3] = (
                    f"{except_indent}from {relative_import} import websockets_client_connect  # noqa: E402"
                )
        modified = True

    # Patch WebSocketClientProtocol import - handle try/except block
    protocol_try_block_start = None
    for i, line in enumerate(lines):
        if "try:" in line and i + 1 < len(lines) and re.search(WEBSOCKETS_PROTOCOL_PATTERN, lines[i + 1]):
            protocol_try_block_start = i
            break

    if protocol_try_block_start is not None:
        # Replace the try branch import
        indent = (
            re.match(r"(\s*)", lines[protocol_try_block_start + 1]).group(1)
            if re.match(r"(\s*)", lines[protocol_try_block_start + 1])
            else ""
        )
        # Check if there are multiple imports on the same line or separate lines
        if "WebSocketClientProtocol" in lines[protocol_try_block_start + 1]:
            lines[protocol_try_block_start + 1] = (
                f"{indent}from {relative_import} import WebSocketClientProtocol  # type: ignore  # noqa: E402"
            )

        # Replace the except branch import if it exists
        if protocol_try_block_start + 2 < len(lines) and "except ImportError:" in lines[protocol_try_block_start + 2]:
            if (
                protocol_try_block_start + 3 < len(lines)
                and "WebSocketClientProtocol" in lines[protocol_try_block_start + 3]
            ):
                except_indent = (
                    re.match(r"(\s*)", lines[protocol_try_block_start + 3]).group(1)
                    if re.match(r"(\s*)", lines[protocol_try_block_start + 3])
                    else indent
                )
                lines[protocol_try_block_start + 3] = (
                    f"{except_indent}from {relative_import} import WebSocketClientProtocol  # type: ignore  # noqa: E402"
                )
        modified = True

    if modified:
        try:
            file_path.write_text("\n".join(lines), encoding="utf-8")
            print(f"Patched: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}", file=sys.stderr)
            return False

    return False


def find_client_files(root_dir: Path) -> list[Path]:
    """Find all client files that might need patching."""
    client_files = []

    # Look for client.py files in listen, speak, agent directories
    for pattern in [
        "**/listen/**/client.py",
        "**/speak/**/client.py",
        "**/agent/**/client.py",
        "**/listen/**/raw_client.py",
        "**/speak/**/raw_client.py",
        "**/agent/**/raw_client.py",
        "**/listen/**/socket_client.py",
        "**/speak/**/socket_client.py",
        "**/agent/**/socket_client.py",
    ]:
        client_files.extend(root_dir.glob(pattern))

    return sorted(set(client_files))


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent / "src" / "deepgram"

    if not root_dir.exists():
        print(f"Error: Directory {root_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    client_files = find_client_files(root_dir)

    if not client_files:
        print("No client files found to patch")
        return

    patched_count = 0
    for file_path in client_files:
        if patch_file(file_path):
            patched_count += 1

    print(f"\nPatched {patched_count} file(s)")


if __name__ == "__main__":
    main()
