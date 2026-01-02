from typing import List, Dict, Any
from ..models import FAQPage, Question

class FAQTemplate:
    schema = {
        "type": "object",
        "required": ["product_name", "faqs"],
        "properties": {
            "product_name": {"type": "string"},
            "faqs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["category", "question", "answer"],
                    "properties": {
                        "category": {"type": "string"},
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                },
                "minItems": 5,
            },
        },
    }

    def _validate(self, data: Dict[str, Any]) -> None:
        if "product_name" not in data or "faqs" not in data:
            raise ValueError("FAQTemplate missing required fields")
        if not isinstance(data["faqs"], list) or len(data["faqs"]) < 5:
            raise ValueError("FAQTemplate requires at least 5 FAQ items")

    def render(self, page: FAQPage) -> Dict[str, Any]:
        data = {
            "product_name": page.product_name,
            "faqs": [
                {"category": q.category, "question": q.text, "answer": q.answer or "Not specified."}
                for q in page.faqs
            ],
        }
        self._validate(data)
        return data
