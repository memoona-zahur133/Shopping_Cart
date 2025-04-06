from shopping_cart.custom_tools.dataset import shopping_products
from agents import function_tool
from shopping_cart.custom_tools.add_to_cart_tool import shopping_products_cart

@function_tool
def see_cart() -> list[dict]:
    """
    Displays the contents of the shopping cart.

    Returns:
        A list of dictionaries representing the cart items.
    """
    cart_items = []
    for item in shopping_products_cart:
        cart_items.append({
            "name": item["product"]["name"],
            "quantity": item["quantity"],
            "price": item["product"]["price"]
        })
    return cart_items