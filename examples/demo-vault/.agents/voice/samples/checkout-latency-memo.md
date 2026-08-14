# Sample: checkout latency memo

**What this is.** An email Alex sent to Dana (director, Commerce) in May 2026, asking for a
two-week hold on the roadmap to fix checkout latency. Written in about twenty minutes, which
is part of why it's useful — it shows the habits that survive time pressure.

**What it demonstrates.** The conclusion lands in the first two sentences. Every number
carries its source. The ask is specific and dated. No em-dashes, no hedging adjectives, and
it stops the moment the reader can act.

**Stripped:** the original had a screenshot of the latency dashboard and a table of
per-endpoint timings. Both removed — they're structure, not voice.

---

Dana,

I want two weeks of the platform team's roadmap back to fix checkout latency, starting the
26th. We've spent three sprints working around it and the workarounds are now the problem.

Here's where it stands. p99 on the checkout confirm endpoint sat at 2.4s through April, per
the weekly dashboard. Our budget is 600ms. The gap isn't one slow query, it's the retry loop
we added in February to absorb the payment provider's timeouts. That loop turned a 3% failure
rate into a 0.2% failure rate, so it earned its place, but it also triples our own latency
whenever the provider degrades. Both things are true.

We've tried the cheap fixes. Connection pooling bought us about 200ms in March. Caching the
merchant config bought maybe 100ms more, though I'd treat that number as soft since we
measured it during a low-traffic week. Neither touches the retry loop, which is where the
remaining 1.5s lives.

The fix is idempotency keys on the payment calls, so a retry becomes cheap instead of a full
re-run. Marco scoped it at two weeks with one engineer, assuming the payments team can review
inside their normal cycle. If review slips, so does the estimate.

The alternative is to keep absorbing it. I don't recommend that, and I want to be honest that
my reason is partly qualitative: support tickets mentioning "stuck at payment" are up, but I
can't cleanly attribute them to latency versus the provider's own outages.

So the ask: two weeks of Marco's time starting the 26th, and your sign-off by Friday so we can
sequence it before the Q3 planning freeze. If the answer is no, tell me what to cut instead
and I'll bring you the trade.

Alex
