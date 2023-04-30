from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
import json

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .modules import main
from .modules.specification_parser import SpecificationParser
from .models import Collection


def home(request):
    user = request.user

    if str(user) == "AnonymousUser":
        loggedin = False
    else:
        loggedin = True

    context = {'loggedin': loggedin}
    return render(request, 'app/dashboard.html', context)


def collections(request):
    user = request.user
    if str(user) == "AnonymousUser":
        collections = Collection.objects.all()
    else:
        collections = user.collection_set.all()

    context = {'collections': collections}
    return render(request, 'app/collections.html', context)


def createCollection(request):
    if request.method == 'POST':
        user = request.user

        uploaded_file = request.FILES['collection-file']
        file_name = uploaded_file.name

        if str(user) == "AnonymousUser":
            collection = Collection(title=file_name, file=uploaded_file)
        else:
            collection = Collection(
                title=file_name, file=uploaded_file, owner=user
            )

        collection.save()
        return redirect('collections')

    return render(request, 'app/create-collection.html')


def viewCollection(request, pk):
    collection = Collection.objects.get(id=pk)
    spec_file_path = collection.file.path

    sp = SpecificationParser(spec_file_path, 'openapi')

    openapi_spec = sp.parse()

    openapi_spec_json = json.dumps(openapi_spec)
    context = {"spec": openapi_spec_json}
    return render(request, 'view-collection.html', context)


def deleteCollection(request, pk):
    if request.method == 'DELETE':
        collection = Collection.objects.get(id=pk)
        collection.delete()

        return HttpResponse('Success', status=200)


def scans(request):
    if request.method == 'POST':
        collection_id = request.POST['collection']
        collection = Collection.objects.get(id=collection_id)
        spec_file_path = collection.file.path

        res = main.runTests(spec_file_path, 'openapi')

        print(res)
        return redirect('home')

    user = request.user
    if str(user) == "AnonymousUser":
        collections = Collection.objects.all()
    else:
        collections = user.collection_set.all()

    context = {"collections": collections}
    return render(request, 'app/scans.html', context)


def vulnerabilities(request):
    return render(request, 'app/vulnerabilities.html')


def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def loginUser(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
