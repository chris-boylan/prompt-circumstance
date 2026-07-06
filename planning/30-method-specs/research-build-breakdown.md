# Prompt Injection Dissertation — Research Build Breakdown

Purpose: break the dissertation research into small, practical sections so the project can be built gradually and documented clearly.

---

## How to use this note

- Treat each section as a separate design decision.
- Do not build everything at once.
- For each section, decide:
  - what the section is for
  - what needs to be built
  - what needs to be decided
  - what evidence or output the dissertation needs
- Mark items as done only when they are written down clearly enough to implement.

---

## 1. Research aim

### Goal
Define the project in one clear sentence.

### Final aim
Design and evaluate a unified, researcher-controlled framework for testing prompt injection in LLM-based agents across direct, indirect, and tool-integrated settings, comparing attack transferability, defence effectiveness, and automated evaluation robustness under consistent conditions.

### Problem statement
Current prompt injection evidence is fragmented across static and dynamic benchmarks, isolated attack studies, and defence-specific evaluations, which makes cross-study comparison difficult and weakens claims about what actually works in practice. In particular, there is no widely adopted, unified methodology that tests attack classes and mitigation strategies across direct, indirect, and tool-using agent contexts while also validating the reliability of automated judgement.

### Why agentic settings matter
Agentic systems amplify prompt injection risk because they combine instruction following with memory, external content handling, and tool execution. A failure is therefore not limited to unsafe text output; it can become unsafe action, data leakage, or persistent context corruption. This makes it necessary to evaluate attacks and defences in agent-relevant settings, not only in isolated prompt-only tests.

### What we need to do
- [x] Write a final one-sentence research aim
- [x] Write a 1-paragraph problem statement
- [x] Write a short rationale for why agentic settings matter
- [x] Make sure the aim matches the literature review conclusion

### Output needed
- dissertation-ready aim statement
- short problem statement
- draft for methodology chapter introduction

---

## 2. Research questions

### Goal
Lock the exact questions the implementation must answer.

### Current working questions
1. How well do prompt injection attacks transfer across direct, indirect, and tool-integrated settings?
2. Which defences reduce attack success without excessively degrading useful task performance?
3. How reliable is automated judgement when the judge may itself be vulnerable to manipulation?

### What we need to do
- [ ] Confirm whether these remain the main research questions
- [ ] Decide whether there will be hypotheses or only questions
- [ ] Define what evidence would count as an answer to each question

### Output needed
- final research question set
- optional hypotheses
- mapping from question to experiment

---

## 3. Scope boundaries

### Goal
Prevent the project from becoming too large.

### In scope
- direct prompt injection
- indirect prompt injection
- tool-integrated agent scenarios
- defence comparison
- automated evaluation robustness
- controlled and ethical sandbox testing

### Probably out of scope for core build
- multimodal attacks
- multi-agent worm propagation
- live exploitation of real systems
- enterprise-scale deployment
- very large numbers of models
- long-term memory poisoning unless time permits

### What we need to do
- [ ] Decide the exact attack families in scope
- [ ] Decide whether memory poisoning is core or stretch scope
- [ ] Decide how many models to include
- [ ] Decide whether the dissertation compares models, defences, or both equally

### Output needed
- scope statement for dissertation methods chapter
- “out of scope” paragraph for clarity

---

## 4. Research environments

### Goal
Define the settings in which attacks will be tested.

### Candidate environments

#### A. Direct environment
A simple assistant where the attack is placed directly in the user prompt.

#### B. Indirect environment
An assistant that processes external untrusted content such as markdown, notes, email, or retrieved text.

#### C. Tool-integrated environment
An agent that can choose from a limited toolset inside a sandbox.

### What we need to do
- [ ] Confirm the final list of environments
- [ ] Write a short description of each environment
- [ ] Decide which environment is built first
- [ ] Decide whether all environments use the same base agent logic

### Output needed
- environment definitions
- simple architecture notes per environment
- justification for why these settings were selected

---

## 5. Agent design

### Goal
Define the application under test.

### Core idea
The target should be a researcher-controlled agent application, not a live third-party system.

### Likely components
- system prompt
- task prompt
- optional external content input
- optional tool access
- optional defence middleware
- output and tool-call logging

### What we need to do
- [ ] Decide whether to build one base agent with modes, or separate agents
- [ ] Decide how much orchestration logic should be custom code
- [ ] Define how tool calls are represented
- [ ] Decide whether conversation memory is included

