from shopping_cart.custom_tools.dataset import shopping_products
from agents import function_tool
from shopping_cart.custom_tools.add_to_cart_tool import shopping_products_cart

@function_tool
def checkout() -> str: 
    """
    Processes the payment and finalizes the order.

    Returns:
        A confirmation or error message.
    """
    if not shopping_products_cart:
        return "Your cart is empty. Please add items before checkout."
    
    else:
        total_cost = 0
        for item in shopping_products_cart:
            total_cost += item["product"]["price"] * item["quantity"]

        shopping_products_cart.clear() #empty the cart after a successful order.
        return f"Payment successful! Total cost: ${total_cost:.2f}. Your order will be delivered in 3-5 business days."
    

