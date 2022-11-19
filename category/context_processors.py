from category.models import Category

#Esta funcion debo registrarla en el proyecto principal
#en settings.py - TEMPLATES - OPTIONS
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)