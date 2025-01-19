from django.shortcuts import render
from .models import General


def general_page(request):
    """Рендер главной страницы"""
    general_obj = General.objects.first()

    # Доступ к default
    default_vac_pic= General._meta.get_field('vac_pic').default
    default_vac_text = General._meta.get_field('vac_text').default

    content = {
        'vac_pic': general_obj.vac_pic.url if general_obj and general_obj.vac_pic else '/media'+default_vac_pic,
        'vac_text': general_obj.vac_text if general_obj else default_vac_text,
    }
    return render(request, 'general_page.html', content)
