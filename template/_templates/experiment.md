---
type: experiment
title: "Experiment Name"
slug: "experiment-name"
status: proposed         # proposed · running · analyzing · concluded · abandoned
owner: "{{owner_slug}}"
projects: "parent-project-slug"   # parent project (lives in that project's docs/experiments/)
metric: ""              # primary metric this experiment moves
started: null            # YYYY-MM-DD when the experiment goes live
ended: null              # YYYY-MM-DD when it stops
---

## Hypothesis

We believe **{change}** for **{audience}** will cause **{effect on primary metric}** because
**{reasoning}**. We'll know it worked when **{measurable threshold}**.

## Metrics

| Role | Metric | Direction | Minimum detectable effect |
|------|--------|-----------|---------------------------|
| Primary | | ↑ / ↓ | |
| Guardrail | | must not regress | |
| Secondary | | | |

## Variants

| Variant | Description | Traffic % |
|---------|-------------|-----------|
| Control | Current experience | 50% |
| Treatment | The change | 50% |

## Audience & sizing

- **Eligibility:** who's in the experiment.
- **Sample size / power:** N per variant for the MDE above at 80% power, 95% confidence.
- **Duration:** expected run length to reach that N (min 1–2 business cycles).

## Instrumentation

Events, dashboards, and the analysis query/link. Confirm tracking fires **before** launch.

## Results

<!-- Append-only. Newest on top. Log readings as they come in. -->

### YYYY-MM-DD

- Primary: control X vs treatment Y (Δ, p-value / CI)
- Guardrail:
- Notes:

## Decision & next steps

- **Outcome:** ship / iterate / kill — and why.
- **Follow-ups:** what to do next (roll out, re-run, new hypothesis).
