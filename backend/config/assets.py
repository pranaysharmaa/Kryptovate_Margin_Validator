from decimal import Decimal

ASSETS = {
    "BTC": {
        "symbol": "BTC",
        "mark_price": Decimal("62000"),
        "contract_value": Decimal("0.001"),
        "allowed_leverage": [5, 10, 20, 50, 100],
    },
    "ETH": {
        "symbol": "ETH",
        "mark_price": Decimal("3200"),
        "contract_value": Decimal("0.01"),
        "allowed_leverage": [5, 10, 25, 50],
    },
}
