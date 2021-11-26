# Generated by Django 3.2.7 on 2021-11-24 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Tiendas', '0001_initial'),
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color_Dispositivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Marca_Dispositivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Modelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo_dispositivo', models.CharField(max_length=100)),
                ('serial', models.CharField(max_length=100)),
                ('imei_principal', models.BigIntegerField()),
                ('imei_opcional', models.BigIntegerField(blank=True, null=True)),
                ('direccion_mac', models.CharField(blank=True, max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clientes.cliente')),
                ('color_dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dispositivos.color_dispositivo')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dispositivos.marca_dispositivo')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tiendas.tienda')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dispositivos.tipo_modelo')),
            ],
        ),
    ]
