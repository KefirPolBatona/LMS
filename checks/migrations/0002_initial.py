# Generated by Django 4.2.16 on 2024-11-11 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materials', '0001_initial'),
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='materials.lesson', verbose_name='Урок'),
        ),
    ]
