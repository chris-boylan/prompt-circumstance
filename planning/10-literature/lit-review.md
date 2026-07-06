Evaluation of current threat vectors posed by prompt injection against contemporary Large Language Models (LLMs), while considering damage of attacks, and effective mitigation strategies.



Introduction

This section reviews relevant research on prompt injection, outlining the nature of the threat, the vulnerabilities it exposes, and the principal attack and defence methods discussed in the literature. It draws on recent studies from both attack and defence-oriented perspectives and highlights gaps that help frame and support the research questions.



Context

This research focuses on prompt injection against AI agents, so it is important to establish a clear understanding of what agents are and why this threat matters. Russell and Norvig, in Artificial Intelligence: A Modern Approach, describe them as:

An intelligent agent is "an agent that acts appropriately for its circumstances and its goals, is flexible to changing environments and goals, learns from experience, and makes appropriate choices given its perceptual and computational limitations." ​[1]​

Considering this definition of an intelligent agent, to supplement a cybersecurity perspective from the Open Worldwide Application Security Project (OWASP), their Top 10 for LLM Apps paper allows the decomposition of core capabilities of agentic systems into the following categories:

Planning and reasoning

Reflection

Chain of Thought

Sub-goal decomposition

Memory or Statefulness

Actions and tool use

OWASP categorises several threats against LLMs and Gen AI app and ranks Prompt Injection as number one in 2025, categorised as LLM01:2025. They define it as the manipulation of LLMs via crafted inputs which can lead to unauthorised access, data breaches, and compromised decision-making.

Of the other threats represented in the Top Ten list, Prompt Injection can also be viewed as an upstream cause of other issues including, sensitive information disclosure, excessive agency and insecure output handling. ​[2]​

Prompt injection has been observed in research and attacks but the first zero-click prompt injection exploit known as “EchoLeak”, categorised as CVE-2025-32711 was discovered in early 2025. Reddy and Gujral detailed the exploit where it allowed for remote unauthenticated exfiltration accomplished via an email which targeted Microsoft Copilot. This bypassed controls including XPIA classifier, external-link redaction, and CSP. ​[3]​

Gartner ​[4]​ in May 2025 estimated 33% of enterprise software applications will use agentic AI by 2028. Differing views have emerged regarding the credibility of the hype surrounding agentic AI, with industry commentary showingboth strong interest in its potential, but also uncertainty about its practical implementation in enterprise settings. ​[4]​

Updated 2026 figures from Gartner suggest that only 17% of organizations have deployed AI agents, with 42% expecting to deploy within the next 12 months, while 22% aim to do so next year. They also predict that over 40% of Agentic AI projects will be cancelled by the end of 2027. This is attributed to escalating costs, unclear business value, or inadequate risk controls. ​[4]​

Ignoring market speculation, the fact remains that Prompt Injection exists as a creditable vulnerability. Organisations should understand the damage this system this poses to set their risk appetite from both a security and a governance perspective. ​[5]​



Threat landscape (Attack methods)

There are several taxonomies proposed for prompt injection attacks, some becoming quite granular in their specificity. With consideration on the delivery vector, categorisation can be immediately split into two different categories, direct and indirect. The security goal with these attacks can be described as what to execute, ignore, override, or change during the processing of the prompt. ​[6]​

Direct

Direct prompt injections is where a user’s prompt affects the behaviour of a model in unexpected ways via devising crafted instructions to generate out-of-distribution (OOD) output. It is called direct prompt injection because the attack is placed directly in the users prompt instructing the LLM to deviate from its instruction set to achieve the security goal.

Indirect

Indirect prompt injection is where input is accepted from external data sources which can include files, documents, websites and emails. As the instructions are not directly placed in the users prompt to the LLM, this method of delivery is considered indirect.



McHugh, Šekrst and Cefalu, employees of Preamble Inc., the company who first discovered and disclosed prompt injection in 2022 ​[7]​, categorise direct and indirect prompt injection as a delivery vector. They supplement the taxonomy further by adding dimensions they describe as attack modularity and propagation behaviour.

Attack modularity

Attack Modularity is the format of the payload used for a prompt injection attack and can take the following forms:

Multimodal

Media (Image, audio and video)

Cross-modal translations

Code injection

Code generation manipulation

Template and configuration injection

Hybrid threats

XSS-enhanced prompt injection

CSRF-amplified attacks

SQL Injection via prompts



Propagation behaviour

Propagation behaviour is how an attack persists or spreads throughout a system or network and can be categorised in the following terms:

Recursive injection

Autonomous propagation

Multi-agent infection

AI Worms



These can be linked to threat definitions from OWASP ​[8]​ due to alignment with agent or goal hijacking and context/memory-based attacks:

T2 Tool Misuse

T6 Intent Breaking & Goal Manipulation

T1 Memory Poisoning

T12 Agent Communication Poisoning

T13 Rogue Agents



Impact and risk

