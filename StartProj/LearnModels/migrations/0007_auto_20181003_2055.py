# Generated by Django 2.1.1 on 2018-10-03 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LearnModels', '0006_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-id',), 'verbose_name': 'Product'},
        ),
    ]