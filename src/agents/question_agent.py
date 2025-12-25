from typing import List
from ..models import Product, Question, FAQPage
from ..blocks.questions import generate_questions, answer_question

class QuestionAgent:
    """Generate categorized questions and answers."""

    def run(self, product: Product) -> List[Question]:
        qs = generate_questions(product)
        answered = [answer_question(q, product) for q in qs]
        return answered

    def make_faq_page(self, product: Product, questions: List[Question]) -> FAQPage:
        # select at least 5 questions with answers
        selected = []
        for q in questions:
            if q.answer and q.answer != "Not specified.":
                selected.append(q)
        # ensure minimum 5; if not, pad with any
        if len(selected) < 5:
            selected = (selected + questions)[:5]
        return FAQPage(product_name=product.name, faqs=selected)
