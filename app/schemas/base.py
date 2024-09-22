from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import List, Optional

class ConferenceState(str, Enum):
    CREATED = "CREATED"
    SUBMISSION = "SUBMISSION"
    ASSIGNMENT = "ASSIGNMENT"
    REVIEW = "REVIEW"
    DECISION = "DECISION"
    FINAL_SUBMISSION = "FINAL_SUBMISSION"
    FINAL = "FINAL"


class RoleType(str, Enum):
  USER = "USER"
  ADMIN = "ADMIN"

class RoleBase(BaseModel):
  role_type: RoleType
  conference_id: int | None = None

class RoleCreate(RoleBase):
  pass

class Role(RoleBase):
  id: int

  class Config:
    from_attributes = True

class PaperBase(BaseModel):
  title: str
  abstract: str
  content: Optional[str] = None
  keywords: Optional[List[str]] = None

class ConferenceBase(BaseModel):
  name: str
  description: str
  