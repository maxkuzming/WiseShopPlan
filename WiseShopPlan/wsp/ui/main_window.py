import tkinter as tk
from tkinter import messagebox
from datetime import date
from typing import Optional

from wsp.config import COLORS, FONTS
from wsp.core.models import Product
from wsp.services.inventory_service import InventoryService
from wsp.services.yandex_gpt_service import YandexGPTService


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("WiseShopPlan")
        self.root.title
        self.root.geometry("550x550")
        self.root.resizable(False, False)

        # Инициализация сервисов
        self.inventory_service = InventoryService()
        self.gpt_service = YandexGPTService()

        # Создание фреймов
        self.main_frame = None
        self.name_frame = None
        self.ingr_frame = None
        self.inventory_frame = None

        # Виджеты
        self.name_entry = None
        self.ingr_entry = None
        self.name_result_text = None
        self.ingr_result_text = None
        self.inventory_listbox = None

        self._setup_ui()

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        self._create_main_frame()
        self._create_name_search_frame()
        self._create_ingredient_search_frame()
        self._create_inventory_frame()

        self.show_main()

    def _create_main_frame(self):
        """Создает главное меню"""
        self.main_frame = tk.Frame(self.root, bg=COLORS["FRAME_BG"])

        header = tk.Label(
            self.main_frame,
            text="WiseShopPlan",
            font=FONTS["TITLE"],
            fg=COLORS["PRIMARY_GREEN"],
            bg=COLORS["FRAME_BG"],
        )
        header.pack(pady=(20, 20))

        button_config = {
            "width": 26,
            "height": 2,
            "bg": COLORS["BUTTON_GREEN"],
            "fg": COLORS["WHITE"],
            "font": ("Arial", 11, "bold"),
            "bd": 0,
            "relief": "flat",
        }

        tk.Button(
            self.main_frame,
            text="Рецепты",
            command=self.show_name_search,
            **button_config,
        ).pack(pady=8)
        tk.Button(
            self.main_frame,
            text="Планировщик",
            command=self.show_ingredient_search,
            **button_config,
        ).pack(pady=8)
        tk.Button(
            self.main_frame,
            text="Меню на неделю",
            command=self._show_health_menu,
            **button_config,
        ).pack(pady=8)
        tk.Button(
            self.main_frame,
            text="Мои продукты",
            command=self.show_inventory,
            **button_config,
        ).pack(pady=8)

    def _create_name_search_frame(self):
        """Создает фрейм поиска по названию"""
        self.name_frame = tk.Frame(self.root, bg=COLORS["FRAME_BG"])

        tk.Label(
            self.name_frame,
            text="Поиск рецепта",
            font=FONTS["HEADER"],
            bg=COLORS["FRAME_BG"],
        ).pack(pady=(15, 10))

        self.name_entry = tk.Entry(self.name_frame, font=FONTS["NORMAL"], width=36)
        self.name_entry.pack(pady=5)

        tk.Button(
            self.name_frame,
            text="Найти рецепт",
            command=self._search_by_name,
            bg=COLORS["ACTIVE_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(pady=10)

        self.name_result_text = tk.Text(
            self.name_frame,
            height=12,
            width=58,
            font=FONTS["SMALL"],
            wrap="word",
            bg=COLORS["BACKGROUND"],
        )
        self.name_result_text.pack(pady=10, padx=10)
        self.name_result_text.config(state="disabled")

        tk.Button(
            self.name_frame,
            text="← Назад",
            command=self.show_main,
            bg=COLORS["DARK_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=15,
        ).pack(pady=5)

    def _create_ingredient_search_frame(self):
        """Создает фрейм поиска по ингредиентам"""
        self.ingr_frame = tk.Frame(self.root, bg=COLORS["FRAME_BG"])

        tk.Label(
            self.ingr_frame,
            text="Что приготовить?",
            font=FONTS["HEADER"],
            bg=COLORS["FRAME_BG"],
        ).pack(pady=(15, 10))

        self.ingr_entry = tk.Entry(self.ingr_frame, font=FONTS["NORMAL"], width=36)
        self.ingr_entry.pack(pady=5)

        tk.Button(
            self.ingr_frame,
            text="Что приготовить?",
            command=self._search_by_ingredients,
            bg=COLORS["ACTIVE_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(pady=10)

        self.ingr_result_text = tk.Text(
            self.ingr_frame,
            height=12,
            width=58,
            font=FONTS["SMALL"],
            wrap="word",
            bg=COLORS["BACKGROUND"],
        )
        self.ingr_result_text.pack(pady=10, padx=10)
        self.ingr_result_text.config(state="disabled")

        tk.Button(
            self.ingr_frame,
            text="Назад",
            command=self.show_main,
            bg=COLORS["DARK_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=15,
        ).pack(pady=5)

    def _create_inventory_frame(self):
        """Создает фрейм инвентаря"""
        self.inventory_frame = tk.Frame(self.root, bg=COLORS["FRAME_BG"])

    def _get_bg_color(self, expiry_str: Optional[str]) -> str:
        """Возвращает цвет фона в зависимости от срока годности"""
        if not expiry_str:
            return COLORS["BACKGROUND"]

        product = Product(name="temp", expiry_date=expiry_str)
        days = product.days_until_expiry()

        return COLORS["EXPIRED"] if days is not None and days < 0 else COLORS["VALID"]

    def _show_health_menu(self):
        """Показывает меню здорового питания"""
        messagebox.showinfo("Здоровое питание", "Меню на неделю будет добавлено позже.")

    def show_main(self):
        """Показывает главное меню"""
        for frame in [self.name_frame, self.ingr_frame, self.inventory_frame]:
            if frame:
                frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_name_search(self):
        """Показывает экран поиска по названию"""
        self.main_frame.pack_forget()
        self.name_frame.pack(fill="both", expand=True)
        self.name_entry.focus_set()

    def show_ingredient_search(self):
        """Показывает экран поиска по ингредиентам"""
        self.main_frame.pack_forget()
        self.ingr_frame.pack(fill="both", expand=True)
        self.ingr_entry.focus_set()

    def show_inventory(self):
        """Показывает экран инвентаря"""
        self.main_frame.pack_forget()
        self.inventory_frame.pack(fill="both", expand=True)

        # Очищаем фрейм при каждом открытии
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.inventory_frame,
            text="Инвентарь",
            font=FONTS["HEADER"],
            bg=COLORS["FRAME_BG"],
        ).pack(pady=(20, 15))

        listbox_frame = tk.Frame(self.inventory_frame, bg=COLORS["FRAME_BG"])
        listbox_frame.pack(pady=10)

        self.inventory_listbox = tk.Listbox(
            listbox_frame, width=55, height=8, font=("Arial", 11)
        )
        self.inventory_listbox.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(
            listbox_frame, orient="vertical", command=self.inventory_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.inventory_listbox.config(yscrollcommand=scrollbar.set)

        # Заполняем список
        products = self.inventory_service.get_all_products()
        if products:
            for product in products:
                line = product.name
                if product.expiry_date:
                    line += f" (до {product.expiry_date})"
                self.inventory_listbox.insert(tk.END, line)

                idx = self.inventory_listbox.size() - 1
                color = self._get_bg_color(product.expiry_date)
                self.inventory_listbox.itemconfig(idx, {"bg": color})
        else:
            self.inventory_listbox.insert(tk.END, "Пусто")

        tk.Button(
            self.inventory_frame,
            text="Добавить продукт",
            command=self._show_add_product_form,
            bg=COLORS["ACTIVE_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(pady=10)

        tk.Button(
            self.inventory_frame,
            text="← В главное меню",
            command=self.show_main,
            bg=COLORS["DARK_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(pady=5)

    def _show_add_product_form(self):
        """Показывает форму добавления продукта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить продукт")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Название:", font=FONTS["SMALL"]).pack(pady=(15, 5))
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="Срок (ГГГГ-ММ-ДД):", font=FONTS["SMALL"]).pack(
            pady=(5, 5)
        )
        expiry_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        expiry_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        expiry_entry.pack(pady=5)

        def add_product():
            name = name_entry.get().strip()
            expiry = expiry_entry.get().strip()

            if not name:
                messagebox.showwarning("Ошибка", "Введите название продукта")
                return

            # Валидация даты
            if expiry:
                temp_product = Product(name="temp", expiry_date=expiry)
                if temp_product.days_until_expiry() is None:
                    messagebox.showwarning(
                        "Ошибка", "Неверный формат даты.\nПример: 2025-04-20"
                    )
                    return

            self.inventory_service.add_product(name, expiry or None)
            self.show_inventory()
            dialog.destroy()

        tk.Button(
            dialog,
            text="Добавить",
            command=add_product,
            bg=COLORS["ACTIVE_GREEN"],
            fg=COLORS["WHITE"],
            font=("Arial", 10, "bold"),
            width=15,
        ).pack(pady=15)

    def _search_by_name(self):
        """Выполняет поиск рецепта по названию"""
        query = self.name_entry.get().strip()
        if not query:
            messagebox.showwarning(
                "Внимание", "Введите название блюда (например: борщ)"
            )
            return

        self._update_text_widget(self.name_result_text, "ИИ думает...")

        answer = self.gpt_service.get_recipe_by_name(query)
        self._update_text_widget(self.name_result_text, answer)

    def _search_by_ingredients(self):
        """Выполняет поиск рецепта по ингредиентам"""
        query = self.ingr_entry.get().strip()
        if not query:
            messagebox.showwarning(
                "Внимание", "Введите ингредиенты (например: яйца, помидоры)"
            )
            return

        self._update_text_widget(self.ingr_result_text, "ИИ думает...")

        answer = self.gpt_service.get_recipe_by_ingredients(query)
        self._update_text_widget(self.ingr_result_text, answer)

    def _update_text_widget(self, text_widget: tk.Text, content: str):
        """Обновляет содержимое текстового виджета"""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

    def run(self):
        """Запускает главный цикл приложения"""
        self.root.eval("tk::PlaceWindow . center")
        self.root.mainloop()
