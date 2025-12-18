from typing import List, Optional
from core.models import Product, ProductStatus


class InventoryService:
    """Сервис управления инвентарем продуктов"""

    def __init__(self):
        self._inventory: List[Product] = []
        # Начальные данные
        self._load_initial_data()

    def _load_initial_data(self):
        """Загружает начальные данные"""
        initial_products = [
            Product("Молоко", "2025-04-20"),
            Product("Яйца", "2025-04-18"),
            Product("Хлеб", "2025-04-10"),
            Product("Сыр", "2025-05-05"),
        ]
        self._inventory = initial_products

    def get_all_products(self) -> List[Product]:
        """Возвращает все продукты, отсортированные по сроку годности"""
        return sorted(self._inventory, key=lambda p: p.days_until_expiry() or 9999)

    def add_product(self, name: str, expiry_date: Optional[str] = None) -> Product:
        """Добавляет новый продукт в инвентарь"""
        product = Product(name=name.strip(), expiry_date=expiry_date)
        self._inventory.append(product)
        return product

    def get_expired_products(self) -> List[Product]:
        """Возвращает просроченные продукты"""
        return [p for p in self._inventory if p.get_status() == ProductStatus.EXPIRED]

    def get_product_count(self) -> int:
        """Возвращает количество продуктов в инвентаре"""
        return len(self._inventory)

    def clear_inventory(self):
        """Очищает инвентарь"""
        self._inventory.clear()

    def get_products_as_dicts(self) -> List[dict]:
        """Возвращает продукты в виде словарей"""
        return [p.to_dict() for p in self.get_all_products()]
