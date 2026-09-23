# mini-ssti — before

A tiny server-side template preview accepts the template directly in a stateless request:

- `/preview?template=Hello%20{{name}}`

The intentionally small template engine resolves names from server-side context. Supplying `{{flag}}` therefore exposes the runtime flag.

The engine is a safe toy implementation for this demo; it does not evaluate arbitrary Python or operating-system code.
