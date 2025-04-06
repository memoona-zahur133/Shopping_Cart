from agents import function_tool

common_questions = {
    "What are your delivery options?": "We offer standard and express delivery. Standard delivery takes 3-5 business days, and express delivery takes 1-2 business days.",
    "What is your return policy?": "You can return items within 30 days of purchase for a full refund.",
    "How can I track my order?": "You can track your order using the tracking number provided in your order confirmation email.",
    "Do you offer international shipping?": "Yes, we ship internationally. Please check our website for a list of countries we ship to.",
    "What payment methods do you accept?": "We accept all major credit cards, PayPal, and bank transfers.",
}

@function_tool
def answer_common_questions(question: str) -> str:
    """
    Answers common customer questions.

    Args:
        question: The customer's question.

    Returns:
        The answer to the question, or a message if the question is not found.
    """
    if question in common_questions:
        return common_questions[question]
    else:
        return "I'm sorry, I don't have an answer to that question. Please contact our support team for further assistance."