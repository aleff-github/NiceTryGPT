# mini-command-injection — before

A tiny diagnostic service sends the player-supplied `cmd` value directly to a deliberately restricted toy shell.

The interface itself practically names the exploit primitive:

- `/diagnostic?cmd=ping%20127.0.0.1`

Appending a second toy-shell command with `;` can read `CTF_FLAG`.

The toy shell is intentionally limited to the commands needed by this local demo; it does not execute operating-system commands.
