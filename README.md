# Mystore - Интернет-магазин

Простой интернет-магазин на Django для продажи цифровых продуктов.

## Установка

```bash
# Виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Зависимости
pip install -r requirements.txt

# База данных
python manage.py migrate

# Запуск
python manage.py runserver
```

## Доступные страницы
Перед переходом на данные ссылки необходимо запустить сервер с помощью команды Запуска - см. выше в блоке "Установка".
- Главная: http://127.0.0.1:8000/
- Контакты: http://127.0.0.1:8000/contacts/

## Функции
- Главная страница с товарами
- Страница контактов с формой
- Обработка формы обратной связи
- Адаптивный дизайн (Bootstrap)

## Технологии
- Django 6.0.1
- Python 3.8+
- Bootstrap 5
- SQLite3