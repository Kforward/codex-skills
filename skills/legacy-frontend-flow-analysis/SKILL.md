---
name: legacy-frontend-flow-analysis
description: "Analyze complex legacy frontend business flows by tracing from a route, page, component, feature flag, or user journey through router entries, components, mixins/composables, stores, APIs, storage, analytics, navigation, variants, and hidden dependencies. Use when asked to understand a large Vue/React/mobile H5 legacy project, identify the representative implementation of a behavior, compare a variant with the normal flow, document modification points, or produce risk and validation checklists before changing code."
---

# Legacy Frontend Flow Analysis

## Purpose

Trace a legacy frontend feature as a runtime business flow, not just as a file tree. Produce an implementation map that helps later agents modify the feature without missing hidden state, implicit dependencies, or variant-specific behavior.

Keep project-specific route names, event codes, product IDs, and business constants in the target repository's docs. Keep this skill generic.

## When Starting

1. Check `git status` and identify unrelated user changes.
2. Read repository instructions such as `AGENTS.md`, `README.md`, and relevant docs.
3. Confirm the analysis anchor:
   - route path or route name
   - page/component name
   - behavior feature, such as "short-link login" or "payment return"
   - user journey, such as "entry -> form -> login -> payment"
4. State that initial plan before reading broadly.

## Trace Strategy

Use evidence chains instead of name guesses.

1. Locate the entry:
   - route table, route guards, redirects, meta fields, feature flags
   - page/component file and wrapper components
   - backend or remote config keys that choose the variant
2. Trace composition:
   - imports, child components, mixins, composables, hooks, services
   - inherited or indirectly mixed-in modules
   - same-name method overrides and lifecycle hooks
3. Trace state:
   - store modules, global callbacks, module-level variables
   - local/session storage, cookies, URL query, caches
   - login/auth state and route-entry differences
4. Trace side effects:
   - APIs, analytics, event reporting, timers, popups
   - navigation, deep links, app/mini-program/native bridge jumps
   - payment, post-submit, return/restore flows
5. Trace variants:
   - normal flow versus special flow
   - representative implementation versus neighboring copies
   - feature-specific differences versus shared base logic

For Vue 2 mixin-heavy code, do not stop at the `mixins: []` list. Build a cross-call map: who calls whom through `this.*`, which fields are assumed to exist, which lifecycle hooks register global callbacks, and which methods are intentionally overridden.

## Analysis Output

Prefer this structure for the final answer or project doc:

- Entry and scope
- Normal flow
- Target or variant flow
- Composition map
- State and implicit contracts
- API/analytics/navigation side effects
- Shared logic and variant-specific differences
- Modification point locator table
- Risks
- Validation checklist
- Open questions or assumptions

Read `references/analysis-templates.md` when writing a reusable project document or a detailed handoff artifact.

## Evidence Rules

- Cite concrete files and lines when possible.
- Distinguish confirmed facts from inference.
- Use behavior signatures to find a representative implementation: query parameters, config keys, APIs, feature flags, special props, or unique state transitions.
- Run targeted searches with `rg`; for large repositories, search by slices such as router, views, components, mixins, store, API, and libs.
- Verify uniqueness when the user asks for "the one page" or "representative page".

## Risk Lens

Look specifically for:

- implicit `this.xxx` dependencies across mixins/components
- module-level variables that may survive route changes
- global callbacks that hold old component instances
- inconsistent auth or login-state checks
- route-entry differences that change initialization
- cache restore and payment-return behavior
- click handlers that execute during render/config construction
- analytics parameters split across click handlers and shared jump helpers
- old logic modified for new business without compatibility checks

## Documentation Rules

When turning analysis into docs:

- Generalize from representative examples; do not name the durable guide after one page unless it is truly page-specific.
- Put stable workflows in `docs/ai-agent/` or the repository's equivalent.
- Put version, requirement, or feature differences in `docs/change-diffs/` or the repository's equivalent.
- Update indexes, locator tables, risk lists, and validation checklists together.
- Do not modify code unless the user asks for implementation.
