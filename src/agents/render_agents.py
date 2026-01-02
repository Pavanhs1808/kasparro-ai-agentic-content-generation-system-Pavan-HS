from __future__ import annotations
from typing import Callable
from ..agent_core import Agent, Message
from ..models import Product, FAQPage, ProductPage, ComparisonPage, Question
from ..templates.faq_template import FAQTemplate
from ..templates.product_template import ProductTemplate
from ..templates.comparison_template import ComparisonTemplate


class FAQRenderAgent:
    name = "FAQRenderAgent"

    def __init__(self) -> None:
        self.tmpl = FAQTemplate()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "FAQ_PAGE_READY":
            page: FAQPage = msg.payload["page"]
            publish(Message(type="FAQ_JSON", payload={"data": self.tmpl.render(page)}))


class ProductRenderAgent:
    name = "ProductRenderAgent"

    def __init__(self) -> None:
        self.tmpl = ProductTemplate()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "PRODUCT_PAGE_READY":
            page: ProductPage = msg.payload["page"]
            publish(Message(type="PRODUCT_JSON", payload={"data": self.tmpl.render(page)}))


class ComparisonRenderAgent:
    name = "ComparisonRenderAgent"

    def __init__(self) -> None:
        self.tmpl = ComparisonTemplate()

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None:
        if msg.type == "COMPARISON_PAGE_READY":
            page: ComparisonPage = msg.payload["page"]
            publish(Message(type="COMPARISON_JSON", payload={"data": self.tmpl.render(page)}))
