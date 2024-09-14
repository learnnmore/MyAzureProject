# uploader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_upload, name='document_upload'),  # Upload page
    path    ('document/download/<str:document_reference>/', views.document_download, name='document_download'),
    # other URL patterns
]
