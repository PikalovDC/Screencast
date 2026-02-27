from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    FORBIDDEN_WORDS = [
        'казино',
        'криптовалюта',
        'крипта',
        'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'category', 'price']
        labels = {
            'title': 'Название товара',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена ($)'
        }

    def __init__(self, *args, **kwargs):
        """CSS классы для стилизации"""
        super().__init__(*args, **kwargs)

        # Класс form-control для всех полей
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Плейсхолдеры
            if field_name == 'title':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
                field.widget.attrs['min'] = '0'
                field.widget.attrs['step'] = '0.01'

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError('Пожалуйста, укажите цену товара')

        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')

        if price == 0:
            raise forms.ValidationError('Цена должна быть больше нуля')

        if price > 999999.99:
            raise forms.ValidationError('Цена не может превышать 999,999.99')

            # Округляем до двух знаков после запятой
        price = round(price, 2)

        return price

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            forbidden_found = self._check_forbidden_words(title)
            if forbidden_found:
                raise forms.ValidationError(f'Название содержит запрещенные слова: {", ".join(forbidden_found)}')

        return title

    def clean_description(self):
        """Валидация поля description"""
        description = self.cleaned_data.get('description')
        if description:
            # Проверяем наличие запрещенных слов
            forbidden_found = self._check_forbidden_words(description)
            if forbidden_found:
                raise forms.ValidationError(
                    f'Описание содержит запрещенные слова: {", ".join(forbidden_found)}'
                )
        return description


    def _check_forbidden_words(self, text):
        text_lower = text.lower()
        found_words = []

        for word in self.FORBIDDEN_WORDS:
            if word in text_lower:
                found_words.append(word)

        return found_words


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        # Дополнительная проверка на спам в обоих полях одновременно
        if title and description:
            # Проверяем, не совпадают ли title и description
            if title.lower() == description.lower():
                raise forms.ValidationError(
                    'Название и описание не должны совпадать'
                )

        return cleaned_data