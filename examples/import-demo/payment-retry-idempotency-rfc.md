---
title: "RFC: Idempotency keys for payment retries"
status: review
authors: [alex, sam]
epic: PAY-1200
last_updated: 2026-07-08
---

# RFC: Idempotency keys for payment retries

> An engineering design doc (RFC) for the **Checkout Reliability** effort. Hosted in a repo as
> plain Markdown — the kind of external doc you'd want to pull into your own planning.

## Summary

Introduce end-to-end **idempotency keys** on the payment-gateway → provider call path so that
retries are safe and bounded. Today an unbounded retry storm during a provider slowdown is the
single biggest driver of checkout latency breaches. This design makes every retry replay the
same logical transaction instead of risking a double charge, and pairs it with a capped retry
budget and backpressure.

## Context & problem

Checkout P99 latency breached its 800ms SLA in three of the last six weeks, peaking at 4.2s
during the June 20 incident. The dominant cause is the provider client retrying failed calls
with no upper bound and no idempotency guarantee, so the safe-but-slow fallback is "retry
forever," which amplifies load exactly when the provider is already degraded.

## Goals & non-goals

**Goals**

- Every payment mutation carries a client-generated idempotency key, stable across retries.
- Retries are capped by a per-request budget with exponential backoff + jitter.
- No double charges under retry, verified by a replay test suite.

**Non-goals**

- Migrating to a new payment provider (tracked separately).
- Changing the customer-facing checkout UI.

## Proposed design

1. **Key generation.** The checkout service mints a UUIDv7 idempotency key per payment intent
   and persists it with the order before the first provider call.
2. **Gateway middleware.** A middleware attaches the key as the `Idempotency-Key` header and
   short-circuits duplicate in-flight requests for the same key.
3. **Retry budget.** The provider client gets a token-bucket retry budget; when exhausted it
   fails fast to the queue rather than hammering the provider.
4. **Backpressure.** Concurrency limits + timeouts on the client, surfaced as a first-class
   metric.

## Detailed design

- **Data model** — new `payment_intents.idempotency_key` column (unique), plus a
  `provider_calls` audit row keyed by it.
- **API** — the internal `POST /charges` contract gains a required `idempotency_key` field;
  the provider adapter forwards it as a header.
- **Key flows** — first attempt writes the audit row; retries match on the key and return the
  recorded result if the provider already committed.

## Alternatives considered

- **Dedupe at the provider only** — rejected: not all providers honor idempotency headers
  consistently, so we need our own record of truth.
- **Global rate limit instead of per-request budget** — rejected: too blunt, penalizes healthy
  traffic during a localized slowdown.

## Rollout

Behind a `payments.idempotency` flag, ramped 1% → 50% → 100% over two weeks, with the June-20
incident scenario replayed in staging as the go/no-go gate.

## Action items

- [ ] **Alex** — Socialize this RFC with the Commerce tribe and get architecture sign-off
- [ ] **Alex** — Break PAY-1200 down into implementation tickets and sequence the rollout
- [ ] **Sam** — Implement the idempotency-key middleware in the payment gateway
- [ ] **Priya** — Add the retry budget + backpressure to the provider client
- [ ] **Dana** — Ship the latency/error dashboard with 1-minute alerting before ramp
