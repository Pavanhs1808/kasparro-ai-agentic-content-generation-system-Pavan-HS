from typing import Dict
from ..models import Product, ComparisonPage
from ..blocks.transform import compare_lists, summarize_comparison

class ComparisonAgent:
    """Create a fictional Product B and compare with Product A."""

    def _make_product_b(self) -> Product:
        # Fictional structured product B
        return Product(
            name="RadianceShield Vitamin C+ Serum",
            concentration="12% Vitamin C",
            skin_types=["Normal", "Combination"],
            key_ingredients=["Vitamin C", "Niacinamide"],
            benefits=["Brightening", "Evens skin tone"],
            how_to_use="Apply 2–3 drops at night on clean skin",
            side_effects="May cause mild irritation for very sensitive skin",
            price="₹799",
        )

    def run(self, product_a: Product) -> ComparisonPage:
        product_b = self._make_product_b()

        # Ingredients comparison
        ing_cmp = compare_lists(product_a.key_ingredients, product_b.key_ingredients)
        ing_summary = summarize_comparison("Ingredients", ing_cmp["overlap"], ing_cmp["only_a"], ing_cmp["only_b"])

        skin_cmp = compare_lists(product_a.skin_types, product_b.skin_types)
        skin_summary = summarize_comparison("Skin Types", skin_cmp["overlap"], skin_cmp["only_a"], skin_cmp["only_b"])

        ben_cmp = compare_lists(product_a.benefits, product_b.benefits)
        ben_summary = summarize_comparison("Benefits", ben_cmp["overlap"], ben_cmp["only_a"], ben_cmp["only_b"])

        comparisons: Dict[str, Dict[str, str]] = {
            "Concentration": {
                "a": product_a.concentration or "Not specified",
                "b": product_b.concentration or "Not specified",
                "summary": "Higher concentration in Product B" if (product_b.concentration and product_a.concentration and product_b.concentration != product_a.concentration) else "Similar or unspecified",
            },
            "Ingredients": {
                "a": ", ".join(product_a.key_ingredients) or "Not specified",
                "b": ", ".join(product_b.key_ingredients) or "Not specified",
                "summary": ing_summary,
            },
            "Skin Types": {
                "a": ", ".join(product_a.skin_types) or "Not specified",
                "b": ", ".join(product_b.skin_types) or "Not specified",
                "summary": skin_summary,
            },
            "Benefits": {
                "a": ", ".join(product_a.benefits) or "Not specified",
                "b": ", ".join(product_b.benefits) or "Not specified",
                "summary": ben_summary,
            },
            "Usage": {
                "a": product_a.how_to_use or "Not specified",
                "b": product_b.how_to_use or "Not specified",
                "summary": "Different recommended timing",
            },
            "Price": {
                "a": product_a.price or "Not specified",
                "b": product_b.price or "Not specified",
                "summary": "Product B is priced higher" if (product_a.price and product_b.price and product_a.price != product_b.price) else "Similar or unspecified",
            },
        }

        return ComparisonPage(product_a=product_a, product_b=product_b, comparisons=comparisons)
