from typing import List
from ..models import Product, Question


def generate_questions(product: Product) -> List[Question]:
    name = product.name
    qs: List[Question] = []

    # Informational
    qs += [
        Question("Informational", f"What is {name}?"),
        Question("Informational", f"What are the key ingredients in {name}?"),
        Question("Informational", f"What skin types is {name} suitable for?"),
        Question("Informational", f"What is the concentration of active ingredients in {name}?"),
        Question("Informational", f"What benefits does {name} offer?"),
    ]

    # Usage
    qs += [
        Question("Usage", f"How should I use {name}?"),
        Question("Usage", f"Can {name} be used in the morning or night?"),
        Question("Usage", f"How many drops of {name} should I apply?"),
        Question("Usage", f"Should I apply sunscreen with {name}?"),
    ]

    # Safety
    qs += [
        Question("Safety", f"Are there any side effects of using {name}?"),
        Question("Safety", f"Is {name} suitable for sensitive skin?"),
        Question("Safety", f"Can I use {name} with other actives?"),
    ]

    # Purchase
    qs += [
        Question("Purchase", f"What is the price of {name}?"),
        Question("Purchase", f"How long will one bottle of {name} last?"),
    ]

    # Comparison
    qs += [
        Question("Comparison", f"How does {name} compare to other Vitamin C serums?"),
        Question("Comparison", f"What makes {name} different from Product B?"),
    ]

    # Ensure at least 15
    return qs


def answer_question(q: Question, product: Product) -> Question:
    p = product
    t = q.text.lower()

    # Specific intents first
    if "key ingredients" in t:
        q.answer = ", ".join(p.key_ingredients) if p.key_ingredients else "Not specified."
    elif "skin types" in t:
        q.answer = ", ".join(p.skin_types) if p.skin_types else "Not specified."
    elif "concentration" in t:
        q.answer = p.concentration or "Not specified."
    elif "benefits" in t:
        q.answer = ", ".join(p.benefits) if p.benefits else "Not specified."
    elif "price" in t:
        q.answer = p.price or "Not specified."
    elif t.startswith("how should i use") or "how should i use" in t:
        q.answer = p.how_to_use or "Not specified."
    elif "morning or night" in t:
        if p.how_to_use and "morning" in p.how_to_use.lower():
            q.answer = "Morning, before sunscreen."
        else:
            q.answer = "Not specified."
    elif "how many drops" in t:
        if p.how_to_use:
            import re
            # Capture counts like "2-3 drops", "2–3 drops", "2 to 3 drops", or a single number
            m = re.search(r"(\d+)(?:\s*(?:\-|\u2013|to)\s*(\d+))?\s*drops", p.how_to_use.lower())
            if m:
                a, b = m.group(1), m.group(2)
                q.answer = f"Apply {a}-{b} drops." if b else f"Apply {a} drops."
            else:
                q.answer = p.how_to_use
        else:
            q.answer = "Not specified."
    elif "sunscreen" in t:
        if p.how_to_use and "sunscreen" in p.how_to_use.lower():
            q.answer = "Yes, apply before sunscreen."
        else:
            q.answer = "Not specified."
    elif "side effects" in t:
        q.answer = p.side_effects or "Not specified."
    elif "sensitive skin" in t:
        if p.side_effects and "sensitive" in p.side_effects.lower():
            q.answer = p.side_effects
        else:
            q.answer = "Not specified."
    elif "other actives" in t:
        q.answer = "Not specified."
    elif "how long will one bottle" in t:
        q.answer = "Not specified."
    elif "compare" in t and "vitamin c serums" in t:
        q.answer = "Not specified."
    elif "different from product b" in t:
        q.answer = "See comparison page."
    elif "what is" in t:
        q.answer = f"{p.name} is a skincare serum."
    else:
        q.answer = "Not specified."
    return q
