from agents import function_tool
from shopping_cart.custom_tools.dataset import shopping_products

user_preferences = {
    1: {"categories": ["Smart Home", "Electronics"], "recent_purchases": [10, 11]},
    2: {"categories": ["Gaming", "Electronics"], "recent_purchases": [9, 6]},
    3: {"categories": ["Home Appliances"], "recent_purchases": [15, 18]},
}

@function_tool
def recommend_products(user_id: int) -> list[dict]:
    """
    Recommends products based on user preferences and shopping history.

    Args:
        user_id: The ID of the user.

    Returns:
        A list of recommended product dictionaries.
    """
    if user_id not in user_preferences:
        return [{"message": "User preferences not found."}]

    preferences = user_preferences[user_id]
    recommended_products = []
    for product in shopping_products:
        if any(category in preferences["categories"] for category in [product.get("details", ""), product.get("name", "")]):
            recommended_products.append(product)

    #Simulate adding in items the user has recently purchased.
    for product in shopping_products:
      if product["id"] in preferences["recent_purchases"]:
        recommended_products.append(product)

    #remove duplicate entries.
    recommended_products = list(dict.fromkeys(map(tuple, map(dict.items, recommended_products))))
    return recommended_products