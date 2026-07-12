# import-url demo asset

A **public, standalone Markdown design doc** used to demo the [`/import-url`](../../template/.agents/skills/import-url/SKILL.md)
skill. It's a plain RFC — the kind of doc a team keeps in a repo — so anyone can import it by
URL with no Confluence/Google auth required.

**Source doc:** [`payment-retry-idempotency-rfc.md`](payment-retry-idempotency-rfc.md)

**Raw URL** (what `/import-url` fetches):

```
https://raw.githubusercontent.com/trustmaster/emos/main/examples/import-demo/payment-retry-idempotency-rfc.md
```

## Try it

From a vault configured like [`examples/demo-vault`](../demo-vault/) (owner `alex`, project
`checkout-reliability`):

```
/weekly-new
/import-url https://raw.githubusercontent.com/trustmaster/emos/main/examples/import-demo/payment-retry-idempotency-rfc.md
```

What you should see:

- The doc is classified as a **design-doc** and proposed for
  `03-projects/checkout-reliability/docs/`.
- Only the **two action items assigned to Alex** (the vault owner) are pulled into the active
  weekly's `## TODO`; Sam's, Priya's, and Dana's are listed as *not pulled*.
- A **review line** is added, linking back to the source URL.
- Nothing is moved until you confirm.

> The RFC's action items are deliberately split across people so the owner-only harvest is
> visible. All names and systems are fictional (the "Payments Platform" demo team).
