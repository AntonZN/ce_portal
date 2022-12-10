# Generated by Django 4.1.2 on 2022-10-29 01:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('taggit', '0005_auto_20220424_2025'),
        ('employees', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.department', verbose_name='Департамент'),
        ),
        migrations.AddField(
            model_name='employee',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='employee',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, help_text='Если у сотрудника нет руководителя, оставьте поле пустым', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisor', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.position', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='employee',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
