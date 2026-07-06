# Literature Review Feedback Notes

Feedback on [`lit-review.md`](lit-review.md)

## Overall verdict

This is a promising draft. It already has the core ingredients of a solid literature review:

- a clear topic
- a sensible section structure
- relevant recent sources
- a visible research gap
- a set of research questions that follow logically from the review

The main thing holding it back is that it still reads a bit more like a well-informed survey of sources than a critical literature review. In other words: there is good coverage, but it needs more synthesis, comparison, and evaluation.

---

## What is already working well

### 1. The structure is sensible
The sequence works well:

- Introduction
- Context
- Threat landscape
- Impact and risk
- Mitigation strategies
- Previous studies using test suites
- Conclusion

This is a strong backbone for the chapter.

### 2. The topic is clearly motivated
The opening context around OWASP, agentic systems, and real-world incidents like EchoLeak gives the reader a good reason to care about prompt injection.

### 3. There is a real research gap emerging
The conclusion is the strongest part conceptually. These questions are good:

- How well attacks transfer across direct, indirect, and tool-integrated settings
- Which defences reduce attack success without harming task performance
- How reliable automated judgement is under adversarial conditions

This is a credible dissertation angle.

### 4. The benchmark section is useful
The comparison of `BIPIA`, `Agent Dojo`, `InjecAgent`, `ASB`, `CAPTURE`, and `PALIT` is one of the most valuable parts of the draft because it begins to synthesize literature rather than just summarize it.

---

## Biggest issue: more synthesis is needed

Right now, many paragraphs follow this pattern:

- Source A says X
- Source B says Y
- Source C says Z

That is useful, but a literature review usually needs one more step:

- What do these sources collectively show?
- Where do they agree?
- Where do they differ?
- What remains uncertain?
- Why does that matter for this dissertation?

### Example
In the attack taxonomy section, the review describes:

- direct vs indirect prompt injection
- modularity
- propagation behaviour
- OWASP threat mappings

That is good descriptive coverage. It would be stronger if it explicitly said:

- whether these taxonomies are complementary or competing
- which taxonomy is most useful for evaluating agentic systems
- whether some schemes are too broad for experimental benchmarking
- which dimensions matter most for this dissertation design

That analytical move would make the review feel more scholarly.

---

## Highest-priority improvements

## 1. Make the chapter more argumentative
The review should not just show that literature exists; it should show what the literature establishes, where it is weak, and why this study is needed.

A stronger pattern for each section is:

1. State the theme
2. Summarize the key literature
3. Compare positions
4. Evaluate limitations
5. Link back to the study

This happens best in the conclusion, but it should happen earlier and more often.

### Good places to add analysis
- after the direct/indirect taxonomy discussion
- after the mitigation taxonomy discussion
- after the benchmark comparison section

---

## 2. Tighten the academic tone
Some phrases sound informal, imprecise, or rhetorical for a dissertation.

### Examples
- “add colour” → too conversational
- “Ignoring market speculation” → sounds dismissive
- “the fact remains” → too rhetorical
- “creditable vulnerability” → should likely be “credible vulnerability”
- “showingboth” → typo

### Better example
Current:
> Ignoring market speculation, the fact remains that Prompt Injection exists as a creditable vulnerability.

Better:
> Regardless of uncertainty surrounding the pace of agentic AI adoption, prompt injection is now established as a credible security vulnerability in LLM-based systems.

---

## 3. Improve citation quality and consistency
This is a major academic issue.

Some sources are strong:

- OWASP
- Russell and Norvig
- conference or arXiv papers
- benchmark papers

Some references look weaker or need justification:

- a vendor blog used to report Gartner claims
- possible secondary reporting instead of primary Gartner material
- the source used for the Copilot incident may not be the best authority for that claim

### Recommendation
Where possible, prefer:

- the primary source
- a peer-reviewed paper
- an official advisory
- a first-party technical disclosure

For example:

- if citing Gartner statistics, use Gartner directly if available
- if discussing CVEs, use the official CVE/NVD or vendor advisory where possible
- if discussing benchmark frameworks, cite the original paper

