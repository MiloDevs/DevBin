from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


class HealthService:
    def __init__(self, session: sessionmaker):
        self.session_maker = session

    async def check(self) -> dict[str, Any]:
        # Try a lightweight DB roundtrip
        try:
            async with self.session_maker() as session:
                await session.execute(text("SELECT 1"))
                db_status = "ok"
        except Exception as exc:  # pragma: no cover - minimal bootstrap
            logging.error(exc)
            db_status = f"error: {exc.__class__.__name__}"

        return {"status": "ok", "dependencies": {"database": db_status}}
