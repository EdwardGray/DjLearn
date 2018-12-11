from django import forms
from .models import Product, Category
from taggit.forms import TagField

TITLE_ERROR_LIST = {'required': 'Укажите название товара',
                    'max_length': 'Слишком длинное название'}


class ProductAddForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.obj.all(), label='Категория')
    title = forms.CharField(label='Название', error_messages=TITLE_ERROR_LIST)
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    in_stock = forms.BooleanField(initial=True, label='В наличии', required=False)
    thumbnail = forms.ImageField(label='Миниатюра', error_messages={'required': 'Укажите файл изображения'})
    tags = TagField(label='Теги')

    class Meta:
        model = Product
        exclude = ('thumbnail_with', 'thumbnail_height')
        # fields = '__all__'


class ProductEditForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.obj.all(), label='Категория')
    title = forms.CharField(label='Название', error_messages=TITLE_ERROR_LIST)
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    in_stock = forms.BooleanField(initial=True, label='В наличии', required=False)
    thumbnail = forms.ImageField(label='Миниатюра', error_messages={'required': 'Укажите файл изображения'})
    tags = TagField(label='Теги')

    class Meta:
        model = Product
        exclude = ('thumbnail_with', 'thumbnail_height')


# class ProductThumbAddFrom(forms.ModelForm):
#
#     thumbnail = forms.ImageField(label='Миниатюра', error_messages={'required': 'Укажите файл изображения'})
#
#     class Meta:
#         model = ProductThumbnail
#         fields = ('product', 'thumbnail')
