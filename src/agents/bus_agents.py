from __future__ import annotations
from typing import Callable, List
from ..agent_core import Agent, Message
from ..models import Product
from .parser_agent import ParserAgent
from .question_agent import QuestionAgent
from .product_page_agent import ProductPageAgent
from .comparison_agent import ComparisonAgent


class ParseAgentNode:
    name = "ParseAgentNode"

    def __init__(self) -> None:
        self.parser = ParserAgent()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "RAW_INPUT":
            product = self.parser.run(msg.payload["raw"])
            publish(Message(type="PRODUCT_PARSED", payload={"product": product}))


class QuestionAgentNode:
    name = "QuestionAgentNode"

    def __init__(self) -> None:
        self.agent = QuestionAgent()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "PRODUCT_PARSED":
            product: Product = msg.payload["product"]
            qs = self.agent.run(product)
            faq_page = self.agent.make_faq_page(product, qs)
            publish(Message(type="QUESTIONS_ANSWERED", payload={"questions": qs}))
            publish(Message(type="FAQ_PAGE_READY", payload={"page": faq_page}))


class ProductPageAgentNode:
    name = "ProductPageAgentNode"

    def __init__(self) -> None:
        self.agent = ProductPageAgent()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "PRODUCT_PARSED":
            product: Product = msg.payload["product"]
            page = self.agent.run(product)
            publish(Message(type="PRODUCT_PAGE_READY", payload={"page": page}))


class ComparisonAgentNode:
    name = "ComparisonAgentNode"

    def __init__(self) -> None:
        self.agent = ComparisonAgent()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "PRODUCT_PARSED":
            product: Product = msg.payload["product"]
            page = self.agent.run(product)
            publish(Message(type="COMPARISON_PAGE_READY", payload={"page": page}))


class OutputCollectorAgent:
    name = "OutputCollectorAgent"

    def __init__(self) -> None:
        self.outputs = {}

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "FAQ_JSON":
            self.outputs["faq"] = msg.payload["data"]
        elif msg.type == "PRODUCT_JSON":
            self.outputs["product_page"] = msg.payload["data"]
        elif msg.type == "COMPARISON_JSON":
            self.outputs["comparison_page"] = msg.payload["data"]
        elif msg.type == "QUESTIONS_ANSWERED":
            qs = msg.payload["questions"]
            self.outputs["all_questions"] = [{"category": q.category, "question": q.text, "answer": q.answer} for q in qs]
        # Emit when all pieces are present
        if all(k in self.outputs for k in ("faq", "product_page", "comparison_page", "all_questions")):
            publish(Message(type="ALL_OUTPUTS_READY", payload={"outputs": dict(self.outputs)}))
