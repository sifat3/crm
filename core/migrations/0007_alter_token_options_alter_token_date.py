# Generated by Django 4.2.7 on 2023-11-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_token_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='token',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
