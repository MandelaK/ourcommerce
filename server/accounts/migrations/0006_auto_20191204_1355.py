# Generated by Django 2.2.4 on 2019-12-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_auto_20191204_1340"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
