# Generated by Django 4.2.7 on 2023-11-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_token_options_alter_token_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='completed_project',
            name='freelancer_email',
            field=models.EmailField(default='nothing@nothing.com', max_length=254),
        ),
    ]