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

    def render(self, page: FAQPage) -> Dict[str, Any]:
        return {
            "product_name": page.product_name,
            "faqs": [
                {"category": q.category, "question": q.text, "answer": q.answer or "Not specified."}
                for q in page.faqs
            ],
        }
