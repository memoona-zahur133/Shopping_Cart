from agents import function_tool

@function_tool
def continue_shopping() -> str:
    """
    Provides a message to continue shopping.

    Returns:
        A message to continue shopping.
    """
    return "You can continue shopping or proceed to checkout."