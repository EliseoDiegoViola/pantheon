# sharedStateA.py

This is an EXAMPLE PLUGIN.

Global variable shared state.

This plugin demoes how three callbacks can share state through a global variable.

The shared state stores two counters one (sequential) will be incremented
sequentially by each callback and will keep incrementing across event ids.

The second counter (rotating) will be incremented by each successive callback
but will be reset at each new event.

## Args

No settings.