Rehberger details how prompt injection compromises all aspects of the CIA Triad (Confidentiality, Integrity and Availability) with several examples. For Confidentiality a simple example was outlined where the invocation of tools sent data to a 3rd party server, in this case the Zapier Plugin where an attacker was able to steal a user's email address. Integrity can be affected in the example of “Terminal DiLLMa”. In this exploit ANSI Escape Codes output by an LLM can perform prompt injection to hijack user terminals. While Availability was shown to be compromised with ChatGPT’s Persistent Output Refusal, with it an attacker was able add fake memories to the LLMs long term memories to refuse any further answers. ​[9]​

Gulyamov et. al. add colour to these types of attack by expanding on example use cases in how they can be utilised. They detail attacks over direct, indirect and tool-based categories and show how hidden instructions in markdown and Unicode can bypass human visual inspection as methods of obfuscation.​ [10]​

An example of a major incident which is categorised as CVE-2025-53773: GitHub Copilot Chat in VS Code Arbitrary Code Execution show how these elements can be combined in a production system where attackers “could exploit the AI agent's contextual interpretation by embedding malicious instructions in innocuous files—such as README.md, source code comments, or evenGitHub issues—to trick Copilot into first modifying the project's .vscode/settings.json configuration with the line "chat.tools.autoApprove": true, thereby disabling all user confirmations for tool invocations. Once activated, this allowed Remote Code Execution (RCE).” ​[11]​

Recommendations from this risk analysis recommend threat modelling, data flow analysis, as penetration testing and red teaming. ​[9]​



Mitigation Strategies (Existing defences)

OWASP ​[12]​ list several prevention and mitigations strategies against prompt injection:

Constrain Model behaviour

Define and validate expected output formats

Implement input and output filtering

Enforce privilege control and least privilege access

Require human approval for high-risk actions

Segregate and identify external content

Conduct adversarial testing and attack simulations

Barcha Correia et al. propose in their literature review on LLM Defenses an extension to terms first defined in a NIST report on adversarial machine learning (AML). In it they define a taxonomy for intervention types:

Training time

Deployment time

Indirect mitigations

Mitigations against indirect prompt injection

Evaluation time interventions

Training time interventions focus on learning from vast collections of data. Deployment time interventions are at the system level rather than the model level. Indirect mitigations work on the assumption that model may produce harmful output and attempts to minimise any impact. Mitigations against indirect prompt injection can include separating data from trusted and untrusted sources and filtering embedded instructions. Evaluation time is where the models vulnerabilities are assessed to direct which safeguards should be implemented. ​[13]​

Schulhoff et. al argue that “Due to their simplicity, prompt based defense are an increasingly well studied solution to prompt injection (Xie et al., 2023; Schulhoff, 2022) How-ever, a significant takeaway from this competition is that prompt based defenses do not work. Even evaluating the output of one model with another is not foolproof.” ​[14]​



Previous studies using test suites

There are many previous studies touching on various aspects of prompt injection, items for consideration include the following test suites.

CAPTURE

This is Context-Aware Prompt Injection Testing and Robustness Enhancement (CAPTURE), a context-aware prompt injection benchmarking framework for prompt guardrail models. It tests prompt injection detection and over-defence, focusing on how well guardrails handle both malicious and benign inputs.

Agent Dojo

A dynamic benchmarking environment for evaluating prompt injection attacks and defences in realistic LLM agent tasks such as workspace, banking, travel, and Slack scenarios.

BIPIA

A benchmark for indirect prompt injection in LLMs that showed models were broadly vulnerable and proposed “boundary awareness” and “explicit reminder” as defences with results showing strong mitigation with preserved output quality.

InjecAgent

A benchmark for tool-integrated LLM agents that measures how vulnerable agents are to indirect prompt injection attacks through external content. It evaluated 30 LLM agents and was designed as a standard for testing resilience to indirect prompt injection attacks.

ASB

An agent security benchmark that evaluates attacks and defences across multiple stages of LLM-based agents, including prompts, tools, and memory.

PALIT

A benchmark dataset for evaluating LLM safety tools on malicious and benign prompts, with attention to precision, recall, false positives, and latency using Garak and other sources to build a benchmark dataset for malicious and benign prompts and compares security solutions on precision, recall, false positives, and latency.

Using the details from the studies examined, a matrix has been devised to attempt to highlight areas where there is room for development.

Paper

Attack focus

Defence focus

Setting

Judge

Main gap

BIPIA

Indirect PI

Boundary awareness, explicit reminder

Static benchmark

Human and eval metrics

Limited agent realism

AgentDojo

Direct & Indirect PI

Multiple defences

Dynamic agent tasks

LLM-assisted

Harder to compare with static benchmarks

InjecAgent

Indirect PI

Limited

Tool-integrated agents

Human / metrics

Weak defence comparison

ASB

Multiple PI types

Multiple defences

Agent security framework

Mixed

Broad but fragmented evidence

CAPTURE

Context-aware PI

Guardrail robustness

Static/context-aware

LLM + human

Not a full agent benchmark

PALIT

