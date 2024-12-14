def cancel_order(order_id: str) -> str:
    """
    Cancel an order based on the order ID.
    """
    # Mock database of orders
    orders = {
        "12345": {"status": "in transit", "cancellable": False},
        "67890": {"status": "delivered", "cancellable": False},
        "54321": {"status": "processing", "cancellable": True}
    }

    # Check if the order exists
    if order_id not in orders:
        return f"Sorry, no order found with ID {order_id}. Please check the ID and try again."

    order = orders[order_id]

    # Check if the order can be cancelled
    if order["cancellable"]:
        return f"Order {order_id} has been successfully cancelled."
    else:
        return f"Order {order_id} cannot be cancelled because it is {order['status']}. \n Please reach out to our customer support representative for more details."

