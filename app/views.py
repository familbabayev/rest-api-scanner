from django.shortcuts import render, redirect


def home(request):
    context = {'n': 5}
    if request.method == 'POST':
        url = request.POST['url']
        print(url)

        return redirect('home')

    return render(request, 'app/home.html', context)
