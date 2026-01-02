from typing import Dict
from ..models import Product, ProductPage
from ..blocks.transform import bullet_list

class ProductPageAgent:
    """Assemble a product page sections from reusable blocks."""

    def run(self, product: Product) -> ProductPage:
        sections: Dict[str, str] = {
            "Overview": f"{product.name} with {product.concentration or 'unspecified concentration'}.",
            "Ingredients": bullet_list(product.key_ingredients),
            "Benefits": bullet_list(product.benefits),
            "Usage": product.how_to_use or "Not specified",
            "Safety": product.side_effects or "Not specified",
            "Suitable For": bullet_list(product.skin_types),
            "Price": product.price or "Not specified",
        }
        return ProductPage(product=product, sections=sections)
