from django.contrib import admin
from .models import CustomerDeletedRecords, CustomerRecords
# Register your models here.
admin.site.register(CustomerRecords)
admin.site.register(CustomerDeletedRecords)