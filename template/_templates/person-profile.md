---
type: person
name: "Full Name"
slug: "firstname"
role: "Title"
level: "IC3"
team: "{{team}}"
start_date: YYYY-MM-DD
contract: permanent
status: active
relation: report        # report | manager | peer | stakeholder | skip
                        # your relationship to this person (from the owner's POV)
manager: "{{owner_slug}}"   # who they report to; keep for relation: report, else clear
# skill_will / growth_areas apply when relation: report (you coach this person).
# Leave blank for manager / peer / stakeholder profiles.
skill_will:
  skill: medium
  will: high
  style: guide
  updated: YYYY-MM-DD
growth_areas: []
strengths: []
links:
  slack: null
  github: null
  linkedin: null
---

<!-- Career Goals / Strengths / Growth Areas are coaching sections — most useful
     for relation: report. For a manager, peer, or stakeholder, keep only the
     sections that fit (e.g. Current Focus, Key Observations). -->

## Current Focus

Primary project or responsibility.

## Career Goals

Where they want to grow, what they're working toward.

## Strengths

Key strengths observed over time.

## Growth Areas

Areas for development with specific examples.

## Key Observations

<!-- Append-only log. Newest entries on top. -->

### YYYY-MM-DD

Observation text.
