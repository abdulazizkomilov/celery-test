from django.urls import path
from .views import ManagerCreateView, ManagerExportCSVView

urlpatterns = [
    path('managers/create/', ManagerCreateView.as_view(), name='create-manager'),
    path('managers/export/', ManagerExportCSVView.as_view(), name='export-managers'),
]
