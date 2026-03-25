from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AddressBase(BaseModel):
    """
    Base properties for an Address. Shared across create, update, and read models.
    """
    name: str = Field(..., description="Name identifier for the address", example="Home")
    street: str = Field(..., description="Street address line", example="123 Main St")
    city: str = Field(..., description="City name", example="Springfield")
    state: str = Field(..., description="State or Province", example="IL")
    country: str = Field(..., description="Country code or name", example="USA")
    latitude: float = Field(..., description="Geographical latitude (-90 to 90)", ge=-90.0, le=90.0)
    longitude: float = Field(..., description="Geographical longitude (-180 to 180)", ge=-180.0, le=180.0)

class AddressCreate(AddressBase):
    """
    Model for Address creation requests. Inherits all fields from AddressBase as required.
    """
    pass

class AddressUpdate(BaseModel):
    """
    Model for Address update requests. Every field is optional.
    """
    name: Optional[str] = Field(None, example="Work")
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)

class AddressResponse(AddressBase):
    """
    Model for returning Address objects from the API. Includes DB-generated fields.
    """
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
