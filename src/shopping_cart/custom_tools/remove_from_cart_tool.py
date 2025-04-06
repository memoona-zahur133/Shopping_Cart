from shopping_cart.custom_tools.dataset import shopping_products
from agents import function_tool
from shopping_cart.custom_tools.add_to_cart_tool import shopping_products_cart

@function_tool
def remove_from_cart(product_id: int, quantity: int) -> str:
    """
    Removes a product from the shopping cart.

    Args:
        product_id: The ID of the product.
        quantity: The quantity to remove.

    Returns:
        A confirmation message.
    """
    for item in shopping_products_cart:
        if item["product"]["id"] == product_id:
            if item["quantity"] >= quantity:
                item["quantity"] -= quantity
                if item["quantity"] == 0:
                    shopping_products_cart.remove(item)
                    return f"All {item['product']['name']}(s) removed from cart."
                else:
                    return f"{quantity} {item['product']['name']}(s) removed from cart."
            else:
                return f"Only {item['quantity']} units of {item['product']['name']} are in cart. You cannot remove {quantity} units."
    return "Product not found in cart."