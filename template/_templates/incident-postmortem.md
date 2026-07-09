---
type: incident
id: "INC-YYYY-MMDD"
title: "Short Description"
severity: medium
status: detected
date_detected: YYYY-MM-DD
date_started: null
date_resolved: null
time_to_detect_days: null
time_to_resolve_days: null
impact:
  users_affected: null       # accounts / requests / customers affected
  business_impact: null       # revenue, SLA breach, etc. — quantify if known
  scope: null                 # systems / regions / segments affected
owner: "{{owner_slug}}"
opsgenie_link: null
confluence_link: null
projects: []            # project slugs this incident relates to
tags: []
---

## Summary

One-paragraph description of what happened.

## Timeline

| Time | Event |
|------|-------|
| YYYY-MM-DD HH:MM | First signal detected |
| | Mitigation started |
| | Root cause identified |
| | Fix deployed |
| | Incident resolved |

## Root Cause

What caused this incident at its core.

## Impact

- **Users affected**:
- **Duration**:
- **Business impact**:

## Action Items

- [ ] **Immediate**: description (owner: @Person, due: YYYY-MM-DD)
- [ ] **Short-term**: description (owner: @Person, due: YYYY-MM-DD)
- [ ] **Long-term**: description (owner: @Person, due: YYYY-MM-DD)

## Lessons Learned

What we should do differently next time.
