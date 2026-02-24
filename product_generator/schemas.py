from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Dict, Any

Lang = Literal["DE", "EN"]

@dataclass
class Product:
    name: str
    material: str
    fit: str
    color: str
    sustainability: str = ""
    additional_details: str = ""

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Product":
        required = ["name", "material", "fit", "color"]
        missing = [k for k in required if not d.get(k)]
        if missing:
            raise ValueError(f"Product is missing required fields: {missing}")
        return Product(
            name=str(d["name"]).strip(),
            material=str(d["material"]).strip(),
            fit=str(d["fit"]).strip(),
            color=str(d["color"]).strip(),
            sustainability=str(d.get("sustainability", "")).strip(),
            additional_details=str(d.get("additional_details", "")).strip(),
        )

@dataclass
class CopyOutput:
    short_description: str
    seo_description: str
    features: List[str]
    meta_title: str
    meta_description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "short_description": self.short_description,
            "seo_description": self.seo_description,
            "features": self.features,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
        }
