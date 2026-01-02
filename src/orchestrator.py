import json
from typing import Dict, Any
from .agent_core import EventBus, Message
from .agents.bus_agents import (
    ParseAgentNode,
    QuestionAgentNode,
    ProductPageAgentNode,
    ComparisonAgentNode,
    OutputCollectorAgent,
)
from .agents.render_agents import (
    FAQRenderAgent,
    ProductRenderAgent,
    ComparisonRenderAgent,
)


class Orchestrator:
    """Coordinates autonomous agents via an event bus (message-passing graph).

    Flow:
      RAW_INPUT -> ParseAgentNode -> PRODUCT_PARSED ->
        - QuestionAgentNode -> FAQ_PAGE_READY -> FAQRenderAgent -> FAQ_JSON
        - ProductPageAgentNode -> PRODUCT_PAGE_READY -> ProductRenderAgent -> PRODUCT_JSON
        - ComparisonAgentNode -> COMPARISON_PAGE_READY -> ComparisonRenderAgent -> COMPARISON_JSON
      Questions also emit QUESTIONS_ANSWERED -> OutputCollectorAgent
      OutputCollectorAgent waits for all pieces and emits ALL_OUTPUTS_READY
    """

    def __init__(self) -> None:
        self.bus = EventBus()
        # Workers
        self.parse_node = ParseAgentNode()
        self.question_node = QuestionAgentNode()
        self.product_page_node = ProductPageAgentNode()
        self.comparison_node = ComparisonAgentNode()
        # Renderers
        self.faq_renderer = FAQRenderAgent()
        self.product_renderer = ProductRenderAgent()
        self.comparison_renderer = ComparisonRenderAgent()
        # Collector
        self.collector = OutputCollectorAgent()

        # Subscriptions (graph wiring)
        self.bus.subscribe("RAW_INPUT", self.parse_node)
        self.bus.subscribe("PRODUCT_PARSED", self.question_node)
        self.bus.subscribe("PRODUCT_PARSED", self.product_page_node)
        self.bus.subscribe("PRODUCT_PARSED", self.comparison_node)

        self.bus.subscribe("FAQ_PAGE_READY", self.faq_renderer)
        self.bus.subscribe("PRODUCT_PAGE_READY", self.product_renderer)
        self.bus.subscribe("COMPARISON_PAGE_READY", self.comparison_renderer)

        self.bus.subscribe("FAQ_JSON", self.collector)
        self.bus.subscribe("PRODUCT_JSON", self.collector)
        self.bus.subscribe("COMPARISON_JSON", self.collector)
        self.bus.subscribe("QUESTIONS_ANSWERED", self.collector)

        self._outputs: Dict[str, Any] = {}
        # Capture final outputs
        class _OutputLatch:
            name = "OutputLatch"

            def on_message(_, msg: Message, publish):
                if msg.type == "ALL_OUTPUTS_READY":
                    self._outputs = msg.payload["outputs"]
        self.bus.subscribe("ALL_OUTPUTS_READY", _OutputLatch())

    def run(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # Kick off the flow
        self.bus.publish(Message(type="RAW_INPUT", payload={"raw": raw}))
        self.bus.run()
        return dict(self._outputs)

    def write_outputs(self, outputs: Dict[str, Any], out_dir: str = "outputs") -> None:
        import os
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "faq.json"), "w", encoding="utf-8") as f:
            json.dump(outputs["faq"], f, ensure_ascii=False, indent=2)
        with open(os.path.join(out_dir, "product_page.json"), "w", encoding="utf-8") as f:
            json.dump(outputs["product_page"], f, ensure_ascii=False, indent=2)
        with open(os.path.join(out_dir, "comparison_page.json"), "w", encoding="utf-8") as f:
            json.dump(outputs["comparison_page"], f, ensure_ascii=False, indent=2)
        with open(os.path.join(out_dir, "all_questions.json"), "w", encoding="utf-8") as f:
            json.dump(outputs["all_questions"], f, ensure_ascii=False, indent=2)
