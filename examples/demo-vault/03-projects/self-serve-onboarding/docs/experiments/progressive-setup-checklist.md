---
type: experiment
title: "Progressive Setup Checklist"
slug: "progressive-setup-checklist"
status: proposed         # proposed · running · analyzing · concluded · abandoned
owner: "alex"
projects: "self-serve-onboarding"   # parent project (lives in that project's docs/experiments/)
metric: "activation rate (first payment within 24h)"
started: null            # YYYY-MM-DD when the experiment goes live
ended: null              # YYYY-MM-DD when it stops
---

## Hypothesis

We believe **showing a persistent, progressive completion checklist** for **new merchants in
the guided setup flow** will cause **a lift in 24h activation** because **merchants can see
exactly what's left and resume instead of dropping off**. We'll know it worked when
**treatment activation beats control by ≥ 3pp with no fraud-rate regression**.

## Metrics

| Role | Metric | Direction | Minimum detectable effect |
|------|--------|-----------|---------------------------|
| Primary | Activation: first payment within 24h | ↑ | +3pp |
| Guardrail | Fraud rate on auto-approved merchants | must not regress | — |
| Secondary | Median time-to-first-payment | ↓ | — |

## Variants

| Variant | Description | Traffic % |
|---------|-------------|-----------|
| Control | Current guided flow, no checklist | 50% |
| Treatment | Guided flow + persistent progressive checklist | 50% |

## Audience & sizing

- **Eligibility:** all new merchants entering self-serve onboarding (excludes manual-review routes).
- **Sample size / power:** ~4,300 merchants per variant to detect +3pp on a ~35% baseline at 80% power, 95% confidence.
- **Duration:** ~3 weeks at current signup volume to reach N across two full weekly cycles.

## Instrumentation

Events: `onboarding_started`, `checklist_step_completed`, `first_payment_succeeded`.
Dashboard: activation funnel by variant. Confirm tracking fires in staging **before** launch.

## Results

<!-- Append-only. Newest on top. Log readings as they come in. -->

### YYYY-MM-DD

- Primary: control X vs treatment Y (Δ, p-value / CI)
- Guardrail:
- Notes:

## Decision & next steps

- **Outcome:** ship / iterate / kill — and why.
- **Follow-ups:** what to do next (roll out, re-run, new hypothesis).
