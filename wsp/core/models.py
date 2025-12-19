"""Доменные объекты и бизнес-логика"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class ProductStatus(Enum):
    """Статус продукта по сроку годности"""
    EXPIRED = "expired"
    VALID = "valid"
    UNKNOWN = "unknown"


@dataclass
class Product:
    """Доменный объект продукта"""
    name: str
    expiry_date: Optional[str] = None
    
    def get_status(self) -> ProductStatus:
        """Определяет статус продукта по сроку годности"""
        days = self.days_until_expiry()
        if days is None:
            return ProductStatus.UNKNOWN
        return ProductStatus.EXPIRED if days < 0 else ProductStatus.VALID
    
    def days_until_expiry(self) -> Optional[int]:
        """Количество дней до истечения срока годности"""
        if not self.expiry_date:
            return None
        
        try:
            expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
            return (expiry - date.today()).days
        except ValueError:
            return None
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь"""
        return {"name": self.name, "expiry": self.expiry_date or ""}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Создает объект из словаря"""
        return cls(
            name=data.get("name", ""),
            expiry_date=data.get("expiry") or None
        )


class Recipe:
    """Доменный объект рецепта"""
    def __init__(self, name: str, ingredients: List[str], instructions: str):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions