from django.db import models
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    obj = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


# CHOICES = ((category.id, category.title) for category in Category.obj.all())


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete='CASCADE',
                                 verbose_name='Категория')
    title = models.CharField(max_length=70, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    in_stock = models.BooleanField(verbose_name='В наличии')

    thumbnail_with = models.PositiveIntegerField()
    thumbnail_height = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to='products/thumbnails',
                                  width_field='thumbnail_with', height_field='thumbnail_height')

    tags = TaggableManager(blank=True, verbose_name='Теги')

    obj = models.Manager()

    class Meta:
        db_table = 'Product '
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('title',)


# class ProductThumbnail(models.Model):
#     product = models.ForeignKey(Product, on_delete='CASCADE',
#                                 verbose_name='Продукт')
#     thumbnail_with = models.PositiveSmallIntegerField()
#     thumbnail_height = models.PositiveSmallIntegerField()
#     thumbnail = models.ImageField(upload_to='products/thumbnails',
#                                   width_field=thumbnail_with, height_field=thumbnail_height)
#
#     obj = models.Manager()
#
#     class Meta:
#         db_table = 'ProductThumbnail'
#         verbose_name = 'Миниатюра'
#         verbose_name_plural = 'Миниатюры'
