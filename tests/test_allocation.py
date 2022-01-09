import pytest
from src.models.Order import Order
from src.models.OrderLine import OrderLine
from src.models.Batch import Batch


def test_allocate_batch():
    batch = Batch(ref=1, sku="SMALL-TABLE", quantity=20)
    line = OrderLine(order_ref=1, sku="SMALL-TABLE", quantity=2)

    assert batch.is_allocate(line)
    batch.allocate(line)
    assert 18 == batch.quantity


def test_allocate_batch_when_batch_quantity_leak_than_allocate_fail():
    batch = Batch(ref=1, sku="BLUE-CUSHION", quantity=1)
    line = OrderLine(order_ref=1, sku="BLUE-CUSHION", quantity=2)

    assert not batch.is_allocate(line)


def test_allocate_batch_when_batch_quantity_leak_than_allocate_fail():
    batch = Batch(ref=1, sku="BLUE-VASE", quantity=10)
    line = OrderLine(order_ref=1, sku="BLUE-VASE", quantity=2)

    batch.allocate(line)
    assert 8 == batch.quantity

    batch.allocate(line)
    assert 8 == batch.quantity
