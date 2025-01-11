from django.shortcuts import render


def general_page(request):
    return render(request, 'general.html')
