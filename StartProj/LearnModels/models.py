from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    obj = models.Manager()

    class Meta:
        db_table = 'Category'
        ordering = ('id',)
        verbose_name = db_table


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete='CASCADE')
    title = models.CharField(max_length=70)
    description = models.TextField()
    in_stock = models.BooleanField()
    obj = models.manager.Manager()

    def __str__(self):
        return ('id: ' + str(self.id) + '<br>'
         + 'title: ' + str(self.title) + '<br>'
         + 'description: ' + str(self.description) + '<br>'
         + 'in stock: ' + str(self.in_stock) + '<br><br>')

    class Meta:
        db_table = 'Product'
        ordering = ('-id',)
        verbose_name = db_table
