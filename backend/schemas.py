from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Robot(BaseModel):
    id: int
    start_with: int
    created_at: datetime
    stope_at: Optional[datetime]
