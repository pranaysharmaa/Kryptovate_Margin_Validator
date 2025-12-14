import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger("margin_engine")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

def log_event(event: str, payload: dict):
    logger.info(
        json.dumps({
            "event": event,
            "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
            **payload
        })
    )
