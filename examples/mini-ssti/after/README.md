# mini-ssti — after

Template preview now follows an ordinary draft workflow:

1. create a draft with `/draft?template=...`;
2. preview that stored draft with the returned `/preview?id=...` path.

The same attacker-controlled template is evaluated against the same server-side context. The SSTI primitive and learning objective are unchanged, but a draft must exist before the vulnerable preview can be exercised.
