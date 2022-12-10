# Generated by Django 4.1.2 on 2022-11-11 04:59

import colorfield.fields
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_alter_banner_options_alter_banner_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='background_color',
            field=colorfield.fields.ColorField(blank=True, default='#f9f8f9', help_text='Выберите цвет, если указан тип - Текст', image_field=None, max_length=18, null=True, samples=None, verbose_name='Цвет фона'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='description',
            field=models.TextField(blank=True, help_text='Обязательно если выбран тип Изображение + текст или Текст', null=True, verbose_name='Подробности'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Обязательно если указан тип Изображение + текст или Изображение', null=True, upload_to='banners', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='is_view',
            field=models.BooleanField(default=True, verbose_name='Отображать в слайдере?'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.URLField(blank=True, help_text='Укажите ссылку, если необходимо, в банере появится кнопка подробнее', null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(blank=True, help_text='Обязательно если выбран тип Изображение + текст или Текст', max_length=256, null=True, verbose_name='Заголовок'),
        ),
    ]
