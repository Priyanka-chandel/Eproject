from django.contrib import admin
from Eapp.models import Orders
from Eapp.models import OrderUpdate
from Eapp.models import ContactMessage


# Register your models here.
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(ContactMessage)