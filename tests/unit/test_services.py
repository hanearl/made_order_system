
def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch('in-stock-batch', "RETRO-CLOCK", 100, eta=None)

