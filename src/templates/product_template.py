from typing import Dict, Any
from ..models import Product, ProductPage
from ..blocks.transform import join_list, fmt_price

class ProductTemplate:
    schema = {
        "type": "object",
        "required": ["name", "concentration", "skin_types", "ingredients", "benefits", "usage", "side_effects", "price"],
    }

    def render(self, page: ProductPage) -> Dict[str, Any]:
        p: Product = page.product
        return {
            "name": p.name,
            "concentration": p.concentration or "Not specified",
            "skin_types": p.skin_types or [],
            "ingredients": p.key_ingredients or [],
            "benefits": p.benefits or [],
            "usage": p.how_to_use or "Not specified",
            "side_effects": p.side_effects or "Not specified",
            "price": fmt_price(p.price),
            "sections": page.sections,
        }
