from fastapi import APIRouter, HTTPException
from decimal import Decimal, ROUND_HALF_UP
from config.assets import ASSETS
from models.schemas import MarginRequest
from services.margin import calculate_margin
from services.logger import log_event

router = APIRouter(prefix="/margin", tags=["margin"])

DECIMAL_2 = Decimal("0.01")


@router.post("/validate")
def validate_margin(req: MarginRequest):
    asset = req.asset.upper()

    # Validate asset
    if asset not in ASSETS:
        log_event("VALIDATION_FAILED", {
            "reason": "unsupported_asset",
            "asset": asset
        })
        raise HTTPException(400, "Unsupported asset")

    cfg = ASSETS[asset]

    # Validate leverage
    if req.leverage not in cfg["allowed_leverage"]:
        log_event("VALIDATION_FAILED", {
            "reason": "invalid_leverage",
            "asset": asset,
            "leverage": req.leverage
        })
        raise HTTPException(400, "Invalid leverage")

    # Validate order size
    order_size = Decimal(req.order_size)
    if order_size <= Decimal("0"):
        log_event("VALIDATION_FAILED", {
            "reason": "invalid_order_size",
            "asset": asset,
            "order_size": req.order_size
        })
        return {
            "status": "error",
            "message": "Order size must be greater than zero",
            "margin_required": 0
        }

    # Compute backend margin
    backend_margin = calculate_margin(
        cfg["mark_price"],
        order_size,
        cfg["contract_value"],
        req.leverage
    ).quantize(DECIMAL_2, rounding=ROUND_HALF_UP)

    # Normalize client margin to same scale
    client_margin = Decimal(req.margin_client).quantize(
        DECIMAL_2, rounding=ROUND_HALF_UP
    )

    log_event("MARGIN_COMPUTED", {
        "asset": asset,
        "order_size": float(order_size),
        "leverage": req.leverage,
        "client_margin": float(client_margin),
        "backend_margin": float(backend_margin)
    })

    # Reject zero-margin orders
    if backend_margin == Decimal("0.00"):
        log_event("VALIDATION_FAILED", {
            "reason": "zero_margin_order",
            "asset": asset,
            "order_size": req.order_size
        })
        return {
            "status": "error",
            "message": "Order size too small – margin rounds to zero",
            "margin_required": 0
        }

    # Margin sufficiency check
    if client_margin < backend_margin:
        log_event("VALIDATION_FAILED", {
            "reason": "insufficient_margin",
            "asset": asset,
            "client_margin": float(client_margin),
            "required_margin": float(backend_margin)
        })
        return {
            "status": "error",
            "message": "Insufficient margin submitted",
            "margin_required": float(backend_margin)
        }

    # Success
    log_event("VALIDATION_SUCCESS", {
        "asset": asset,
        "margin_required": float(backend_margin)
    })

    return {
        "status": "ok",
        "margin_required": float(backend_margin)
    }
