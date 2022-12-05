from .models import AppInfo, Category

def appdetail(request):
    info = AppInfo.objects.get(pk=1)
    meal = Category.objects.all()

    context = {
        'info':info,
        'meal':meal
    }

    return context