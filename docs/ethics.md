Ethics, Safety, and Human Oversight
-----------------------------------

Scope and Principle
-------------------

This system flags potential influence campaigns and narratives; it does not judge individuals. The goal is to assist analysts in identifying coordinated behavior and risky narratives while respecting privacy and free expression.

Privacy
-------

- Collect only public content. Do not store PII beyond public handles/IDs.
- Support data deletion and retention limits.
- Secure data at rest (database) and in transit (TLS when deployed).

Free Speech and Bias
--------------------

- Classifiers may be biased; provide transparency on model outputs and thresholds.
- Do not automatically remove content; surface risk scores for human review.
- Allow appeals and correction of mislabeled narratives.

Human-in-the-Loop
-----------------

- Analysts review alerts before action.
- Provide explainable factors: toxicity, stance distribution, volume spikes, graph centrality.

Transparency and Auditability
-----------------------------

- Log decisions and model versions.
- Provide clear documentation and intended use.


