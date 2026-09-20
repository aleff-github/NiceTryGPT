# Resistance patterns

Use this file as a menu, not a checklist. Most challenges need zero or one pattern.

## Pattern break

Use when names, messages, or layout practically announce a textbook exploit. Rename or reframe the cue while leaving enough evidence for a player to form the same hypothesis naturally.

Good: a generic `receipt` identifier instead of a parameter literally named `admin_id`.

Bad: renaming every variable to random strings.

## Runtime discovery

Move one small solve-relevant fact into normal runtime behavior.

Good: a nearby activity endpoint reveals a valid object reference that the vulnerable endpoint fails to authorize.

Bad: a random secret generated on every request with no player-visible way to discover it.

## Context split

Place two simple clues in different but nearby application surfaces so the player must connect them.

Good: an order ID appears in recent activity and is accepted by an insecure receipt endpoint.

Bad: requiring clues from unrelated protocols, files, and services for an otherwise easy challenge.

## State dependency

Let a small amount of ordinary state affect the solve.

Good: a session-created resource must exist before an authorization bug can be exercised.

Bad: a five-step state machine that turns an easy challenge into an exploitation chain.

## Semantic decoy

Add a plausible attack surface that can be disproved quickly.

Good: a download endpoint looks traversal-prone but rejects traversal cleanly; one test is enough to move on.

Bad: multiple deep rabbit holes, fake flags, destructive traps, rate-limit punishment, or misleading evidence that costs substantial time.

## Selection rule

Choose the pattern that creates the largest reduction in cheap pattern matching for the smallest increase in human effort. If none clears that bar, make no change.
