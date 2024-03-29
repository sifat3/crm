# Generated by Django 4.2.7 on 2023-11-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_token_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completed_project',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='ongoing_project',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='bill',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='first_payment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='profit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='second_payment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ongoing_project',
            name='third_payment',
            field=models.IntegerField(default=0),
        ),
    ]