Malicious/benign prompts

Safety tools

Tool evaluation

Metrics-based

Not a full end-to-end agent study



Conclusion

Prior studies have established prompt injection taxonomies and demonstrated individual attacks and defences, but fewer works compare attack classes and mitigation strategies under a unified test suite while also accounting for evaluation robustness. This leaves open the question of how well defences generalise across direct and indirect injections, and how reliable automated judge-based assessment remains under adversarial conditions.

The studies examined so far show that the field already has useful benchmarks for direct and indirect prompt injection, but the evidence is fragmented. Some papers focus on attack generation, others on defences, and only a few connect those to dynamic tool-using or robust evaluation with an LLM-as-judge. The next step would be to position my research around several linked questions.

How well do existing attacks transfer across direct, indirect, and tool-integrated settings?

Which defences reduce attack success without damaging useful task performance?

How reliable is automated judgement when the judge itself may be vulnerable to manipulation?

This framing aims to target the research gap because recent work still highlights problems with static benchmarks, over-defence, and the lack of context-dependent evaluation.

This dissertation can extend prior work by developing a unified prompt-injection evaluation framework that tests direct and indirect attacks, compares defences under consistent conditions, and incorporates LLM-based judgement with validation checks to address known weaknesses in automated evaluation.





​​Bibliography

​​

​[1]

​R. J. Stuart and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed., Hoboken: Prentice Hall, 2020, p. 34.

​[2]

​OWASP, “OWASP Top 10 for Large Language Model Applications,” 2026. [Online]. Available: https://owasp.org/www-project-top-10-for-large-language-model-applications/.

​[3]

​P. Reddy and A. S. Gujral, “EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System,” Proceedings of the AAAI Symposium Series, 2025.

​[4]

​R. Sheinberg, “Xpander,” 12 April 2026. [Online]. Available: https://xpander.ai/blog/gartner-hype-cycle-for-agentic-ai-what-it-means-for-ai-agent-development-platforms. [Accessed 3 June 2026].

​[5]

​Sotiropoulos John, Rosario Ron F. Del, Kokuykin Evgeniy, Oakley Helen, Habler Idan, et al.., “OWASP Top 10 for LLM Apps & Gen AI Agentic Security Initiative,” OWASP, 2025.

​[6]

​I. Naik, N. Naik and D. Naik, “Threat Landscape of Adversarial Attacks on Generative AI and Large Language Models (LLMs): Exploring Diﬀerent Types of Adversarial Attacks, Associated Risks, and Mitigation Strategies,” https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.176539611.16370746/v1, 2025.

​[7]

​Preamble Inc., “Declassifying the Responsible Disclosure of the Prompt Injection Attack Vulnerability of GPT-3,” 2022. [Online]. Available: https://www.preamble.com/prompt-injection-a-critical-vulnerability-in-the-gpt-3-transformer-and-how-we-can-begin-to-solve-it?utm_source=perplexity. [Accessed 8 Jun 2026].

​[8]

​J. McHugh, K. Šekrst and J. Cefalu, “Prompt Injection 2.0: Hybrid AI Threats,” 2025.

​[9]

​J. Rehberger, “Trust No AI: Prompt Injection Along The CIA Security Triad,” https://arxiv.org/pdf/2412.06090?, 2024.

​[10]

​S. Gulyamov, S. Gulyamov, A. Rodionov, R. Khursanov, K. Mekhmonov, D. Babaev and A. Rakhimjonov, “Prompt Injection Attacks in Large Language Models and AI Agent Systems: A Comprehensive Review of Vulnerabilities, Attack Vectors, and Defense Mechanisms,” MDPI, Tashkent, 2026.

​[11]

​K. I. Eduardovich, “ADVERSARIAL THREAT VECTORS IN AI-AUGMENTED SOFTWARE DEVELOPMENT: PROMPT INJECTION, DATA POISONING, AND EXPLOITATION RISKS,” https://scientific-publication.com/images/PDF/2025/75/dversarial-threat-vectors.pdf, 2025.

​[12]

​OWASP, “LLM01:2025 Prompt Injection,” 2025. [Online]. Available: https://genai.owasp.org/llmrisk/llm01-prompt-injection/. [Accessed 9 Jun 2026].

​[13]

​P. H. B. Correiaa, R. W. Achjiana, D. E. G. C. d. Oliveirac, Y. A. Mariaa, V. T. Hayashia, M. Lopesb, C. C. Miersc and M. A. S. Jr, “A Systematic Literature Review on LLM Defenses Against Prompt Injection and Jailbreaking: Expanding NIST Taxonomy,” https://arxiv.org/pdf/2601.22240, São Paulo, 2026.

​[14]

​“Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of LLMs through a Global Scale Prompt Hacking Competition,” 2024.

​[15]

​Shi, Jiawen; Yuan, Zenghui; et. al., “Optimization-based Prompt Injection Attack to LLM-as-a-Judge,” CCS, Salt Lake City, 2024.

￼

 

 

 