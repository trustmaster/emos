---
type: meeting
title: "Sprint Planning — Jun 29"
date: 2026-06-29
attendees: [alex, sam, dana, priya, marco]
projects: [checkout-reliability, self-serve-onboarding]
tags: [planning]
---

## Agenda

1. Checkout Reliability — next steps post-ADR
2. Self-Serve Onboarding — kickoff scope

## Notes

### Checkout Reliability

ADR-0001 accepted. Next: backpressure + provider timeout (@Sam), roll alerting to
on-call (@Dana). Idempotency shipping this week (@Priya).

### Self-Serve Onboarding

Starting the guided setup flow (@Marco). Fraud edge cases need a manual fallback.

## Action Items

- [ ] @Sam: add backpressure to the provider client
- [ ] @Dana: roll out latency alerting to on-call
- [ ] @Marco: draft the guided setup flow
