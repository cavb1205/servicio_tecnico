from django.contrib import admin
from Tiendas.models import Membresia, Tienda, Moneda, Ciudad, Tienda_membresia

# Register your models here.
admin.site.register(Tienda)
admin.site.register(Ciudad)
admin.site.register(Moneda)
admin.site.register(Membresia)
admin.site.register(Tienda_membresia)