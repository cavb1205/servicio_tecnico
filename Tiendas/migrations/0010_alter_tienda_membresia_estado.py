# Generated by Django 3.2.7 on 2021-12-14 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendas', '0009_alter_tienda_membresia_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda_membresia',
            name='estado',
            field=models.CharField(choices=[('Activa', 'Activa'), ('Vencida', 'Vencida'), ('Pendiente Pago', 'Pendiente Pago')], default=True, max_length=50),
        ),
    ]