### Output needed
- agent architecture diagram
- description of trust boundaries
- implementation notes for the victim application

---

## 6. Task design

### Goal
Create realistic but controlled tasks that can be scored reliably.

### Likely task categories
- summarization
- extraction
- classification
- instruction following with constraints
- simple retrieval and answer tasks
- tool suggestion or tool invocation tasks

### Good task design rules
Each task should define:
- legitimate goal
- trusted input
- optional untrusted input
- allowed tools
- expected successful behaviour
- malicious failure conditions

### What we need to do
- [ ] Decide the number of task types per environment
- [ ] Write a task schema/template
- [ ] Define benign success criteria for each task
- [ ] Define how many total tasks are needed for a meaningful study

### Output needed
- task template
- task list
- scoring rules per task type

---

## 7. Attack design

### Goal
Select a manageable, defensible set of attack types.

### Candidate attack families
- direct instruction override
- indirect embedded instructions in external content
- tool misuse prompts
- exfiltration attempts
- structured output disruption
- judge-targeting prompts

### What we need to do
- [ ] Choose the final attack families
- [ ] Write attack templates for each family
- [ ] Decide how attacks vary across environments
- [ ] Decide whether to use any external probe source such as `garak`
- [ ] Define attack success conditions per family

### Output needed
- attack taxonomy used in the study
- attack template library
- attack-to-environment mapping

---

## 8. Defence design

### Goal
Define which defences will be compared.

### Candidate defence families
- no defence baseline
- prompt hardening
- trust-boundary marking / spotlighting
- input scanning / classifier-based filtering
- structured output enforcement
- tool permissioning / approval gates
- layered defence

### What we need to do
- [ ] Select a small shortlist of defences
- [ ] Decide which are implemented manually and which may use external libraries
- [ ] Decide how to measure over-defence or false positives
- [ ] Decide whether layered defence is a separate condition

### Output needed
- defence shortlist
- defence descriptions
- per-defence configuration notes

---

## 9. Evaluation design

### Goal
Define how success and failure are measured.

### Primary measures
- attack success rate
- task success rate
- utility retention
- over-defence / false positive rate
- tool misuse rate
- canary leakage rate
- latency / overhead

### What we need to do
- [ ] Define the final metric list
- [ ] Define exact formulas where possible
- [ ] Decide which metrics are primary and which are secondary
- [ ] Define what counts as a successful attack in each environment

### Output needed
- metric definitions
- evaluation rules
- results table templates

---

## 10. Judge robustness section

### Goal
Measure whether automated evaluation can be trusted.

### Core idea
Do not rely only on an LLM to say whether an injection worked.

### Candidate evaluation layers
- deterministic checks
- external judge model
- human validation sample

### What we need to do
- [ ] List all deterministic checks available in the study
- [ ] Decide where LLM-as-judge is actually needed
- [ ] Decide how large the human validation sample should be
- [ ] Decide how to compare judge decisions against stronger ground truth
- [ ] Decide whether to include judge-targeted attack cases explicitly

### Output needed
- judge validation methodology
- agreement analysis plan
- section for threats to validity

---

## 11. Tooling choices

### Goal
Choose the minimum useful software stack.

### Likely core tooling
- Python
- structured schemas for tasks/results
- CSV/JSONL logging
- notebook or script-based analysis

### Candidate research tools
- `garak`
- `PyRIT`
- `promptbench`
- `llm-guard`
- `guardrails-ai`
- local model runners if needed

### What we need to do
- [ ] Decide what must be custom-built
- [ ] Decide what tools are optional versus core
- [ ] Write a tool-selection rationale
- [ ] Check setup complexity and API cost implications

### Output needed
- tooling shortlist
- justification for chosen stack
- dependency plan

---

## 12. Logging and data collection

### Goal
Make every experiment run auditable and reproducible.

### Each run should likely record
- run ID
- environment
- task ID
- attack ID and family
- defence configuration
- model and version
- input/output data
- tool calls
- attack success label
- task success label
- judge label
- latency/cost metadata

### What we need to do
- [ ] Define the run record schema
- [ ] Decide where raw logs are stored
- [ ] Decide how summaries are generated
- [ ] Decide what data must be kept for audit and write-up

### Output needed
- run schema
- logging format
- result folder structure

---

## 13. Experiment matrix

### Goal
Define the combinations that will actually be run.

### Main variables
- environment
- model
- attack family
- defence condition
- task type
- repetition count

