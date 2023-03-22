from django.shortcuts import render


def home(request):
    context = {'n': 5}

    return render(request, 'app/home.html', context)
