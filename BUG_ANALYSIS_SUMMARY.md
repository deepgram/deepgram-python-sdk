# Bug Analysis Summary: `start_listening()` Blocking Issue

## 🐛 The Problem

You're experiencing a bug where `connection.start_listening()` never returns, preventing subsequent code from executing. **This is the expected behavior**, but it's poorly documented.

## 🔍 What's Happening

The `start_listening()` method contains an **infinite loop** that blocks until the websocket connection closes:

```python
def start_listening(self):
    self._emit(EventType.OPEN, None)
    try:
        for raw_message in self._websocket:  # ← Loops forever until connection closes
            parsed, is_binary = self._process_message(raw_message)
            self._emit(EventType.MESSAGE, parsed)
    finally:
        self._emit(EventType.CLOSE, None)
```

When you write:
```python
connection.start_listening()
print("I've started listening!")  # ← THIS NEVER EXECUTES
```

The print statement never runs because `start_listening()` doesn't return - it's designed to run until the connection closes.

## 📚 Documentation Issues

### Misleading Examples

The documentation shows examples that **cannot work as written**:

**❌ websockets-reference.md (line 52):**
```python
connection.start_listening()
connection.send_media(audio_bytes)  # Never executes!
```

**❌ README.md (line 62):**
```python
connection.start_listening()
# Any code here never runs!
```

### Correct Usage (From Working Examples)

**✅ Synchronous (requires threading):**
```python
import threading

threading.Thread(target=connection.start_listening, daemon=True).start()
# Now code continues executing
connection.send_media(audio_bytes)
```

**✅ Async (requires task):**
```python
import asyncio

listen_task = asyncio.create_task(connection.start_listening())
# Now code continues executing
await connection.send_media(audio_bytes)
```

## 🔧 Why Tests Pass

Tests work because they use **mock websockets** that return a finite set of messages and then stop. In production, real websockets keep connections open indefinitely.

## ✅ Solutions

### Quick Fix for Your Code

**If using sync:**
```python
import threading

# Start listening in background
threading.Thread(target=connection.start_listening, daemon=True).start()

# Now this will print!
print("I've started listening!")
```

**If using async:**
```python
import asyncio

# Start listening as a task
listen_task = asyncio.create_task(connection.start_listening())

# Now this will print!
print("I've started listening!")
```

### Recommended SDK Fixes

1. **Update documentation** in `websockets-reference.md` and `README.md` to show correct threading/task usage
2. **Add helper methods** like `start_listening_background()` that handle threading automatically
3. **Rename method** to `listen_until_closed()` to make blocking behavior explicit

## 📁 Affected Files

- `src/deepgram/listen/v1/socket_client.py`
- `src/deepgram/listen/v2/socket_client.py`
- `src/deepgram/speak/v1/socket_client.py`
- `src/deepgram/agent/v1/socket_client.py`
- `websockets-reference.md`
- `README.md`

## 🎯 Next Steps

1. ✅ Bug identified and documented
2. ⏭️ Fix documentation to show correct usage
3. ⏭️ Consider adding non-blocking helper methods
4. ⏭️ Add clear warnings in method docstrings about blocking behavior
