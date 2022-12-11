# Generated by Django 4.1.2 on 2022-12-10 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import filer.fields.image
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0015_alter_file_owner_alter_file_polymorphic_ctype_and_more'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('author', models.CharField(blank=True, max_length=200, null=True, verbose_name='Автор')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание')),
                ('cover', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Обложка')),
                ('file', filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, related_name='book_file', to='filer.file', verbose_name='Файл книги')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['name'],
            },
        ),
    ]