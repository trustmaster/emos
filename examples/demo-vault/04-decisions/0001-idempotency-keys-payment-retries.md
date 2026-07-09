---
type: decision
id: "ADR-0001"
title: "Idempotency keys for payment retries"
status: accepted
date: 2026-06-26
deciders: ["alex", "sam"]
projects: [checkout-reliability]
tags: ["payments", "reliability"]
superseded_by: null
---

## Context

The June 20 checkout incident was caused by uncapped, non-idempotent retries: a
slow provider response produced duplicate in-flight charges risk and a retry
storm. We need retries that are both safe (no double charge) and bounded.

## Decision

Attach a client-generated **idempotency key** to every payment request and reuse
it across retries. Cap retries at 3 with exponential backoff and a 2s per-attempt
timeout. The provider dedupes on the key.

## Consequences

### Positive

- Retries can't double-charge; safe to retry aggressively within the cap.
- Bounded retries prevent storm amplification.

### Negative

- Requires storing keys for the retry window; small state overhead.

### Risks

- Key collisions if generation is weak — use UUIDv4 per logical attempt.

## Alternatives Considered

### No retries

Rejected — transient provider blips would surface as user-facing failures.

### Server-side dedupe only

Rejected — doesn't bound client retry volume during a brownout.
