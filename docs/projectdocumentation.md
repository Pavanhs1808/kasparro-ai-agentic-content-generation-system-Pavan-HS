Kasparro – Agentic Content Generation System

Problem Statement
Design and implement a modular, agentic automation system that ingests a small product dataset and automatically generates structured, machine‑readable content pages (FAQ, Product Description, Comparison). The system must demonstrate:
- Clear agent boundaries (single responsibility, explicit input/output, no hidden globals)
- Dynamic agent interaction via an orchestration mechanism
- Reusable content logic blocks
- Template‑based generation
- Clean, deterministic JSON outputs

Solution Overview
- Input: A minimal JSON-like product record (name, concentration, skin type, ingredients, benefits, usage, side effects, price).
- Core Abstractions:
  - Message + EventBus: a synchronous pub/sub message bus that coordinates autonomous agents.
  - Agents: stateless components that react to subscribed message types and emit new messages.
  - Templates: strongly‑typed JSON renderers for FAQ, Product Page, and Comparison Page.
  - Content Logic Blocks: reusable functions for formatting and comparisons.
- Outputs: faq.json, product_page.json, comparison_page.json, and all_questions.json.

Scopes & Assumptions
- Only the provided product facts are used. When data is absent, the system emits “Not specified.”
- Comparison uses a deterministic fictional Product B with defined structure (name, ingredients, benefits, price).
- No external network calls; pure Python execution with filesystem I/O.
- UTF‑8 JSON output (ensure_ascii=False). Consumers should read with UTF‑8.

System Design
1) Data Models (src/models.py)
- Product: normalized fields (lists for ingredients/benefits/skin types, etc.).
- Question: category, text, answer.
- FAQPage, ProductPage, ComparisonPage: structured page objects passed to templates.

2) Reusable Content Logic Blocks (src/blocks)
- transform.py: list joining, bullet formatting, price formatting, list comparisons, comparison summary construction.
- questions.py: question generation rules and grounded answering (never invents facts; defaults to “Not specified.” when missing).

3) Template Engine (src/templates)
- FAQTemplate: defines schema and renders an FAQ page to JSON.
- ProductTemplate: defines schema and renders a product description page with normalized fields and human-readable sections.
- ComparisonTemplate: defines schema and renders a two‑product comparison with per‑field results and a summary.

4) Agent Core (src/agent_core.py)
- Message: { type: str, payload: dict } envelope.
- Agent protocol: on_message(msg, publish) — stateless processing with explicit publish callback.
- EventBus: synchronous pub/sub; maintains subscriber lists by message type and a FIFO queue of messages.

5) Agents and Responsibilities (src/agents)
- Worker Nodes (wrap business capabilities):
  - ParseAgentNode: subscribes RAW_INPUT → emits PRODUCT_PARSED
  - QuestionAgentNode: subscribes PRODUCT_PARSED → emits QUESTIONS_ANSWERED and FAQ_PAGE_READY
  - ProductPageAgentNode: subscribes PRODUCT_PARSED → emits PRODUCT_PAGE_READY
  - ComparisonAgentNode: subscribes PRODUCT_PARSED → emits COMPARISON_PAGE_READY
- Render Agents (template application):
  - FAQRenderAgent: subscribes FAQ_PAGE_READY → emits FAQ_JSON
  - ProductRenderAgent: subscribes PRODUCT_PAGE_READY → emits PRODUCT_JSON
  - ComparisonRenderAgent: subscribes COMPARISON_PAGE_READY → emits COMPARISON_JSON
- Aggregation:
  - OutputCollectorAgent: subscribes FAQ_JSON, PRODUCT_JSON, COMPARISON_JSON, QUESTIONS_ANSWERED → emits ALL_OUTPUTS_READY once all parts are present.

6) Orchestration Graph (src/orchestrator.py)
- The orchestrator wires subscriptions, publishes the initial RAW_INPUT message, and then steps aside.
- Message flow:
  RAW_INPUT → ParseAgentNode → PRODUCT_PARSED
    → QuestionAgentNode → QUESTIONS_ANSWERED + FAQ_PAGE_READY → FAQRenderAgent → FAQ_JSON
    → ProductPageAgentNode → PRODUCT_PAGE_READY → ProductRenderAgent → PRODUCT_JSON
    → ComparisonAgentNode → COMPARISON_PAGE_READY → ComparisonRenderAgent → COMPARISON_JSON
  QUESTIONS_ANSWERED + FAQ_JSON + PRODUCT_JSON + COMPARISON_JSON → OutputCollectorAgent → ALL_OUTPUTS_READY
- The orchestrator captures ALL_OUTPUTS_READY and persists JSON to disk.

7) Sequence (Text Diagram)
- Orchestrator: publish RAW_INPUT
- ParseAgentNode: on RAW_INPUT → emit PRODUCT_PARSED
- QuestionAgentNode: on PRODUCT_PARSED → emit QUESTIONS_ANSWERED, FAQ_PAGE_READY
- FAQRenderAgent: on FAQ_PAGE_READY → emit FAQ_JSON
- ProductPageAgentNode: on PRODUCT_PARSED → emit PRODUCT_PAGE_READY
- ProductRenderAgent: on PRODUCT_PAGE_READY → emit PRODUCT_JSON
- ComparisonAgentNode: on PRODUCT_PARSED → emit COMPARISON_PAGE_READY
- ComparisonRenderAgent: on COMPARISON_PAGE_READY → emit COMPARISON_JSON
- OutputCollectorAgent: when it has all of {FAQ_JSON, PRODUCT_JSON, COMPARISON_JSON, QUESTIONS_ANSWERED} → emit ALL_OUTPUTS_READY
- Orchestrator: on ALL_OUTPUTS_READY → write outputs

8) Extensibility
- Add a new capability by introducing an agent that subscribes to existing messages (e.g., PRODUCT_PARSED) and emits new messages (e.g., REVIEW_PAGE_READY), plus a render agent for its template.
- No changes to existing agents are required; only bus wiring (subscriptions) is updated.
- Templates and content blocks are orthogonal and reusable across agents.

9) Execution & Outputs
- Command: python run.py
- Outputs (UTF‑8 JSON):
  - outputs/faq.json
  - outputs/product_page.json
  - outputs/comparison_page.json
  - outputs/all_questions.json

10) Testing Notes
- Deterministic logic; no external dependencies.
- Suggested (optional) enhancements:
  - Add jsonschema validation for each template.
  - Unit tests for blocks (transform, questions) and agent message flows.

11) Constraints Alignment
- Clear agent boundaries: Each agent has a single responsibility and explicit I/O via message types.
- Dynamic coordination: EventBus drives the flow; orchestrator does not manually sequence business logic.
- Reusable content logic: blocks in src/blocks are shared across agents and templates.
- Template engine: custom schemas and render methods per page type.
- Machine‑readable output: all final pages are JSON files.
