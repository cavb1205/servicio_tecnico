# Generated by Django 3.2.7 on 2021-10-03 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='estado_cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Clientes.estado_cliente'),
        ),
    ]
