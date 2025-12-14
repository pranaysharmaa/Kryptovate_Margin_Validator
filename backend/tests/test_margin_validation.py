from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Helper payload

def base_payload():
    return {
        "asset": "BTC",
        "order_size": 2,
        "side": "long",
        "leverage": 20,
        "margin_client": 6.2
    }


#  Valid margin

def test_valid_margin_passes():
    payload = base_payload()
    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["margin_required"] == 6.2



#  Insufficient margin

def test_insufficient_margin_fails():
    payload = base_payload()
    payload["margin_client"] = 6.19

    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "error"
    assert body["message"] == "Insufficient margin submitted"



#  Zero-margin order 

def test_zero_margin_order_rejected():
    payload = {
        "asset": "BTC",
        "order_size": 0.0000001,
        "side": "long",
        "leverage": 20,
        "margin_client": 0
    }

    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "error"
    assert "rounds to zero" in body["message"]



#  Invalid leverage

def test_invalid_leverage_rejected():
    payload = base_payload()
    payload["leverage"] = 15

    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid leverage"



#  Unsupported asset

def test_unsupported_asset_rejected():
    payload = base_payload()
    payload["asset"] = "DOGE"

    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 400
    assert res.json()["detail"] == "Unsupported asset"



#  Rounding HALF_UP correctness

def test_rounding_half_up():
    payload = {
        "asset": "BTC",
        "order_size": 2.0145,  # to create .xx5 ambiguity
        "side": "long",
        "leverage": 20,
        "margin_client": 6.25
    }

    res = client.post("/margin/validate", json=payload)

    body = res.json()
    assert body["status"] == "ok"
    assert body["margin_required"] == 6.25

#  Negative order size

def test_negative_order_size_rejected():
    payload = {
        "asset": "BTC",
        "order_size": "-2",
        "side": "long",
        "leverage": 20,
        "margin_client": "0"
    }

    res = client.post("/margin/validate", json=payload)

    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "error"
    assert body["message"] == "Order size must be greater than zero"
