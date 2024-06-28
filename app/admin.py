from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'contact_no', 'organization_name', 'address']

admin.site.register(CustomUser)

admin.site.register(Customer)    
admin.site.register(Quality)
admin.site.register(Point)
admin.site.register(Brand)

class BundleInline(admin.TabularInline):
    model = Bundle
    extra = 1
    fields = [ 'status','bill_no','bundle', 'grade', 'sizes', 'sheet', 'weight', 'remarks']  # Include Bundle fields

class SelectedInline(admin.TabularInline):
    model = Selected
    extra = 1
    fields = ['name', 'bill_no', 'date']  # Include Selected fields

class PackingAdmin(admin.ModelAdmin):
    list_display = ['date_packing','name', 'lot_no', 'quality', 'point', 'brand', 'lot_kgs']
    inlines = [BundleInline, SelectedInline]

admin.site.register(Packing, PackingAdmin)


admin.site.register(packing_slip_new)
