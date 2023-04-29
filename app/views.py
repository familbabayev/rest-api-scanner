from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from .modules import main
from .modules.specification_parser import SpecificationParser
from .models import Collection


def home(request):
    context = {}
    return render(request, 'app/dashboard.html', context)


def collections(request):
    collections = Collection.objects.all()
    context = {'collections': collections}

    return render(request, 'app/collections.html', context)


def createCollection(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['collection-file']
        file_name = uploaded_file.name

        collection = Collection(title=file_name, file=uploaded_file)
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

    api_collections = Collection.objects.all()

    context = {"collections": api_collections}
    return render(request, 'app/scans.html', context)
    # return render(request, 'mainKit.html')


def vulnerabilities(request):
    return render(request, 'app/vulnerabilities.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')
