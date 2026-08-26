# Ethics and Governance

## Data handling

- Task corpora are synthetic.
- Ticket and customer identifiers in fixtures are synthetic.
- No production systems or real user data are accessed by default harness runs.

## Safety and misuse posture

- Attack templates are used only for controlled defensive evaluation.
- Tool-integrated runs enforce least-privilege tool allowlists.
- High-risk tool calls are routed to approval-required state in layered defence cells.

## Disclosure posture

- Any novel harmful model behavior discovered during evaluation should be disclosed responsibly to relevant providers before public release.

## Fairness and scope

- Matrix includes open/local and hosted model backends to reduce single-vendor bias.
- Conclusions are bounded to tested domains (support-ticket style tasks) and documented as such.

## Reproducibility and transparency

- Protocol, matrix config, tasks, and attack templates are frozen in `reproducibility/`.
- Results are generated from scripts in-repo and retained as raw + aggregated artifacts.

