# Hermes

A lightweight lifecycle manager for threaded asyncio applications.

# Motivation

Long-running Python applications often combine threads and "asyncio". While Python provides excellent concurrency primitives, it leaves orchestration to the developer.

This project was created to centralize that orchestration.

Instead of scattering event loop creation, thread management, exception handling, shutdown logic, and task scheduling throughout an application, Hermes provides a small set of components that own those responsibilities.

The goal is simple:

- One owner for the event loop.
- One owner for worker threads.
- One place to submit background tasks.
- One place to observe failures.
- One place to perform graceful shutdown.

---

# Features

## ThreadManager

A wrapper around "ThreadPoolExecutor" that provides:

- Background worker execution
- Centralized exception handling
- Automatic logging of worker thread failures
- Graceful executor shutdown

No more silent thread failures hidden inside "Future" objects.

---

## LoopManager

A dedicated manager for an asyncio event loop running in its own thread.

Responsibilities include:

- Creating and owning an event loop
- Running the loop in a background thread
- Thread-safe task submission
- Task naming
- Duplicate task prevention
- Centralized task exception handling
- Graceful task cancellation
- Event loop shutdown
- Async generator cleanup

---

# Design Philosophy

## Explicit ownership

Each resource has exactly one owner.

- ThreadManager owns worker threads.
- LoopManager owns the event loop.
- LoopManager owns task scheduling.
- LoopManager owns task shutdown.

This keeps responsibilities isolated and predictable.

---

## Lifecycle first

The project is built around lifecycle management rather than simply "running async code."

Every managed resource follows a clear lifecycle.

Create
    ↓
Run
    ↓
Schedule Work
    ↓
Handle Errors
    ↓
Cancel Tasks
    ↓
Shutdown
    ↓
Release Resources

---

## Fail loudly

Unhandled exceptions should never disappear.

Worker thread exceptions are surfaced automatically.

Async task exceptions are detected through completion callbacks and logged with full tracebacks.

---

## Defensive concurrency

Submitting the same long-running task repeatedly is an easy mistake to make in asynchronous systems.

Hermes supports task deduplication by name to prevent accidentally spawning duplicate background tasks.

---

## Example
```
# to view logs cleanly you can import my log.py file,
or use the logging lib and set level to debug

from thread_manager import ThreadManager
from loop_manager import LoopManager

tm = ThreadManager()
lm = LoopManager()

tm.start(lm.run_loop) #start event loop thread

lm.submit_task(
    "market-feed",
    websocket_consumer
) # name is required so each task can be differentiated from the others

...

lm.submit_task(
    "shutdown",
    lm.stop
) # graceful shutdown

tm.shutdown()
```

## Update
```
hm = HermesManager()


hm.start_event_loop()


hm.add_task(fn, *args, **kwargs)

hm.add_thread(fn, *args, **kwargs)

hm.add_periodic_task(interval, callback, *args, **kwargs)
```
---

## Why?

This project exists because concurrency bugs are often subtle.

Examples include:

- silent worker thread crashes
- forgotten task exceptions
- duplicate background tasks
- improper event loop shutdown
- resource leaks
- lifecycle bugs

The goal is to make these problems visible instead of silent.

---

# Current Status

Hermes is intentionally lightweight.

The focus is correctness, observability, and predictable lifecycle management rather than providing another asynchronous framework.

It is designed as a reusable building block for long-running Python services such as:

- WebSocket clients
- Trading systems
- Background workers
- Automation services
- Daemons
- Monitoring systems

---

# Future Ideas

- Task registry and inspection
- Restart policies
- Task groups
- Periodic task scheduling
- Health monitoring
- Metrics integration
- Configurable exception policies
- Async context manager support
- Optional process management

---

# Philosophy

«Concurrency is difficult enough without lifecycle being an afterthought.»

Hermes aims to make ownership explicit, failures visible, and shutdown predictable.
