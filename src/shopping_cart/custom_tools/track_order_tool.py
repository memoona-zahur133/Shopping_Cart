from agents import function_tool

orders = {
    1001: {"status": "Shipped", "tracking_number": "TRACK12345"},
    1002: {"status": "Delivered", "tracking_number": "TRACK67890"},
    1003: {"status": "Processing", "tracking_number": None},
}

@function_tool
def track_order(order_id: int) -> str:
    """
    Tracks an order by its ID.

    Args:
        order_id: The ID of the order to track.

    Returns:
        The order status and tracking information, or a message if the order is not found.
    """
    if order_id in orders:
        order = orders[order_id]
        if order["tracking_number"]:
            return f"Order {order_id} is {order['status']}. Tracking number: {order['tracking_number']}."
        else:
            return f"Order {order_id} is {order['status']}. Tracking number will be available soon."
    else:
        return "Order not found."