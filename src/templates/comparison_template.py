from typing import Dict, Any
from ..models import ComparisonPage, Product

class ComparisonTemplate:
    schema = {
        "type": "object",
        "required": ["product_a", "product_b", "comparisons"],
    }

    def _product_to_dict(self, p: Product) -> Dict[str, Any]:
        return {
            "name": p.name,
            "concentration": p.concentration,
            "skin_types": p.skin_types,
            "ingredients": p.key_ingredients,
            "benefits": p.benefits,
            "usage": p.how_to_use,
            "side_effects": p.side_effects,
            "price": p.price,
        }

    def render(self, page: ComparisonPage) -> Dict[str, Any]:
        return {
            "product_a": self._product_to_dict(page.product_a),
            "product_b": self._product_to_dict(page.product_b),
            "comparisons": page.comparisons,
        }
