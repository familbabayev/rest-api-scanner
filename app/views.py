from django.shortcuts import render, redirect
from django.conf import settings
import os, json

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

    spec_file_path = os.getcwd() + settings.MEDIA_URL + str(collection.file)
    sp = SpecificationParser(spec_file_path, 'openapi')
    # print(spec_file_path)
    openapi_spec = sp.parse()

    openapi_spec_json = json.dumps(openapi_spec)
    context = {"spec": openapi_spec_json}
    return render(request, 'view-collection.html', context)


def scans(request):
    if request.method == 'POST':
        collection = Collection.objects.get(id=7)

        spec_file_path = os.getcwd() + settings.MEDIA_URL + str(collection.file)
        res = main.runTests(spec_file_path, 'openapi')

        print(res)
        return redirect('home')

    return render(request, 'app/scans.html')


def vulnerabilities(request):
    return render(request, 'app/vulnerabilities.html')
