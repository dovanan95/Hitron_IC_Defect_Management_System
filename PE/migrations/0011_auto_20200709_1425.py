# Generated by Django 3.0.6 on 2020-07-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PE', '0010_auto_20200709_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterdata',
            name='Change_date',
            field=models.DateField(),
        ),
    ]
