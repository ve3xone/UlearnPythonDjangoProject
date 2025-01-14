from django.shortcuts import render


def general_page(request):
    return render(request, 'general_page.html')
    # Проверка, AJAX-запрос это или нет
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     # Возвращаем только контент для AJAX
    #     return render(request, 'general_partial.html')
    # else:
    #     # Возвращаем полный шаблон
    #     return render(request, 'general_page.html')
