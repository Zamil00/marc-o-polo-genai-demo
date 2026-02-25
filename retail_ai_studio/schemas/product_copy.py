from __future__ import annotations
from pydantic import BaseModel, Field, conlist, field_validator

class ProductCopy(BaseModel):
    short_description: str = Field(..., description="<= 60 words")
    seo_description: str = Field(..., description="~150 words")
    features: conlist(str, min_length=5, max_length=5)
    meta_title: str = Field(..., description="<= 60 characters")
    meta_description: str = Field(..., description="<= 155 characters")

    @field_validator("meta_title")
    @classmethod
    def title_len(cls, v: str):
        if len(v) > 60:
            raise ValueError("meta_title must be <= 60 characters")
        return v

    @field_validator("meta_description")
    @classmethod
    def desc_len(cls, v: str):
        if len(v) > 155:
            raise ValueError("meta_description must be <= 155 characters")
        return v
