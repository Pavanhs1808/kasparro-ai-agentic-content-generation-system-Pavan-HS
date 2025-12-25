import json
from typing import Dict, Any
from .agents.parser_agent import ParserAgent
from .agents.question_agent import QuestionAgent
from .agents.product_page_agent import ProductPageAgent
from .agents.comparison_agent import ComparisonAgent
from .templates.faq_template import FAQTemplate
from .templates.product_template import ProductTemplate
from .templates.comparison_template import ComparisonTemplate

class Orchestrator:
    """Coordinates agents in a simple DAG: parse -> (questions, product page, comparison) -> templates -> outputs"""

    def __init__(self) -> None:
        self.parser = ParserAgent()
        self.qagent = QuestionAgent()
        self.page_agent = ProductPageAgent()
        self.comp_agent = ComparisonAgent()
        self.faq_tmpl = FAQTemplate()
        self.prod_tmpl = ProductTemplate()
        self.comp_tmpl = ComparisonTemplate()

    def run(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        product = self.parser.run(raw)

        questions = self.qagent.run(product)
        faq_page = self.qagent.make_faq_page(product, questions)
        product_page = self.page_agent.run(product)
        comparison_page = self.comp_agent.run(product)

        outputs = {
            "faq": self.faq_tmpl.render(faq_page),
            "product_page": self.prod_tmpl.render(product_page),
            "comparison_page": self.comp_tmpl.render(comparison_page),
            "all_questions": [{"category": q.category, "question": q.text, "answer": q.answer} for q in questions],
        }
        return outputs

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
