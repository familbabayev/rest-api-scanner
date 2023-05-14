from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('collections/', views.collections, name="collections"),
    path(
        'collections/create', views.createCollection, name="create-collection"
    ),
    path('collections/<int:pk>/', views.viewCollection, name="view-collection"),
    path(
        'collections/<int:pk>/delete/',
        views.deleteCollection,
        name="delete-collection",
    ),
    path('scans/new-scan', views.newScan, name="new-scan"),
    path('scans/', views.scans, name="scans"),
    path('scans/<int:pk>/', views.singleScan, name="single-scan"),
    path(
        'scans/<int:pk>/vulnerability/<int:pk2>',
        views.singleScanVuln,
        name="single-scan-vuln",
    ),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
]
