from django.urls import path
from .views import google_login, google_callback, upload_file_to_drive,fetch_drive_files,download_file_from_drive

urlpatterns = [
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("google/upload/", upload_file_to_drive, name="google_upload"),
    path("google/files/", fetch_drive_files, name="google_files"),
    path("google/download/<str:file_id>/", download_file_from_drive, name="google_download"),

]
