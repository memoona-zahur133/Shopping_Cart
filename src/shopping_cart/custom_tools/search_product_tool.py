from agents import function_tool

from shopping_cart.custom_tools.dataset import shopping_products


@function_tool
def search_product(query: str)  -> list[dict]:
    """
    Searches the products list for items matching the given query.

    Args:
        query: The user's search term.

    Returns:
        A list of product dictionaries matching the query.
    """
    query = query.lower()  # Convert query to lowercase for case-insensitive search
    results = []
    for product in shopping_products:
        if query in product["name"].lower() or query in product["details"].lower():
            results.append(product)
    return results
