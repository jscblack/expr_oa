# Generated by Django 3.2.4 on 2021-06-26 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oa', '0005_auto_20210626_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusers',
            name='PersonDirectSuperior',
            field=models.IntegerField(verbose_name='self'),
        ),
    ]
