from .OrderLine import OrderLine


class Batch:
    def __init__(self, ref: int, sku: str, quantity: int, eta=None):
        self.ref = ref
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self.allocated_order_line = set()

    def allocate(self, order_line: OrderLine):
        if not self.is_allocate(order_line):
            return ;

        self.allocated_order_line.add(order_line.order_ref)
        self.quantity -= order_line.quantity

    def is_allocate(self, order_line: OrderLine):
        if order_line.sku != self.sku:
            return False

        if self.quantity < order_line.quantity:
            return False

        if order_line.order_ref in self.allocated_order_line:
            return False

        return True
