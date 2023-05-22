from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db.models import Case, When, Value, IntegerField
import json

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .modules import main
from .modules.specification_parser import SpecificationParser
from .models import Collection, Scan, ScanDetail


def home(request):
    user = request.user
    is_loggedin = user.is_authenticated

    severity_counts = {
        'All': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0,
        'Info': 0,
    }

    if is_loggedin:
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
        'severity_counts': severity_counts,
        'chart_data': chart_data,
    }
    return render(request, 'app/dashboard.html', context)


def collections(request):
    user = request.user
    is_loggedin = user.is_authenticated

    if is_loggedin:
        collections = user.collection_set.all()
    else:
        collections = Collection.objects.all()

    context = {'collections': collections}
    return render(request, 'app/collections.html', context)


def createCollection(request):
    if request.method == 'POST':
        user = request.user
        is_loggedin = user.is_authenticated

        uploaded_file = request.FILES['collection-file']
        file_name = uploaded_file.name

        if is_loggedin:
            collection = Collection(
                title=file_name, file=uploaded_file, owner=user
            )
        else:
            collection = Collection(title=file_name, file=uploaded_file)

        collection.save()
        return redirect('collections')

    return render(request, 'app/create-collection.html')


def viewCollection(request, pk):
    user = request.user
    is_loggedin = user.is_authenticated

    try:
        if is_loggedin:
            collection = Collection.objects.filter(owner=user).get(id=pk)
        else:
            collection = Collection.objects.filter(owner__isnull=True).get(
                id=pk
            )
    except Exception:
        return render(request, 'error.html')

    spec_file_path = collection.file.path

    sp = SpecificationParser(spec_file_path)

    openapi_spec = sp.parse()

    openapi_spec_json = json.dumps(openapi_spec)
    context = {"spec": openapi_spec_json}
    return render(request, 'view-collection.html', context)


def deleteCollection(request, pk):
    if request.method == 'DELETE':
        user = request.user
        is_loggedin = user.is_authenticated

        try:
            if is_loggedin:
                collection = Collection.objects.filter(owner=user).get(id=pk)
            else:
                collection = Collection.objects.filter(owner__isnull=True).get(
                    id=pk
                )
        except Exception:
            return render(request, 'error.html')

        collection.delete()

        return HttpResponse('Success', status=200)


def newScan(request):
    user = request.user
    is_loggedin = user.is_authenticated

    if request.method == 'POST':
        coll = request.POST['collection']
        coll_id, coll_title = coll.split(':')
        collection = Collection.objects.get(id=coll_id)
        spec_file_path = collection.file.path

        scan_type = request.POST['scantype']
        auth_type = request.POST['authtype']
        auth_detail = request.POST['authdetail']
        if auth_type == "None":
            auth_detail = False

        if is_loggedin:
            scan = Scan.objects.create(
                user=user,
                scan_type=scan_type,
                coll_title=coll_title,
                auth_type=auth_type,
                auth_detail=auth_detail,
            )
        else:
            scan = Scan.objects.create(
                scan_type=scan_type,
                coll_title=coll_title,
                auth_type=auth_type,
                auth_detail=auth_detail,
            )

        try:
            main.runTests(spec_file_path, scan)
        except Exception:
            scan.status = 'FAILED'
            scan.save()
            return redirect('scans')

        scan.status = 'COMPLETED'
        scan.save()

        return redirect('scans')

    if is_loggedin:
        collections = user.collection_set.all()
    else:
        collections = Collection.objects.all()

    context = {"collections": collections}
    return render(request, 'app/new-scan.html', context)


def scans(request):
    user = request.user
    is_loggedin = user.is_authenticated

    if is_loggedin:
        scans = Scan.objects.filter(user=user).order_by('-scan_date')
    else:
        scans = Scan.objects.filter(user__isnull=True).order_by('-scan_date')

    context = {"scans": scans}
    return render(request, 'app/scans.html', context)


def singleScan(request, pk):
    user = request.user
    is_loggedin = user.is_authenticated

    try:
        if is_loggedin:
            scan = Scan.objects.filter(user=user).get(id=pk)
        else:
            scan = Scan.objects.filter(user__isnull=True).get(id=pk)
    except Exception:
        return render(request, 'error.html')

    severity_ordering = Case(
        When(vulnerability__severity='High', then=Value(1)),
        When(vulnerability__severity='Medium', then=Value(2)),
        When(vulnerability__severity='Low', then=Value(3)),
        When(vulnerability__severity='Informational', then=Value(4)),
        default=Value(5),
        output_field=IntegerField(),
    )
    scan_details = scan.scandetail_set.select_related('vulnerability').order_by(
        severity_ordering
    )

    context = {'scan_details': scan_details, 'last_scan_id': scan.id}
    return render(request, 'app/single-scan.html', context)


def singleScanVuln(request, pk, pk2):
    user = request.user
    is_loggedin = user.is_authenticated

    try:
        if is_loggedin:
            scan = Scan.objects.filter(user=user).get(id=pk)
        else:
            scan = Scan.objects.filter(user__isnull=True).get(id=pk)
    except Exception:
        return render(request, 'error.html')

    scan_detail = scan.scandetail_set.select_related('vulnerability').get(
        id=pk2
    )

    context = {'scan_detail': scan_detail, "scan_id": pk}
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
