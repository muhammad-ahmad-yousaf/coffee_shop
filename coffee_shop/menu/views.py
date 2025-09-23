from django.shortcuts import render
from .models import MenuItem
from django.views import View

class MenuListView(View):
    def get(self, request):
        category = request.GET.get("category")
        if category:
            items = MenuItem.objects.filter(category=category)
        else:
            items = MenuItem.objects.all()
        return render(request, "menu/menu_list.html", {"items": items})
