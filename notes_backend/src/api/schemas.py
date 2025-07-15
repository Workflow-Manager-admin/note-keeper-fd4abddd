from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """User registration payload."""
    username: str = Field(..., min_length=3, max_length=128, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Login payload."""
    username: str
    password: str

# PUBLIC_INTERFACE
class UserOut(BaseModel):
    """User info for response."""
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

# PUBLIC_INTERFACE
class TokenData(BaseModel):
    """Payload extracted from JWT."""
    username: Optional[str] = None

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base note fields."""
    title: str
    content: Optional[str] = ""

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Create note payload."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Update note payload."""
    title: Optional[str] = None
    content: Optional[str] = None

# PUBLIC_INTERFACE
class NoteOut(NoteBase):
    """Returned note model."""
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class ErrorResponse(BaseModel):
    """Generic error response."""
    detail: str
