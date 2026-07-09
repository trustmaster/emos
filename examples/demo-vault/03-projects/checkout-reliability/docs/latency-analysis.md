# Checkout latency analysis (working doc)

_Project-local working doc — lives in the project folder, not linked via `projects:`._

## June latency breakdown

| Week | P99 (ms) | Error rate | SLA breach |
|------|---------:|-----------:|:----------:|
| W23  | 740      | 0.4%       | no         |
| W24  | 910      | 0.9%       | yes        |
| W25  | 1,120    | 1.4%       | yes        |
| W26  | 780      | 0.5%       | no (post-fix) |

## Findings

- 80% of spike latency came from synchronous retries against the payment
  provider with no cap — a single slow provider call fanned out into 4–6 retries.
- The June 20 incident was a retry storm triggered by a provider brownout.

## Recommendation

Idempotency keys + capped retries + a 2s provider timeout. Tracked as the project's
approach; see the [hub](../checkout-reliability.md).