### What we need to do
- [ ] Decide number of models
- [ ] Decide number of attacks
- [ ] Decide number of tasks
- [ ] Decide number of defence conditions
- [ ] Estimate total run count
- [ ] Reduce matrix if cost or time is too high

### Output needed
- experiment matrix table
- run-count estimate
- feasibility check

---

## 14. Ethics and safety

### Goal
Keep the study clearly ethical and university-safe.

### Principles
- no attacks on real third-party systems
- no real user data
- no PII
- no live unsafe tool execution
- sandbox-only tools and synthetic secrets

### What we need to do
- [ ] Write a short ethics statement
- [ ] Define the sandbox boundaries
- [ ] Define synthetic test data strategy
- [ ] Note how attack content will be stored safely

### Output needed
- ethics section draft
- risk mitigation note
- possible wording for ethics application

---

## 15. Analysis plan

### Goal
Define how the results will be interpreted.

### Candidate comparisons
- direct vs indirect vs tool-integrated attack success
- baseline vs defended conditions
- defence effectiveness vs utility loss
- deterministic evaluation vs judge agreement
- model-to-model differences if included

### What we need to do
- [ ] Decide which comparisons are the main results
- [ ] Decide whether basic statistical tests are needed
- [ ] Decide what figures and tables the dissertation should include
- [ ] Define how to discuss threats to validity

### Output needed
- analysis plan
- results chapter outline
- chart/table list

---

## 16. Dissertation artefacts

### Goal
Be clear about what the project produces.

### Likely artefacts
- literature review
- research design / methodology chapter
- experiment harness code
- task/attack/defence definitions
- run logs and summary tables
- final analysis and discussion

### What we need to do
- [ ] Decide what code or appendix material will be submitted
- [ ] Decide whether a repository structure is needed now
- [ ] Decide how much technical detail belongs in appendices vs main text

### Output needed
- artefact list
- submission packaging plan

---

## 17. Suggested build order

### Phase 1 — lock the design
- [x] Finalise research aim
- [ ] Finalise scope boundaries
- [ ] Finalise environments
- [ ] Finalise attack shortlist
- [ ] Finalise defence shortlist
- [ ] Finalise metrics

### Phase 2 — build the smallest useful prototype
- [ ] Build one direct prompt environment
- [ ] Add one task type
- [ ] Add one attack family
- [ ] Add baseline evaluation
- [ ] Confirm logging works

### Phase 3 — extend to the full core study
- [ ] Add indirect environment
- [ ] Add tool-integrated environment
- [ ] Add defence conditions
- [ ] Add deterministic evaluation rules
- [ ] Add judge evaluation layer

### Phase 4 — run the study
- [ ] Freeze configs
- [ ] Run experiments
- [ ] Export summary tables
- [ ] Review anomalies
- [ ] Re-run only where justified

### Phase 5 — write up
- [ ] Methods chapter
- [ ] Results chapter
- [ ] Discussion and limitations
- [ ] Conclusion and future work

---

## 18. Immediate next actions

These are the best next slow steps.

### Step 1
Choose and lock:
- [ ] final main research gap
- [ ] final research questions
- [ ] core scope exclusions

### Step 2
Define the first build target:
- [ ] choose the first environment to implement
- [ ] choose one task type
- [ ] choose one attack family
- [ ] choose one baseline metric

### Step 3
Define the comparison structure:
- [ ] decide whether the dissertation is primarily attack-focused, defence-focused, or evaluation-focused
- [ ] decide whether `garak` is baseline, supplementary, or central

### Step 4
Create the first design specs:
- [ ] task schema
- [ ] attack template schema
- [ ] run logging schema

---

## 19. Current recommendation

If the goal is to move slowly and keep scope under control, start with this:

### First implementation slice
- one direct prompt environment
- one simple task type
- two or three direct attacks
- no-defence baseline
- one simple defence
- deterministic success checks

Then extend only after that slice works.

This keeps the project manageable and makes later expansion much easier.

---

## 20. Questions to answer next

1. What is the exact one-sentence aim? **Answer:** Design and evaluate a unified, researcher-controlled framework for testing prompt injection in LLM-based agents across direct, indirect, and tool-integrated settings, comparing attack transferability, defence effectiveness, and automated evaluation robustness under consistent conditions.
2. Which environment should be built first?
3. Is the project mainly comparing attacks, defences, or evaluation methods?
4. Is `garak` a core component or a supplementary benchmark?
5. What is the minimum viable experiment that still answers the dissertation question?
