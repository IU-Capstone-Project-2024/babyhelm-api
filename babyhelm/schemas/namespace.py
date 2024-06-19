from typing import Dict, Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    name: str
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None


class Values(BaseModel):
    project: Metadata