---

## 4. Convert the benchmark comparison into a real table
The matrix is conceptually useful, but the current formatting is hard to read because it is written as vertical text rather than an actual table.

### Suggested format

| Paper      | Attack focus            | Defence focus                         | Setting                  | Judge         | Main gap                          |
|------------|-------------------------|----------------------------------------|--------------------------|---------------|-----------------------------------|
| BIPIA      | Indirect PI             | Boundary awareness, explicit reminder | Static benchmark         | Human/metrics | Limited agent realism             |
| AgentDojo  | Direct & indirect PI    | Multiple defences                     | Dynamic agent tasks      | LLM-assisted  | Harder to compare with static     |
| InjecAgent | Indirect PI             | Limited                               | Tool-integrated agents   | Human/metrics | Weak defence comparison           |
| ASB        | Multiple PI types       | Multiple defences                     | Agent security framework | Mixed         | Broad but fragmented evidence     |
| CAPTURE    | Context-aware PI        | Guardrail robustness                  | Static/context-aware     | LLM + human   | Not a full agent benchmark        |
| PALIT      | Malicious/benign prompts| Safety tools                          | Tool evaluation          | Metrics-based | Not a full end-to-end agent study |

This one change would improve readability significantly.

---

## 5. Bring the LLM-as-judge literature into the main body earlier
The conclusion raises a strong question about judge reliability, but the main body does not fully build toward it.

Reference `[15]` is relevant here:

- Shi et al., “Optimization-based Prompt Injection Attack to LLM-as-a-Judge”

### Why this matters
If part of the dissertation contribution involves automated evaluation, then the review should explicitly discuss:

- why LLM-as-judge is attractive
- how it can be manipulated
- what prior work says about adversarial evaluation failure
- why validation checks are needed

That would make the conclusion feel much more earned.

---

## Section-by-section comments

## Introduction
This is fine, but it could be sharper.

It would help to make the contribution of the chapter more explicit, for example:

- what themes it covers
- how those themes lead to the research gap
- what criteria are being used to compare studies

At present it is competent but somewhat generic.

---

## Context
This section is useful, but two improvements would help.

### A. Clarify the “agent” framing
Russell and Norvig are used to define agents, then the discussion pivots to OWASP’s decomposition of agentic capabilities. That works, but the transition could be clearer.

It may help to state explicitly that, for the purposes of this dissertation, agentic AI systems are operationalized in terms of:

- planning/reasoning
- memory/state
- tool use
- goal decomposition
- reflection

That would make it clear this is a working definition rather than just a list of features.

### B. Be careful with hype/adoption material
The Gartner discussion adds context, but it may not need as much space unless it directly supports the research rationale. At the moment it feels somewhat tangential.

If kept, it should be brief and analytical:

- growing adoption increases exposure
- uneven governance increases risk
- therefore robust evaluation is needed

---

## Threat landscape
This is a solid section, but currently too list-heavy.

### What works
- direct vs indirect distinction
- extension to modularity and propagation
- OWASP mapping

### What to improve
Explain why these taxonomies matter for the dissertation design.

For example:

- direct/indirect is useful for input-origin comparison
- modularity matters for attack realism
- propagation matters more in multi-agent or memory-enabled systems
- OWASP mappings help align technical testing with security governance

That turns taxonomy summary into literature review analysis.

---

## Impact and risk
This section is strong in topic choice but could be more analytical.

### Good point
Using the CIA triad is a smart organizing frame.

### Suggested improvement
Rather than just listing confidentiality, integrity, and availability examples, explicitly argue that prompt injection is not merely a content safety problem but a system security problem affecting:

- data confidentiality
- action integrity
- service availability

That is an important conceptual point.

The Copilot example is strong, but the source should be checked to ensure it is the best one to rely on.

---

## Mitigation strategies
This section needs more critical analysis.

Right now it mostly lists defences and taxonomy categories. The reader will want to know:

- Which mitigation classes appear promising?
- Which are weak?
- Which generalize well to agentic systems?

