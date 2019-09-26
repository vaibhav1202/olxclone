from django.contrib import admin
from clone.models import seller
# Register your models here.
class sellerAdmin(admin.ModelAdmin):
    list_display = ["item_name","s_name" , "s_pn", "s_email","s_description","s_img","s_price","s_years","s_area"]
    list_filter = ["item_name","s_years","s_price","s_area"]
    search_fields = ["item_name","s_years","s_price","s_area"]
admin.site.register(seller,sellerAdmin)