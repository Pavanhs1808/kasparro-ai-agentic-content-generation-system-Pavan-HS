import json
from src.orchestrator import Orchestrator

RAW_INPUT = {
    "Product Name": "GlowBoost Vitamin C Serum",
    "Concentration": "10% Vitamin C",
    "Skin Type": "Oily, Combination",
    "Key Ingredients": "Vitamin C, Hyaluronic Acid",
    "Benefits": "Brightening, Fades dark spots",
    "How to Use": "Apply 2–3 drops in the morning before sunscreen",
    "Side Effects": "Mild tingling for sensitive skin",
    "Price": "₹699",
}

if __name__ == "__main__":
    orch = Orchestrator()
    outputs = orch.run(RAW_INPUT)
    orch.write_outputs(outputs)
    print("Generated outputs in outputs/ directory:")
    for k in ["faq.json", "product_page.json", "comparison_page.json", "all_questions.json"]:
        print("- outputs/" + k)
