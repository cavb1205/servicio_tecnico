# Generated by Django 3.2.7 on 2021-11-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendas', '0002_alter_tienda_ciudad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membresia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Gratis', 'Gratis'), ('Mensual', 'Mensual'), ('Anual', 'Anual')], max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]