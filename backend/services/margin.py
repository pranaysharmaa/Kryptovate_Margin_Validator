from decimal import Decimal, ROUND_HALF_UP

def calculate_margin(
    mark_price: Decimal,
    order_size: Decimal,
    contract_value: Decimal,
    leverage: int,
) -> Decimal:
    raw = (mark_price * order_size * contract_value) / Decimal(leverage)
    return raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
