from django.db import models
from django.urls import reverse
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def get_url(self):
        # esta funcion lo que hace es a la url del store, agregar el slug
        #http://127.0.0.1:8000/store/category_slug
        return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.category_name
