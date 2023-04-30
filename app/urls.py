from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('collections/', views.collections, name="collections"),
    path(
        'collections/create', views.createCollection, name="create-collection"
    ),
    path('collections/<str:pk>/', views.viewCollection, name="view-collection"),
    path(
        'collections/<int:pk>/delete/',
        views.deleteCollection,
        name="delete-collection",
    ),
    path('scans/', views.scans, name="scans"),
    path('vulnerabilities/', views.vulnerabilities, name="vulnerabilities"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
]
