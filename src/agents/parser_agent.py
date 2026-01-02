from typing import Dict, Any
from ..models import Product

class ParserAgent:
    """Single-responsibility: parse raw dict into Product model."""

    def run(self, raw: Dict[str, Any]) -> Product:
        return Product(
            name=raw.get("Product Name", ""),
            concentration=raw.get("Concentration"),
            skin_types=[s.strip() for s in raw.get("Skin Type", "").split(",") if s.strip()],
            key_ingredients=[s.strip() for s in raw.get("Key Ingredients", "").split(",") if s.strip()],
            benefits=[s.strip() for s in raw.get("Benefits", "").split(",") if s.strip()],
            how_to_use=raw.get("How to Use"),
            side_effects=raw.get("Side Effects"),
            price=raw.get("Price"),
        )
