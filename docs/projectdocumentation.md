# Kasparro – Agentic Content Generation System

Problem Statement
Design a modular agentic automation system that ingests a small product dataset and automatically generates structured, machine-readable content pages (FAQ, Product, Comparison). The system must use clear multi-agent boundaries, reusable logic blocks, custom templates, and output clean JSON.

Solution Overview
- Input: a minimal JSON-like product record.
- Agents: Parser, Question Generator, Product Page Assembler, Comparison Builder.
- Orchestrator: DAG-style flow that routes parsed model to worker agents and templates.
- Content Logic Blocks: small, reusable utilities for list formatting, comparisons, and Q&A answering.
- Templates: JSON schemas and renderers for the three required page types.
- Output: faq.json, product_page.json, comparison_page.json (plus all_questions.json for auditability).

Scopes & Assumptions
- Use only provided product facts; where information is absent, emit "Not specified" instead of inventing facts.
- Comparison requires a fictional Product B; this is explicitly allowed and provided as deterministic structured data.
- No external network calls; pure Python, filesystem I/O only.
- System is easily extensible to additional page types, agents, or templates.

System Design
1. Data Models (src/models.py)
   - Product, Question, FAQPage, ProductPage, ComparisonPage dataclasses.

2. Reusable Logic Blocks (src/blocks/)
   - transform.py: list joins, bullet formatting, price formatting, list comparisons, comparison summaries.
   - questions.py: category-based question generation and grounded answering that never invents facts.

3. Agents (src/agents/)
   - ParserAgent: converts raw dict input to Product model (single responsibility).
   - QuestionAgent: generates 15+ categorized questions and provides grounded answers; also selects at least 5 for FAQ.
   - ProductPageAgent: assembles product page sections using transform blocks.
   - ComparisonAgent: builds a deterministic fictional Product B and produces section-wise comparisons using transform blocks.

4. Templates (src/templates/)
   - FAQTemplate, ProductTemplate, ComparisonTemplate define schemas and render to clean JSON dicts.

5. Orchestration (src/orchestrator.py)
   - DAG: parse -> (questions, product page, comparison) -> templates -> JSON output.
   - Provides write_outputs() to persist JSON artifacts.

6. Execution (run.py)
   - Provides the given product dataset and invokes the orchestrator.

Extensibility
- Add agents without changing existing code by wiring them into the Orchestrator.
- Add new page templates by following the same schema+render pattern.
- Swap Product B generator logic in ComparisonAgent to simulate different scenarios.

Optional Diagrams (verbal)
- Orchestrator DAG: RAW -> Parser -> {QuestionAgent -> FAQTemplate, ProductPageAgent -> ProductTemplate, ComparisonAgent -> ComparisonTemplate} -> JSON files.

Testing Notes
- Run: `python run.py` to generate outputs.
- Validate JSON shape using the schemas embedded in templates or external tools if needed.
