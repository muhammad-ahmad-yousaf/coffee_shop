from django.shortcuts import render
from .models import MenuItem



def menu_list(request):
    category = request.GET.get("category")
    if category:
        items = MenuItem.objects.filter(category=category)
    else:
        items = MenuItem.objects.all()
    return render(request, "menu/menu_list.html", {"items": items})
