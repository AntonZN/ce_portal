# Generated by Django 4.1.2 on 2022-12-22 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_formproxy_questionsproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
