---
type: prd
title: "Self-Serve Onboarding"
slug: "self-serve-onboarding"
status: draft            # draft · review · approved · shipped · archived
owner: "alex"
projects: "self-serve-onboarding"   # parent project (lives in that project's docs/)
jira_epic: "PAY-1310"
target_date: 2026-08-15
tags: [growth, onboarding]
---

## Summary

Let new merchants onboard and take their first payment without a support handoff. A guided
setup flow plus automated verification replaces today's manual review, cutting
time-to-first-payment and support load.

## Problem & context

Onboarding requires a manual review step that adds 2–3 days and generates a support ticket
per merchant. That delay is the single biggest drop-off point in activation, and the ticket
volume scales linearly with signups. Evidence: current median time-to-first-payment is ~3
business days; ~1 support ticket per new merchant tagged `onboarding`.

## Goals & non-goals

**Goals**

- Merchant reaches first successful payment with no human in the loop for the common case.
- Cut median time-to-first-payment from ~3 days to under 1 hour.
- Reduce onboarding-tagged support tickets per merchant by 60%.

**Non-goals**

- Redesigning the post-onboarding merchant dashboard.
- Removing manual review entirely — high-risk merchants still route to a human.

## Users & use cases

Primary: a new small/medium merchant setting up their first payment integration, self-serve,
outside support hours. Secondary: the risk team, who need auto-approved merchants to stay
within fraud tolerances.

## User stories

- As a **new merchant**, I want to **complete setup and verification in one sitting** so that **I can take a payment the same day**.
- As a **new merchant**, I want to **know exactly what's left to go live** so that **I'm not waiting on an opaque review**.
- As a **risk analyst**, I want **auto-approved merchants scored and logged** so that **I can audit and tune the threshold**.

## Requirements

| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| R1 | Guided setup flow with a visible completion checklist | P0 | Empty/partial states must be resumable |
| R2 | Automated identity + bank verification | P0 | Third-party verification provider |
| R3 | Risk-scored auto-approve with manual fallback | P0 | Threshold owned by risk; see PAY-1310 |
| R4 | First-payment confirmation + next steps | P1 | |
| R5 | Progress email/resume link if merchant drops off | P2 | |

_Priority: P0 = must-have for launch · P1 = important · P2 = nice-to-have._

## UX & design notes

Single guided flow with a persistent checklist. Key states: fresh start, resumed (partial),
verification pending, verification failed → manual fallback, approved → take first payment.

## Success metrics

| Metric | Baseline | Target | How measured |
|--------|----------|--------|--------------|
| Median time-to-first-payment | ~3 days | < 1 hour | activation funnel |
| Onboarding tickets / merchant | ~1.0 | ≤ 0.4 | support tags |
| Fraud rate on auto-approved (guardrail) | current | no regression | risk dashboard |

## Rollout & launch

Internal test merchants → 10% of new signups behind a flag → GA. Go/no-go: auto-approve
fraud rate within tolerance for two full weeks at 10%.

## Open questions

- [ ] What risk score threshold balances auto-approve rate against fraud tolerance?
- [ ] Do we need KYC re-verification for merchants who resume after >7 days?

## Appendix

Links to research (`09-knowledge/research/`), experiments (`docs/experiments/`), decisions
(`04-decisions/`), and external docs. Jira: [PAY-1310](https://acme.atlassian.net/browse/PAY-1310).
