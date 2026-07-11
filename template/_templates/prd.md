---
type: prd
title: "Feature / Product Name"
slug: "feature-name"
status: draft            # draft · review · approved · shipped · archived
owner: "{{owner_slug}}"
projects: "parent-project-slug"   # parent project (for humans; lives in that project's docs/)
jira_epic: null          # e.g. PROJ-1234
target_date: null
tags: []
---

## Summary

One paragraph: what we're building and why it matters now. Write this last, read it first.

## Problem & context

The user or business problem, who has it, and the evidence it's real (data, research,
support volume). Why now.

## Goals & non-goals

**Goals**

- What success looks like — outcomes, not features.

**Non-goals**

- Explicitly out of scope for this version, so reviewers don't assume it.

## Users & use cases

Who this is for (personas / segments) and the concrete situations they're in when they reach
for it.

## User stories

- As a **{user}**, I want to **{action}** so that **{outcome}**.
- As a **{user}**, I want to **{action}** so that **{outcome}**.

## Requirements

| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| R1 | Description | P0 | |
| R2 | Description | P1 | |
| R3 | Description | P2 | |

_Priority: P0 = must-have for launch · P1 = important · P2 = nice-to-have._

## UX & design notes

Flows, wireframe links, key states (empty / error / loading), and any interaction constraints.

## Success metrics

| Metric | Baseline | Target | How measured |
|--------|----------|--------|--------------|
|        |          |        |              |

Include a guardrail metric that must **not** regress.

## Rollout & launch

Phasing (internal → beta → GA), flags, dependencies, and the go/no-go criteria.

## Open questions

- [ ] Question needing an answer before build.

## Appendix

Links to research (`09-knowledge/research/`), experiments (`docs/experiments/`), decisions
(`04-decisions/`), and external docs.
