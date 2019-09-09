# sharedStateC.py

This is an EXAMPLE PLUGIN.

Object based shared state.

This example aims to show that you can store state in callable object instances.

The shared state stores two counters one (sequential) will be incremented
sequentially by each callback and will keep incrementing across event ids.

The second counter (rotating) will be incremented by each successive callback
but will be reset at each new event.

## Args

No settings.
