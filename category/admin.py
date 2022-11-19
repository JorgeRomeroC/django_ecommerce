from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    # quiere que se genere automaticamente el slug, con la propiedad category_name
    prepopulated_fields = {'slug':('category_name',)}
    # En el grid de la tabla quiero mostar el nombre de la categoria y el slug
    list_display = ('category_name','slug')

admin.site.register(Category, CategoryAdmin)
