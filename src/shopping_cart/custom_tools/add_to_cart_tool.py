from agents import function_tool

from shopping_cart.custom_tools.dataset import shopping_products

shopping_products_cart = []

msg = "Product not found!"

@function_tool
def add_to_cart(product_id: int, quantity: int) -> str:
    """
    Adds a product to the shopping cart.

    Args:
        product_id: The ID of the product.
        quantity: The quantity to add.

    Returns:
        A confirmation message.
    """
    for product in shopping_products:
        if product["id"] == product_id:
            shopping_products_cart.append({
                "product": product,
                "quantity": quantity
            })
            return f"{quantity} {product['name']}(s) added to cart."
    return msg