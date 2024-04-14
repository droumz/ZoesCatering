from django.contrib import admin
from .models import Category, Size, Product, ProductAttribute, ContactMessage

admin.site.register(Category)
admin.site.register(Size)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','status')
    list_editable = ('status',)


admin.site.register(Product,ProductAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id','product','price','size')


admin.site.register(ProductAttribute,ProductAttributeAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'timestamp']


admin.site.register(ContactMessage, ContactMessageAdmin)
