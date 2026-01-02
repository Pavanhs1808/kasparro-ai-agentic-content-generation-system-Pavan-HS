from typing import Dict, Any
from ..models import Product, ProductPage
from ..blocks.transform import join_list, fmt_price, normalize_punctuation

class ProductTemplate:
    schema = {
        "type": "object",
        "required": ["name", "concentration", "skin_types", "ingredients", "benefits", "usage", "side_effects", "price"],
    }

    def _validate(self, data: Dict[str, Any]) -> None:
        required = ["name", "concentration", "skin_types", "ingredients", "benefits", "usage", "side_effects", "price"]
        for k in required:
            if k not in data:
                raise ValueError(f"ProductTemplate missing required field: {k}")

    def render(self, page: ProductPage) -> Dict[str, Any]:
        p: Product = page.product
        data = {
            "name": p.name,
            "concentration": p.concentration or "Not specified",
            "skin_types": p.skin_types or [],
            "ingredients": p.key_ingredients or [],
            "benefits": p.benefits or [],
            "usage": normalize_punctuation(p.how_to_use) or "Not specified",
            "side_effects": normalize_punctuation(p.side_effects) or "Not specified",
            "price": fmt_price(p.price),
            "sections": page.sections,
        }
        self._validate(data)
        return data
