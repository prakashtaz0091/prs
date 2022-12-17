from django.contrib import admin
from home.models import Contact, Product, ScrappedProduct,Search


# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)

admin.site.register(ScrappedProduct)
admin.site.register(Search)