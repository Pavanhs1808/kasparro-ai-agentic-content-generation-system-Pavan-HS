import unittest
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

class TestPipeline(unittest.TestCase):
    def test_end_to_end(self):
        orch = Orchestrator()
        outputs = orch.run(RAW_INPUT)
        self.assertIn("faq", outputs)
        self.assertIn("product_page", outputs)
        self.assertIn("comparison_page", outputs)
        self.assertIn("all_questions", outputs)
        # Ensure drop count answer normalized with hyphen
        found = False
        for qa in outputs["all_questions"]:
            if qa["question"].lower().startswith("how many drops"):
                self.assertIn("Apply 2-3 drops", qa["answer"])  # hyphen normalized
                found = True
        self.assertTrue(found, "Expected a 'how many drops' QA")
        # Ensure price is present
        self.assertEqual(outputs["product_page"]["price"], "₹699")

if __name__ == "__main__":
    unittest.main()
