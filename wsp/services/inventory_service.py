from typing import List, Optional
from wsp.core.models import Product, ProductStatus


class InventoryService:
    """Сервис управления инвентарем продуктов"""

    def __init__(self):
        self._inventory: List[Product] = []
        # Начальные данные
        self._load_initial_data()

    def _load_initial_data(self):
        """Загружает начальные данные"""
        initial_products = [
            Product("Молоко", "2025-04-20", 1.0, "л"),
            Product("Яйца", "2025-04-18", 10, "шт"),
            Product("Хлеб", "2025-04-10", 1, "шт"),
            Product("Сыр", "2025-05-05", 500, "г"),
        ]
        self._inventory = initial_products

    def get_all_products(self) -> List[Product]:
        """Возвращает все продукты, отсортированные по сроку годности"""
        return sorted(self._inventory, key=lambda p: p.days_until_expiry() or 9999)

    def add_product(self, name: str, expiry_date: Optional[str] = None,
                    amount: Optional[float] = None, unit: Optional[str] = None) -> Product:
        """Добавляет новый продукт в инвентарь"""
        product = Product(name=name.strip(), expiry_date=expiry_date,
                          amount=amount, unit=unit)
        self._inventory.append(product)
        return product

    # НОВЫЙ МЕТОД ДЛЯ ОБНОВЛЕНИЯ ПРОДУКТА
    def update_product(self, index: int, name: str, expiry_date: Optional[str] = None,
                       amount: Optional[float] = None, unit: Optional[str] = None) -> bool:
        """Обновляет продукт в инвентаре по индексу"""
        if 0 <= index < len(self._inventory):
            product = self._inventory[index]
            product.name = name.strip()
            product.expiry_date = expiry_date
            product.amount = amount
            product.unit = unit
            return True
        return False

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
