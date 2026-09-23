# Outreach plan

The goal of the first public outreach is to get **useful design feedback from CTF authors**, not to maximize impressions.

## Canonical feedback path

Send external reviewers to the GitHub issue form:

https://github.com/aleff-github/NiceTryGPT/issues/new?template=ctf-author-feedback.yml

This keeps feedback public, structured, and tied to the project.

Useful feedback is about:

- fairness;
- additional human effort;
- whether the intended learning objective was preserved;
- which challenge classes suffer from cheap LLM shortcuts;
- which transformation patterns feel artificial.

Model benchmarks are not required for this phase.

## Channel 1 — GitHub

This is the default destination.

Use:

- the v0.5.0 release;
- README before/after tables;
- the Human Cost Gate;
- the feedback issue form.

Do not add a discussion forum or another platform until there is enough incoming feedback to justify one.

## Channel 2 — direct CTF-organizer outreach

Prefer a very small number of personalized contacts over mass messaging.

A good target is an organizer, challenge author, or cybersecurity educator who publicly provides a project/event contact channel.

Suggested process:

1. read one of their recent public CTF/event pages;
2. make sure web/security challenge design is relevant to them;
3. use an official public contact channel;
4. send one short message;
5. ask for methodology feedback, not promotion;
6. do not follow up repeatedly if there is no response.

CTFtime is useful for discovering current events and organizer identities, but it is primarily an event directory rather than the place to advertise NiceTryGPT itself.

## Channel 3 — OWASP communities

OWASP mailing lists are public collaboration channels and most are open for membership.

Only use a list when NiceTryGPT is genuinely relevant to that specific chapter/project/community. Do not broadcast the same message across multiple lists.

The useful framing is educational:

- preserving CTF learning objectives;
- measuring human cost;
- designing training labs in the presence of capable LLMs.

Reference:

https://owasp.org/legal/mailing-lists

## Channel 4 — Hacker News

NiceTryGPT is executable, open source, and can be tried without signup, so its repository is structurally suitable for a Show HN.

However, HN currently emphasizes two constraints:

- do not use HN primarily for self-promotion;
- submission text should be written by the human poster, not generated or edited by an LLM.

For that reason the repository deliberately does **not** include a ready-to-paste HN body.

Before submitting, read:

- https://news.ycombinator.com/showhn.html
- https://news.ycombinator.com/newsguidelines.html

If posting, use the factual checklist in `launch-kit.md` and write the actual text yourself.

## Channel 5 — Reddit and similar communities

Rules change frequently and differ by subreddit/community.

Do not maintain a permanent “post here” list in the repository.

Before sharing:

1. read the current sidebar/rules;
2. verify self-promotion is allowed;
3. participate as a community member rather than using an account only for promotion;
4. disclose that you maintain the project;
5. ask for technical feedback rather than votes or traffic.

If the rules are unclear, skip the channel.

## Outreach log

Record actual outreach in issue #7 using this compact format:

```text
Date:
Channel:
Audience:
Link/contact:
Message type:
Response:
Actionable feedback:
Follow-up:
```

Do not record private email addresses or private conversation content without permission.

## Stop condition

Pause outreach and review the project after either:

- 5 substantive external feedback responses; or
- 10 targeted outreach attempts with no meaningful response.

The next change should be driven by the feedback, not by a desire to keep posting.
