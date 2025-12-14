from fastapi import APIRouter
from config.assets import ASSETS

router = APIRouter(prefix="/config", tags=["assets"])

@router.get("/assets")
def get_assets():
    return {
        "assets": [
            {
                "symbol": a["symbol"],
                "mark_price": float(a["mark_price"]),
                "contract_value": float(a["contract_value"]),
                "allowed_leverage": a["allowed_leverage"],
            }
            for a in ASSETS.values()
        ]
    }
