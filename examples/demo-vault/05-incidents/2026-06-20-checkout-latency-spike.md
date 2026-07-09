---
type: incident
id: "INC-2026-0620"
title: "Checkout latency spike"
severity: high
status: reviewed
date_detected: 2026-06-20
date_started: 2026-06-20
date_resolved: 2026-06-20
time_to_detect_days: 0
time_to_resolve_days: 0
impact:
  users_affected: "~3,400 checkout attempts"
  business_impact: "~1.9% checkout failure for 70 min"
  scope: "all regions, card payments"
owner: "sam"
opsgenie_link: null
confluence_link: null
projects: [checkout-reliability]
tags: [latency, payments]
---

## Summary

A payment-provider brownout triggered a retry storm; checkout P99 hit 4.2s and
failure rate reached 1.9% for ~70 minutes before retries were capped and the
provider recovered.

## Timeline

| Time | Event |
|------|-------|
| 2026-06-20 14:05 | Latency dashboard alert (P99 > 2s) |
| 2026-06-20 14:12 | On-call (Sam) engaged; provider brownout identified |
| 2026-06-20 14:40 | Emergency retry cap deployed |
| 2026-06-20 15:15 | Provider recovered; latency normal |

## Root Cause

Uncapped synchronous retries against a slow provider amplified load and latency.

## Impact

- **Users affected**: ~3,400 checkout attempts, ~1.9% failed
- **Duration**: ~70 minutes
- **Business impact**: elevated checkout failure; no data loss

## Action Items

- [ ] **Immediate**: cap provider retries (owner: @Sam, done 2026-06-20)
- [ ] **Short-term**: idempotency keys for safe retries (owner: @Priya) — see [ADR-0001](../04-decisions/0001-idempotency-keys-payment-retries.md)
- [ ] **Long-term**: backpressure + provider timeout (owner: @Sam)

## Lessons Learned

Retries without caps turn a provider blip into an outage. Idempotency + backpressure
are now the [Checkout Reliability](../03-projects/checkout-reliability/checkout-reliability.md) project's core.
