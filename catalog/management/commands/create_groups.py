from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **kwargs):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем нужные разрешения
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_unpublish_product', 'delete_product']
        )

        # Назначаем разрешения группе
        for perm in permissions:
            moderator_group.permissions.add(perm)
            self.stdout.write(f'Добавлено разрешение: {perm.codename}')

        self.stdout.write(self.style.SUCCESS('Настройка группы завершена'))