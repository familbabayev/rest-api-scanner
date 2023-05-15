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

    severity_counts = {
        'All': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0,
        'Info': 0,
    }

    if loggedin:
        scans = Scan.objects.filter(user=user)
    else:
        scans = Scan.objects.filter(user__isnull=True)

    for scan in scans:
        count_info = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Info"
        ).count()
        severity_counts["Info"] += count_info

        count_low = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Low"
        ).count()
        severity_counts["Low"] += count_low

        count_medium = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="Medium"
        ).count()
        severity_counts["Medium"] += count_medium

        count_high = ScanDetail.objects.filter(
            scan=scan, vulnerability__severity="High"
        ).count()
        severity_counts["High"] += count_high

        severity_counts["All"] = (
            severity_counts["Info"]
            + severity_counts["Low"]
            + severity_counts["Medium"]
            + severity_counts["High"]
        )

    chart_data = [
        severity_counts["High"],
        severity_counts["Medium"],
        severity_counts["Low"],
        severity_counts["Info"],
    ]

    context = {
        'loggedin': loggedin,
        'severity_counts': severity_counts,
        'chart_data': chart_data,
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


import time


def newScan(request):
    user = request.user
    if request.method == 'POST':
        coll = request.POST['collection']
        coll_id, coll_title = coll.split('_')
        collection = Collection.objects.get(id=coll_id)
        spec_file_path = collection.file.path

        scan_type = request.POST['scantype']

        if str(user) == "AnonymousUser":
            scan = Scan.objects.create(
                scan_type=scan_type, coll_title=coll_title
            )
        else:
            scan = Scan.objects.create(
                user=user, scan_type=scan_type, coll_title=coll_title
            )

        time.sleep(5)
        main.runTests(spec_file_path, 'openapi', scan.id)

        scan.finished = True
        scan.save()

        return redirect('single-scan', scan.id)

    if str(user) == "AnonymousUser":
        collections = Collection.objects.all()
    else:
        collections = user.collection_set.all()

    context = {"collections": collections}
    return render(request, 'app/new-scan.html', context)


def scans(request):
    user = request.user

    if str(user) == "AnonymousUser":
        scans = Scan.objects.filter(user__isnull=True).order_by('-scan_date')
    else:
        scans = Scan.objects.filter(user=user).order_by('-scan_date')

    context = {"scans": scans}
    return render(request, 'app/scans.html', context)


def singleScan(request, pk):
    user = request.user

    try:
        if str(user) == "AnonymousUser":
            scan = Scan.objects.filter(user__isnull=True).get(id=pk)
        else:
            scan = Scan.objects.filter(user=user).get(id=pk)
    except Exception:
        return render(request, 'error.html')

    scan_details = scan.scandetail_set.select_related('vulnerability')

    context = {'scan_details': scan_details, 'last_scan_id': scan.id}
    return render(request, 'app/single-scan.html', context)


def singleScanVuln(request, pk, pk2):
    user = request.user
    try:
        if str(user) == "AnonymousUser":
            scan = Scan.objects.filter(user__isnull=True).get(id=pk)
        else:
            scan = Scan.objects.filter(user=user).get(id=pk)
    except Exception:
        return render(request, 'error.html')

    scan_detail = scan.scandetail_set.select_related('vulnerability').get(
        id=pk2
    )
    print(scan_detail)
    context = {'scan_detail': scan_detail}
    return render(request, 'app/single-scan-vuln.html', context)


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
