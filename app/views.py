from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
import json

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .modules import main
from .modules.specification_parser import SpecificationParser
from .models import Collection, Scan, ScanDetail


def home(request):
    user = request.user

    loggedin = True
    if str(user) == "AnonymousUser":
        loggedin = False

    if loggedin:
        scan = Scan.objects.get(user=user)

        severity_counts = {'High': 0, 'Medium': 0, 'Low': 0, 'Info': 0}

        count_info = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Info"
        ).count()
        severity_counts["Info"] = count_info

        count_low = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Low"
        ).count()
        severity_counts["Low"] = count_low

        count_medium = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Medium"
        ).count()
        severity_counts["Medium"] = count_medium

        count_high = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="High"
        ).count()
        severity_counts["High"] = count_high

    context = {
        'loggedin': loggedin,
        'severity_counts': severity_counts,
    }
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


def newScan(request):
    user = request.user
    if request.method == 'POST':
        collection_id = request.POST['collection']
        collection = Collection.objects.get(id=collection_id)
        spec_file_path = collection.file.path

        if str(user) == "AnonymousUser":
            scan = Scan.objects.create()
        else:
            scan = Scan.objects.create(user=user)

        main.runTests(spec_file_path, 'openapi', scan.id)

        return redirect('single-scan', scan.id)

    if str(user) == "AnonymousUser":
        collections = Collection.objects.all()
    else:
        collections = user.collection_set.all()

    context = {"collections": collections}
    return render(request, 'app/new-scan.html', context)


def scans(request):
    return render(request, 'app/single-scan.html')


def singleScan(request, pk):
    user = request.user

    last_scan = Scan.objects.filter(user=user).latest('id')

    scan_details = last_scan.scandetail_set.select_related('vulnerability')

    context = {'scan_details': scan_details, 'last_scan_id': last_scan.id}
    return render(request, 'app/single-scan.html', context)


def singleScanVuln(request, pk, pk2):
    return render(request, 'app/single-scan-vuln.html')


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
