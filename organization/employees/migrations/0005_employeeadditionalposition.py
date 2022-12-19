# Generated by Django 4.1.2 on 2022-12-19 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_alter_city_options'),
        ('employees', '0004_employee_city_alter_employee_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAdditionalPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='additional_employees', to='organization.department', verbose_name='Департамент')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_positions', to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='employees.position')),
            ],
        ),
    ]
