from agents import function_tool

from shopping_cart.custom_tools.dataset import shopping_products


@function_tool
def check_stock(product_id: int, quantity_requested: int) -> str:
    """
    Checks the stock availability of a product.

    Args:
        product_id: The ID of the product.
        quantity_requested: The quantity requested by the user.

    Returns:
        A string indicating the stock availability.
    """
    for product in shopping_products:
        if product["id"] == product_id:
            if product["quantity"] >= quantity_requested:
                return f"There are {product['quantity']} units of {product['name']} in stock."
            else:
                return f"Only {product['quantity']} units of {product['name']} are in stock. You cannot request {quantity_requested} units."
    return "Product not found."
