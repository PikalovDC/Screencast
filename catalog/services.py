from .models import Product


class ProductService:
    """Сервис для работы с продуктами"""

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список всех продуктов в указанной категории"""
        return Product.objects.filter(category_id=category_id, is_published=True)