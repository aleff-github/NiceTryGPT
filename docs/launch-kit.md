# Launch kit

This file keeps public messaging consistent while NiceTryGPT is still an early project.

## One-line description

> NiceTryGPT minimally transforms existing CTF challenges to reduce cheap LLM shortcuts without deliberately making them harder for humans.

## Short description

NiceTryGPT is a small Agent Skill for CTF authors. It first solves a challenge end-to-end, identifies one cheap LLM shortcut, applies the smallest useful transformation, and solves it again. The vulnerability class and learning objective stay the same, and human cost is explicitly bounded.

## GitHub / social post

> ☕ Your CTF got one-shot by an LLM? Nice try.
>
> I released **NiceTryGPT v0.2.0**: a tiny Agent Skill that solves an existing CTF first, identifies cheap LLM shortcuts, then applies the smallest useful transformation while preserving the vulnerability and keeping human cost bounded.
>
> Three reproducible before/after demos are included: IDOR, path traversal, and SQL injection. The suite checks both shortcut reduction and preservation of the intended vulnerability.
>
> **Less pattern matching. More actual hacking.**
>
> https://github.com/aleff-github/NiceTryGPT

## Show HN draft

**Title**

`Show HN: NiceTryGPT – make CTFs less shortcut-friendly to LLMs without hurting humans`

**Body**

> I built NiceTryGPT, a small Agent Skill for CTF authors.
>
> The idea is deliberately narrow: take an existing challenge, solve it end-to-end first, identify one cheap LLM shortcut, make the smallest useful change, then solve it again.
>
> The transformation must preserve the vulnerability class, learning objective, prerequisite knowledge, and roughly the same human difficulty.
>
> v0.2.0 includes three dependency-free before/after demos (IDOR, path traversal, and SQL injection), a CI-enforced example acceptance contract, and a fresh-context evaluation protocol. I am not claiming the examples are AI-proof; independent multi-model results are intentionally not published until they are actually run.
>
> Feedback from CTF authors on the Human Cost Gate and transformation patterns would be especially useful.
>
> https://github.com/aleff-github/NiceTryGPT

## CTF organizer outreach

> Hi — I’m experimenting with a small open-source project called NiceTryGPT for adapting existing CTF challenges in the LLM era.
>
> Instead of making challenges broadly harder, it requires a verified baseline solve and then tries to remove one cheap model shortcut with a minimal change. The original vulnerability and learning objective should remain intact.
>
> I’ve published v0.2.0 with three tiny reproducible examples and would be interested in feedback from challenge authors on whether the methodology matches real CTF design constraints:
>
> https://github.com/aleff-github/NiceTryGPT

## Good places to share

Use a staged launch rather than posting everywhere at once:

1. GitHub profile / personal portfolio;
2. one technical community where CTF authors are likely to give useful feedback;
3. Show HN or a similar builder community;
4. relevant cybersecurity communities, respecting each community's self-promotion rules;
5. direct outreach to a small number of CTF organizers or educators;
6. after real evaluation data exists, a deeper technical article with results.

The goal of the first launch is **feedback and contributors**, not inflated reach.

## What to show

Lead with concrete evidence:

- the 30-second installation;
- the three before/after examples;
- green E2E tests;
- the CI-enforced report contract;
- the Human Cost Gate;
- the downloadable v0.2.0 release.

A short terminal recording or GIF can be added later, but it is not required for the first public post.

## What not to claim

Do not say:

- “AI-proof CTFs”;
- “the first anti-LLM CTF system”;
- “LLMs cannot solve these challenges”;
- “human difficulty is unchanged” as an empirical fact before human testing;
- “NiceTryGPT beats Claude/GPT/Gemini” before independent runs exist.

Prefer:

- “reduces an identified cheap shortcut”;
- “designed to keep human cost small”;
- “same vulnerability and learning objective”;
- “fresh-model evaluation is planned.”

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
