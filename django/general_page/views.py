from django.shortcuts import render


def general_page(request):
    """Рендер главной страницы"""
    return render(request, 'general_page.html')
