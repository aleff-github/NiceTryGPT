# mini-command-injection — after

The diagnostic surface now asks for a host, not a command:

- `/diagnostic?host=127.0.0.1`

The server still constructs a toy-shell command unsafely from player input, so the command-injection primitive is unchanged. The old `cmd=` shortcut no longer works; the player must identify that the host value reaches a command context.

No operating-system commands are executed by the demo.
