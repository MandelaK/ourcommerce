# Generated by Django 2.2.2 on 2019-08-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttag',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]
