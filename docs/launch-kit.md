# Launch kit

This file keeps public messaging consistent while NiceTryGPT is still an early project.

## One-line description

> NiceTryGPT minimally transforms existing CTF challenges to reduce cheap LLM shortcuts without deliberately making them harder for humans.

## Short description

NiceTryGPT is a small Agent Skill for CTF authors. It first solves a challenge end-to-end, identifies one cheap LLM shortcut, applies the smallest useful transformation, and solves it again. The vulnerability class and learning objective stay the same, and human cost is explicitly bounded.

## GitHub / social post

> ☕ Your CTF got one-shot by an LLM? Nice try.
>
> I released **NiceTryGPT v0.3.0**: a tiny Agent Skill that solves an existing CTF first, identifies cheap LLM shortcuts, then applies the smallest useful transformation while preserving the vulnerability and keeping human cost bounded.
>
> Three reproducible before/after demos are included: IDOR, path traversal, and SQL injection. The suite checks both shortcut reduction and preservation of the intended vulnerability.
>
> **Less pattern matching. More actual hacking.**
>
> https://github.com/aleff-github/NiceTryGPT

## Hacker News

Do **not** copy an LLM-written submission body to Hacker News.

Current HN guidance explicitly asks users to write submission text themselves and discourages using the site primarily for promotion.

If the maintainer decides to submit NiceTryGPT as a Show HN, write the post manually and cover these factual points in your own words:

- you built NiceTryGPT for existing CTF challenges;
- it requires a baseline solve before any transformation;
- it tries to remove one cheap shortcut with the smallest useful change;
- it preserves the vulnerability class and learning objective;
- v0.3.0 includes IDOR, path traversal, and SQL injection demos plus external GPT evaluation;
- CI checks deterministic before/after properties;
- fresh-context GPT results are published for Interstellar Ingress and DiceMiner; no cross-model replication claim is made;
- you want feedback specifically on the Human Cost Gate and fairness of transformations.

Suggested title only:

`Show HN: NiceTryGPT – reduce cheap LLM shortcuts in existing CTFs`

Before posting, re-read:

- https://news.ycombinator.com/showhn.html
- https://news.ycombinator.com/newsguidelines.html

## CTF organizer outreach

> Hi — I’m experimenting with a small open-source project called NiceTryGPT for adapting existing CTF challenges in the LLM era.
>
> Instead of making challenges broadly harder, it requires a verified baseline solve and then tries to remove one cheap model shortcut with a minimal change. The original vulnerability and learning objective should remain intact.
>
> I’ve published v0.3.0 with three tiny reproducible examples and preliminary external GPT evidence and would be interested in feedback from challenge authors on whether the methodology matches real CTF design constraints:
>
> https://github.com/aleff-github/NiceTryGPT
>
> There is also a short structured feedback form:
>
> https://github.com/aleff-github/NiceTryGPT/issues/new?template=ctf-author-feedback.yml

## Good places to share

Use a staged launch rather than posting everywhere at once:

1. GitHub profile / personal portfolio;
2. a handful of CTF organizers through their public project/event contact channels;
3. one relevant cybersecurity or education community whose rules permit project feedback posts;
4. Hacker News only if the maintainer is already participating there and writes the submission text personally;
5. after real evaluation data exists, a deeper technical article with raw results.

The goal of the first launch is **feedback and contributors**, not inflated reach.

See [`outreach-plan.md`](outreach-plan.md) for channel-specific guidance.

## What to show

Lead with concrete evidence:

- the 30-second installation;
- the three before/after examples;
- green E2E tests;
- the CI-enforced report contract;
- the Human Cost Gate;
- the downloadable v0.3.0 release;
- the structured CTF-author feedback form.

A short terminal recording or GIF can be added later, but it is not required for the first public post.

## What not to claim

Do not say:

- “AI-proof CTFs”;
- “the first anti-LLM CTF system”;
- “LLMs cannot solve these challenges”;
- “human difficulty is unchanged” as an empirical fact before human testing;
- “NiceTryGPT beats Claude/GPT” or any universal resistance claim.

Prefer:

- “reduces an identified cheap shortcut”;
- “designed to keep human cost small”;
- “same vulnerability and learning objective”;
- “fresh-context GPT evaluation is published with explicit limitations.”

## When evaluation results arrive

The public message can become stronger only after the raw runs are committed.

Then publish:

- model/version identifiers;
- protocol version;
- before/after solve rates;
- successful-solve action counts;
- shortcut-attempt rates;
- failures and anomalies;
- limitations.

Keep raw data available so others can reproduce the summary.
