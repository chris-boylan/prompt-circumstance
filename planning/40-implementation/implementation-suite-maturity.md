# Prompt Injection Dissertation — Test Suite Maturity Plan

Purpose: prioritize full harness development before dissertation writing by hardening experiment control, coverage, and reproducibility.

---

## 1. Current phase objective

Move from "working prototype" to "research-grade test suite" with stable experiment orchestration, richer indirect realism, and stronger defence/evaluation coverage.

---

## 2. Phase priorities (in order)

1. **Experiment control**
   - add repeat-run support (`n_repeats`)
   - emit run manifests for each experiment batch
   - standardize output naming and metadata for repeated runs

2. **Automated aggregation**
   - add script/command to compute matrix summaries
   - report core rates: `task_success`, `attack_success`, `contains_canary`
   - emit machine-readable summary artifact

3. **Indirect realism expansion**
   - add `carrier_type` dimension (email, markdown, kb snippet, note)
   - ensure attacks are bound to explicit untrusted carriers
   - preserve trust-boundary markers in prompt assembly

4. **Defence expansion**
   - keep prompt hardening as baseline defence
   - add one stronger indirect defence:
     - boundary spotlighting / untrusted content isolation
     - optional structured output enforcement

5. **Evaluation robustness**
   - normalize failure taxonomy across environments
   - add consistency checks across repeats
   - ensure schema/log fields remain backward-compatible unless versioned

6. **Quality gates**
   - extend smoke and regression tests for matrix routes
   - add tests for repeat aggregation and manifest integrity

---

## 3. Deliverables for this phase

- repeatable experiment runner behavior
- reproducible run manifests
- cross-run aggregation utility
- indirect carrier-aware task/attack coverage
- at least one additional non-prompt-only defence condition
- expanded test suite for orchestration and metric integrity

---

## 4. Exit criteria

- all matrix paths execute via config without manual patching
- repeated runs produce deterministic, auditable artifacts
- aggregation output is consistent across providers/environments
- indirect attacks are tagged by carrier type
- test coverage protects core runner, logging, and scoring flows

