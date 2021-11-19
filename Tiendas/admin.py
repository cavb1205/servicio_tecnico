from django.contrib import admin
from Tiendas.models import Tienda, Moneda, Ciudad

# Register your models here.
admin.site.register(Tienda)
admin.site.register(Ciudad)
admin.site.register(Moneda)
