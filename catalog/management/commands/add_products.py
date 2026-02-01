from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Все товары и категории удалены"))

        categories = [
            {'name': 'phones', 'description': 'Мобильные телефоны'},
            {'name': 'earbuds', 'description': 'Наушники'}
        ]
        created_categories = []
        for category_data in categories:
            category, created = Category.objects.get_or_create(**category_data)
            created_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Категория успешно добавлена: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Категория уже существует: {category.name}"))


        products =[
            {'title': 'Xiaomi ultra mega x5000',
             'description': '8 Тб, 5000 Mpx',
             'category': created_categories[0],
             'price': 90000.00},
            {'title': 'iphone_17',
             'description': '512 Гб',
             'category': created_categories[0],
             'price': 80000.00},
            {'title': 'iPhone 17 Pro Max',
             'description': '512 Гб, титановый корпус, процессор A19',
             'category': created_categories[0],
             'price': 109999.00},
            {'title': 'Apple AirPods Pro 3',
             'description': 'Адаптивный звук, шумоподавление, 30ч работы',
             'category': created_categories[1],
             'price': 19590.00},
            {'title': 'Samsung Galaxy Buds 3 Pro',
             'description': 'ИИ-шумоподавление, открытый дизайн',
             'category': created_categories[1],
             'price': 10999.00}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Товар успешно добавлен: {product.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Товар уже существует: {product.title}"))