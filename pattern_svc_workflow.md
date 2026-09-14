# Pattern/Svc Workflow

> **TLDR:** Two published crates/repos per domain — `{domain}-pattern` (traits +
> value types + errors + DTOs, zero implementation, zero backend vocabulary) and
> `{domain}-svc` (`core` + `spi/*` + `saf`, every real implementation). Consumers
> depend on both by version. See checklist at end.

## Table of Contents
- [When to Use This, vs SEA's In-Repo Layering](#when-to-use-this-vs-seas-in-repo-layering)
- [Repo Structure](#repo-structure)
- [Single Responsibility: One Domain Per `-pattern` Crate](#single-responsibility-one-domain-per--pattern-crate)
- [Naming Conventions](#naming-conventions)
- [The "Zero Implementation" Rule, Precisely](#the-zero-implementation-rule-precisely)
- [Where Shared Logic Belongs](#where-shared-logic-belongs)
- [`core` vs `spi`: the Technology Boundary Test](#core-vs-spi-the-technology-boundary-test)
- [Config Ownership](#config-ownership)
- [SemVer, Pre-1.0](#semver-pre-10)
- [The path + version Dependency Rule](#the-path--version-dependency-rule)
- [Per-Crate Git Tagging](#per-crate-git-tagging)
- [Compliance Checklist](#compliance-checklist)
- [Anti-Patterns](#anti-patterns)
- [Worked Example](#worked-example)

This is the cross-repo counterpart to [SEA Workflow](sea_workflow.md)'s in-repo
`common/spi/api/core/facade` layering — same vocabulary (`spi`, `core`), different
problem. Distilled from `message-broker-pattern`/`message-broker-svc`'s own build,
including three real corrections made along the way (documented under
[Anti-Patterns](#anti-patterns) below, not sanitized out).

## When to Use This, vs SEA's In-Repo Layering

| | SEA (`sea_workflow.md`) | Pattern/Svc (this doc) |
|---|---|---|
| Scope | Layers within **one** module, one repo | A domain's primitives, split across **two** published repos |
| Consumer | Code elsewhere in the same repo | Any number of *other* repos, by version |
| Layers | `common`/`spi`/`api`/`core`/facade, all siblings | `-pattern` (contract) and `-svc` (`core`+`spi/*`+`saf`), each its own repo |
| Use when | Organizing one module's internals | A domain's contract needs to be reused and versioned independently of any one implementation, by multiple consuming repos |

A `-svc` repo's own internals (`core`, `spi/<tech>-spi`, `saf`) are themselves
organized SEA-style — the two conventions compose, they don't compete.

## Repo Structure

```
{domain}-pattern/                  # published, standalone
└── src/
    ├── traits/                    # MessageBroker, TaskQueue, Validator, ...
    ├── vo/                        # Message, Task, TaskId, ...
    ├── dto/                       # *Request/*Response
    ├── error/                     # BrokerError, QueueError, ...
    └── types/                     # BrokerFuture, marker constants

{domain}-svc/                      # published, standalone
└── main/{domain}/
    ├── core/                      # the technology-free reference implementation
    ├── spi/
    │   ├── {tech-a}-spi/          # wraps exactly one external technology
    │   └── {tech-b}-spi/
    └── saf/                       # construction facade + no-op reference impl

consumer-repo/                     # depends on both by version, defines no
                                    # primitives of its own for this domain
```

## Single Responsibility: One Domain Per `-pattern` Crate

A `-pattern` crate is one bounded domain concept — one reason to change. Two
traits sharing a repo's own history, or sounding topically adjacent, is not the
same thing as sharing a responsibility. Before adding a second trait to an
existing `-pattern` crate (or before splitting one that already has two), run
this test:

> **Do the two traits have different consumers, different delivery/behavioral
> contracts, or different evolution drivers?** If yes to any of these, they are
> two domains, not one — even if they were extracted from the same source repo,
> even if most consumers currently want both.

**Real case study, this org**: `message-broker-pattern` originally bundled
`MessageBroker` (fan-out/broadcast — every subscriber gets every message) with
`TaskQueue` (competing-consumer — each task goes to exactly one worker). They
came from the same source pilot (`edge-message-broker`) and were merged into
one crate specifically so "a consumer gets this domain's whole primitive set
from one crate" — migration-completeness, not SRP, was the reasoning at the
time. Revisited later: `MessageBroker` and `TaskQueue` have genuinely different
evolution drivers (pub/sub concerns — topic wildcards, ordering — vs. queue
concerns — visibility timeout, retry, dead-letter handling) and different
consumers (some want broadcast, some want a work queue, not all want both).
Split into `message-broker-pattern` (`MessageBroker` only) and a new
`task-queue-pattern` (`TaskQueue` only) — and the split goes **all the way
through `-svc` too**: `message-broker-svc-nats-spi` (broker only) and a new
`task-queue-svc-nats-spi` (queue only), not one crate implementing both traits
per backend. Shared history is not shared responsibility, one layer down
either.

**Applied proactively, same org, same day**: "scheduler" is ambiguous across
three distinct domains — an executor/runtime abstraction (which runtime drives
a future — no concept of time), a time-based/cron scheduler (run at/every X),
and a distributed task queue (already `TaskQueue`, above). Rather than build
one `scheduler-pattern` covering all three and needing this same correction
later, they were kept as separate repo pairs from the start:
`executor-pattern`/`executor-svc` (the runtime-selection domain, renamed from
"Scheduler" to "Executor" specifically to stop it from absorbing the
time-based domain's name) and `scheduler-pattern`/`scheduler-svc` (the
time-based domain, freed of that ambiguity). Neither depends on the other's
crate for its own trait — `scheduler-svc`'s implementation may use an
`Executor` internally to run a fired job, but that's an implementation detail
of `-svc`, invisible to `scheduler-pattern`'s own contract.

**The litmus test for a new domain considering whether to bundle two traits**:
would a consumer who genuinely wants only one of them be forced to also
depend on, understand, and keep pace with version bumps to the other? If yes,
for two traits with real behavioral differences, that's two `-pattern` crates,
not a bundle-for-convenience.

## Naming Conventions

- **`{domain}-pattern`** — the contract. Traits, value objects, errors, DTOs.
  Nothing else. Never named `{domain}-contract` if `-pattern` is this org's live
  convention for the repo pair — check a real sibling (`wasm-capability-pattern`)
  before naming a new one from scratch.
- **`{domain}-svc`** — every real implementation. `core` + `spi/*` + `saf`.
- **`core`** — the **zero-external-dependency reference implementation** of the
  domain's trait(s). Not a home for shared helper functions. Verified precedent:
  `runtime-resource-limit-core` ("pure, technology-free logic with no external
  dependency"), `edge-runtime`'s original `runtime-message-broker-core`
  (`InMemoryMessageBroker`/`InMemoryTaskQueue`, "pure, technology-free
  implementation"). If a `core` crate in your domain holds only free functions and
  no reference implementation, it is very likely misnamed — see
  [Anti-Patterns](#anti-patterns).
- **`{domain}-{technology}-spi`** — wraps **exactly one external technology**
  (NATS, Kafka, Postgres, a specific cloud API). An implementation with zero
  external dependencies is not an "spi" under this rule, no matter how it's
  currently filed — it belongs in `core`. There is no such thing as an
  "in-memory spi", a "local-fs spi", or any `*-spi` crate whose `Cargo.toml` names
  no external client library.
- **`saf`** — construction facade (`XFactory` structs, associated functions) plus
  the reference no-op implementation, if the domain has one. Never re-exports a
  concrete `spi`/`core` type — a consumer depending on `-svc-saf` alone cannot name
  `NatsMessageBroker` etc. without also depending on that `spi` crate directly.
- Apply this org's global naming rules on top: types are nouns, functions are
  verbs, reject `*Service`/`*Manager`/`*Handler`/`*Helper`/`*Util` suffixes.

## The "Zero Implementation" Rule, Precisely

`{domain}-pattern` has "zero implementation" — but that phrase is easy to
over-apply. The precise rule, confirmed against real precedent
(`wasm-capability-pattern-contract`'s own hand-written `PartialEq`):

> A contract/pattern crate implements **none of its own primary traits for any
> concrete type**. It is not barred from ever using the `impl` keyword.

Two things this permits, both already used in practice:

1. **Small, structural `impl`s** on the crate's own *value types* — constructors,
   `Display`, a hand-written `PartialEq` — because Rust requires an inherent impl
   to live in the same crate as the type. `Message::new()`, `TaskId::new()`, etc.
2. **Default methods on the crate's own traits**, as long as the method doesn't
   implement that trait (or any other primary trait) for a concrete type. See
   [Where Shared Logic Belongs](#where-shared-logic-belongs) — this is the
   corrected part of the rule; it was under-applied once in real use before being
   checked against precedent.

## Where Shared Logic Belongs

When two or more `-svc`-side implementors need identical logic built on top of a
`-pattern` trait, work through this order — **don't reach for a new shared-helper
crate first**:

1. **Does the logic touch only the trait's own required method(s) and the
   pattern crate's own types (no backend vocabulary)?** If yes: it's a **default
   method on the trait itself**, declared in `-pattern`. This is the
   `Validator::validate_config`/`validator_response` and
   `TaskQueueFactoryContract::new_task_id`/`build_handle` shape — object-safety is
   preserved by adding `where Self: Sized` to any method that needs it (excludes
   it from the vtable without breaking `dyn Trait` usage elsewhere).
2. **Does it need real state, or does Rust's orphan rule block a default method
   here** (e.g. it must implement a *different* trait for many concrete types)?
   Then a small `-svc`-side crate — mirror the local `MessageBrokerFactory`/
   `TaskQueueFactory` shape: a zero-size marker struct with an `impl` block of
   associated functions, never bare free functions in a module.
3. **Is it genuinely specific to one `spi` crate?** Keep it local. Don't
   preemptively generalize before a second real consumer exists.

A `spi/shared` (or `common`/`util`) crate that exists solely to hold trait-adjacent
helper functions is a strong signal you actually wanted step 1 — check it before
building step 2's shape. (This was tried, in real use, before being corrected back
to step 1 — see [Anti-Patterns](#anti-patterns).)

## `core` vs `spi`: the Technology Boundary Test

One question settles it: **does this implementation have a client-library
dependency on one external technology?**

- No external dependency at all → `core` (the reference implementation — every
  domain has at most one).
- Exactly one external technology (a network client, an SDK, a specific wire
  protocol) → `{technology}-spi`.
- More than one external technology in one crate → split it; a single `spi` crate
  wrapping two technologies is a scope violation of the same rule.

Naming something "in-memory spi" or "no-op spi" is a category error: neither wraps
an external technology, so `spi` is the wrong word regardless of where the code
currently lives.

## Config Ownership

- No crate-spanning "which backend" enum or shared config struct, anywhere. Each
  `spi` crate (and `core`, if it needs runtime parameters — most reference
  implementations don't) defines its **own local** config type.
- A contract type in `-pattern` never implements a foreign trait like a
  TOML-section-loader interface itself — that would be real implementation code in
  the wrong repo, and the orphan rule means no other crate could write it either.
  Each `-svc`-side config type implements the pattern crate's own validation trait
  (e.g. `Validator`) **and** whatever local config-loading trait this org's tooling
  requires, independently, in its own crate.
- A config type with zero fields (a backend with no runtime parameters) still
  exists rather than being skipped — the pattern trait's own contract (e.g.
  `MessageBroker::validator()`) still needs a return value, and
  presence/absence of its config section can still carry real, enforced meaning.

## SemVer, Pre-1.0

Both `-pattern` and `-svc` are pre-1.0 (`0.y.z`). Two real, distinct bump sizes are
in active use — verify against your own repo's git history before assuming, don't
just follow this table blindly:

| Change | Bump | Real example |
|---|---|---|
| Breaking: public API removed/reshaped for existing callers | `0.y.z → 0.(y+1).0` | `core`'s content swap (free functions removed, `InMemoryMessageBroker` added) was `0.1.0 → 0.2.0` |
| Additive: new capability, fully backward compatible | `0.y.z → 0.y.(z+1)` | A whole new trait (`TaskQueue`) added to `-pattern` was `0.1.0 → 0.1.1` — additive, even at that scale, bumped patch, not minor |
| Internal-only: dependency swap, no public API change | `0.y.z → 0.y.(z+1)` | An `spi` crate swapping which internal crate provides a trait method, with no signature change for its own consumers |

## The path + version Dependency Rule

Every intra-repo dependency between crates that are each independently published
(e.g. `-saf` depending on `spi/nats-spi`, or `core` depending on `-pattern`) sets
**both** `path` and `version` in `Cargo.toml`:

```toml
{domain}-nats-spi = { path = "../spi/nats-spi", version = "0.1.4" }
```

A `path`-only dependency makes the crate unpublishable (crates.io rejects path
deps with no version). A cross-*repo* dependency (`-svc` depending on
`-pattern`) is version-only, never `git`/`path` — pin to the published version,
bump the floor whenever a new capability you depend on ships.

## Per-Crate Git Tagging

Each independently-published crate gets its own tag series in the shared repo:
`{crate-dir}/v{version}` — e.g. `core/v0.2.1`, `nats-spi/v0.1.4`, `saf/v0.2.2`. Not
one tag per repo release; each crate's own history is independently addressable.

## Compliance Checklist

Mirror this as `docs/3-design/compliance/compliance_checklist.md` in both repos,
one rule per row, each with a real, re-run-and-verify `grep`/`cargo` command — not
an assertion. See `message-broker-svc`'s own checklist for a worked example this
was derived from. Minimum rule set:

- [ ] Every trait in `-pattern` shares the same responsibility with every other
      trait there — different consumers or different evolution drivers means a
      separate `-pattern`/`-svc` repo pair, not a second trait bundled in
      (see [Single Responsibility](#single-responsibility-one-domain-per--pattern-crate))
- [ ] No crate-spanning "which backend" type anywhere (`grep` for the obvious enum
      name returns nothing)
- [ ] `-pattern` implements none of its own primary traits for a concrete type
      (`grep -rn "^impl {Trait} for"` in `-pattern`'s own `src/` returns nothing)
- [ ] `core` names no backend technology and has no external-technology dependency
- [ ] No crate under `spi/` is named for a backend that wraps nothing external
- [ ] No `spi`/`core`/`saf` crate hand-rolls logic that already lives as a default
      method on a `-pattern` trait
- [ ] Every `*Factory` constructor in `saf` returns the same boxed trait-object
      type — never a mix of `impl Trait` and `Box<dyn Trait>` across constructors
      of the same factory
- [ ] `saf`'s own public surface never re-exports a concrete `spi`/`core` type
- [ ] `-svc` has zero dependency on any specific consumer repo
- [ ] Lint gates (`#![deny(unsafe_code)]`, `#![warn(missing_docs)]`, `clippy -D
      warnings`, `fmt --check`) enforced in every crate

## Anti-Patterns

Real corrections made building `message-broker-pattern`/`message-broker-svc`,
kept here specifically because they were real mistakes, not hypothetical ones:

1. **`core` holding shared helper functions instead of the reference
   implementation.** Caught by checking the *real* precedent
   (`runtime-resource-limit-core`, `edge-runtime`'s original
   `runtime-message-broker-core`) rather than assuming. Fix: `core` is always the
   technology-free reference implementation; shared helpers go through
   [Where Shared Logic Belongs](#where-shared-logic-belongs) instead.
2. **Naming a zero-external-dependency implementation `*-spi`.** "SPI" means
   wrapping one external technology; in-memory (or any local-only backend) wraps
   nothing external. Fix: it belongs in `core`.
3. **Building a `spi/shared` crate for logic that was actually common to every
   trait implementor.** First correct move (out of `core`, since `core` isn't a
   helper-function home either) — but not the final one. Once checked against
   `-pattern`'s own "zero implementation" precedent (implementing none of the
   *primary traits*, not "no default method ever"), the logic collapsed into
   default methods on the trait itself, and the whole `spi/shared` crate was
   deleted, not kept as a re-export. Don't stop at "not `core`, so a new shared
   crate" — check whether the trait itself can carry it first.
4. **Free-standing functions instead of a struct+`impl` or a trait method** for
   grouped `-svc`-side logic. This org's constructors already use zero-size
   marker structs (`MessageBrokerFactory`) with associated functions — match that
   shape, or better, check anti-pattern 3 first.
5. **Deprecating instead of deleting** a crate/module once its content moves.
   `inmemory-spi` and `spi/shared` were both deleted outright when their content
   relocated — no compatibility shim, no re-export stub.
6. **Bundling two traits with different reasons to change into one `-pattern`
   crate because they share an origin repo.** `MessageBroker` (fan-out) and
   `TaskQueue` (competing-consumer) were merged into one crate for
   migration-completeness, not because they're one responsibility — see
   [Single Responsibility](#single-responsibility-one-domain-per--pattern-crate)
   above for the real case study and the split that fixed it, all the
   way through `-svc`.

## Worked Example

`message-broker-pattern` + `message-broker-svc` (this org, this repo pair) —
`core::InMemoryMessageBroker`, `spi::{nats,kafka,postgres}-spi`,
`saf::MessageBrokerFactory`. `message-broker-pattern`'s own
`Validator` trait carries `validate_config`/`validator_response` as default
methods — the concrete, reusable instance of the "default method on the trait
itself" rule above. See that repo pair's own `docs/3-design/architecture.md` for
the full reasoning behind each decision recorded here. The SRP split described
above (`TaskQueue` moving to a new `task-queue-pattern`/`task-queue-svc` repo
pair) has been executed — see `message-broker-pattern#2`/`message-broker-svc#4`
(both closed) and the new
[`task-queue-pattern`](https://github.com/sweengineeringlabs/task-queue-pattern)/
[`task-queue-svc`](https://github.com/sweengineeringlabs/task-queue-svc) repo pair.

Prior art for the same split, one domain over: `wasm-capability-pattern` /
`wasm-capability-svc`.

A second worked example, built the same day this SRP section was added:
`executor-pattern`/`executor-svc` (extracted from a real existing
implementation, `edge/scheduler`'s `swe-edge-runtime-scheduler` — see that
repo's own ADR-001 for the extraction and the `Scheduler`→`Executor` rename)
and `scheduler-pattern`/`scheduler-svc` (designed contract-first, no existing
pilot — see that repo's own ADR-001 for the domain-modeling reasoning behind
`Trigger`/`Job`/`JobId` with no prior implementation to extract from). Also
worth noting: `Executor::run<F: Future>` is generic, so `Executor` is not
object-safe (no `dyn Executor`) — `executor-svc-saf`'s `ExecutorFactory`
returns `impl Executor` per constructor instead of the usual
`Box<dyn Trait>` shape. `Scheduler::schedule`/`::cancel` have no generic
parameters, so `Scheduler` *is* object-safe, and `scheduler-svc-saf`'s
`SchedulerFactory` does return `Box<dyn Scheduler>`. Two sibling repos in the
same org, two different, both-correct answers — check your own trait's
object-safety before assuming one shape.