A clearer structure might be:

- prompt-level / instruction-level
- model-level
- application / system-level
- tool-use / permissioning controls
- detection / guardrail controls
- evaluation / red-teaming controls

Likely underlying argument:

- prompt-only defences are insufficient
- system-level controls matter most in tool-using agents
- evaluation must test both attack success and over-defence

That argument is good; it just needs to be stated more directly.

---

## Previous studies using test suites
This is one of the strongest sections.

### What works
- concrete benchmarks
- clear scope descriptions
- visible attempt at comparison
- natural bridge to the research gap

### What to improve
Two main things:

1. Turn the matrix into a real table
2. Add one or two synthesis paragraphs after the comparison

Possible synthesis points:

- static benchmarks enable comparability but reduce realism
- dynamic agent benchmarks improve realism but complicate controlled comparison
- defence evaluation remains inconsistent across studies
- judge robustness is underdeveloped across the benchmark landscape

That would significantly strengthen the section.

---

## Conclusion
This is probably the strongest section in the draft.

The research questions are coherent and dissertation-worthy.

### One suggestion
The final paragraph is good, but the methodological contribution could be made slightly more explicit:

- unified test suite
- direct and indirect attacks
- defence comparison under common metrics
- LLM judge with robustness checks
- measurement of both attack success and utility degradation

That would connect the literature gap more tightly to the proposed study.

---

## Line-level issues to fix

### Language and grammar
- Opening line reads more like a working title than a polished chapter title
- “Gen AI app” → likely “GenAI applications” or “LLM applications”
- “showingboth” → typo
- “creditable vulnerability” → should likely be “credible vulnerability”
- “the damage this system this poses” → duplicated wording
- “Direct prompt injections is” → grammar error
- “users prompt” → should be “user’s prompt”
- “Attack Modularity” capitalization is inconsistent
- “3rd party” → use “third-party”
- “was able add” → missing “to”
- “et. al.” → should be `et al.`
- “show” → should be “shows”
- “evenGitHub” → missing space
- “Recommendations from this risk analysis recommend” → repetitive
- “OWASP list” → should be “OWASP lists”
- “mitigations strategies” → should be “mitigation strategies”
- “assumption that model may produce” → should be “assumption that the model may produce”

### Referencing and consistency
- Bibliography `[1]`: `R. J. Stuart` is almost certainly wrong; should be `S. J. Russell` and `P. Norvig`
- Bibliography style is inconsistent across entries
- `[15]` appears in the bibliography but is not integrated into the main body
- `[14]` appears incomplete as written

---

## Bibliography cleanup tasks

The bibliography needs a dedicated cleanup pass.

### Problems visible now
- inconsistent author formatting
- inconsistent capitalization of titles
- inconsistent use of URLs
- some entries lack venue details
- mixed source types without consistent formatting
- incomplete or weakly documented entries

### Recommendation
Pick one citation style and normalize everything:

- Harvard
- IEEE
- APA
- or the department’s required style

Using a reference manager would help avoid inconsistencies.

---

## Top five priorities for the next draft

1. Convert descriptive summaries into comparative analysis
2. Turn the benchmark matrix into a proper table
3. Strengthen the LLM-as-judge discussion using `[15]`
4. Replace weak or secondary sources where possible with primary sources
5. Do a full language and citation consistency pass

---

## Possible framing sentence for the literature review

> Existing prompt-injection research has established diverse attack taxonomies and a growing set of defences, but evidence remains fragmented across static and dynamic benchmarks, especially for tool-using agents and automated evaluation pipelines. This creates a need for a unified framework that compares attack classes and mitigation strategies under consistent conditions while also testing the robustness of LLM-based judgement itself.

---

## Bottom line

This is good enough to build on, but not yet polished enough as a final literature review chapter. The biggest upgrade is not necessarily adding more sources, but doing more with the sources already included:

- compare them
- evaluate them
- show disagreement and limitations
- tie them directly to the research design

That will move the chapter from descriptive summary toward a stronger critical literature review.

