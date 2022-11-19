from django.db import models

from category.models import Category


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    #llave foranea en relacion con la categoria y q ue elimine en cascada
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #Fecha de creacion del producto, se creara automaticamente
    create_date = models.DateTimeField(auto_now_add=True)
    # Fecha de modificacion del producto
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        # listar por nombre del roducto
        return self.product_name