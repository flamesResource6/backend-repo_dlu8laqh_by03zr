"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (you can still use these elsewhere if needed)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio profile schema (collection name: "profile")
class Profile(BaseModel):
    name: str = Field(..., description="Person's display name")
    tagline: Optional[str] = Field(None, description="Short one-liner under the name")
    bio: Optional[str] = Field(None, description="Longer about text")
    roles: List[str] = Field(default_factory=list, description="Primary roles/titles")
    skills: List[str] = Field(default_factory=list, description="Key skills or knowledge areas")
    hobbies: List[str] = Field(default_factory=list, description="Personal hobbies")
    avatar_url: Optional[str] = Field(None, description="Public URL for the profile image")
