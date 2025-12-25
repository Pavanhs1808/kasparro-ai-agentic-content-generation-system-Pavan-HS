from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal

QuestionCategory = Literal["Informational", "Safety", "Usage", "Purchase", "Comparison"]

@dataclass
class Product:
    name: str
    concentration: Optional[str] = None
    skin_types: List[str] = field(default_factory=list)
    key_ingredients: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    how_to_use: Optional[str] = None
    side_effects: Optional[str] = None
    price: Optional[str] = None

@dataclass
class Question:
    category: QuestionCategory
    text: str
    answer: Optional[str] = None

@dataclass
class FAQPage:
    product_name: str
    faqs: List[Question]

@dataclass
class ProductPage:
    product: Product
    sections: Dict[str, str]

@dataclass
class ComparisonPage:
    product_a: Product
    product_b: Product
    comparisons: Dict[str, Dict[str, str]]  # section -> {a: str, b: str, summary: str}
