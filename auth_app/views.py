import requests
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def google_login(request):
    """Redirect user to Google's OAuth 2.0 login page."""
    params = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        "redirect_uri": settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/drive.file",
        "access_type": "offline",
        "prompt": "consent",
        }
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)

def google_callback(request):
    """Handle Google OAuth callback and return user info."""
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    # Exchange code for access token
    data = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        "redirect_uri": settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL,
        "code": code,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_info = token_response.json()

    # Check if token was received properly
    if "access_token" not in token_info:
        return JsonResponse({"error": "Failed to retrieve access token", "details": token_info}, status=400)

    access_token = token_info.get("access_token")

    # Get user information
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    user_info = user_info_response.json()

    # Return both user info and access token (for testing/demo purposes)
    response_data = {
        "user_info": user_info,
        "access_token": access_token,
    }
    return JsonResponse(response_data)

GOOGLE_DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
@csrf_exempt
def upload_file_to_drive(request):
    """Upload a file to Google Drive."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=400)

    access_token = request.headers.get("Authorization")
    print("🔹 Received Access Token:", access_token)  # Debug print

    if not access_token:
        return JsonResponse({"error": "Missing access token"}, status=401)

    if "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    uploaded_file = request.FILES["file"]
    print("🔹 File Received:", uploaded_file.name)  # Debug print

    # Prepare metadata and file content
    metadata = {
        "name": uploaded_file.name,
        "mimeType": uploaded_file.content_type,
    }

    files = {
        "metadata": (None, json.dumps(metadata), "application/json"),
        "file": (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type),
    }

    headers = {"Authorization": access_token}  # No need to add "Bearer" manually

    response = requests.post(GOOGLE_DRIVE_UPLOAD_URL, headers=headers, files=files)
    print("🔹 Google Drive API Response:", response.status_code, response.text)  # Debug print

    return JsonResponse(response.json(), status=response.status_code)


GOOGLE_DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
@csrf_exempt
def fetch_drive_files(request):
    """Fetch the list of files from Google Drive."""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=400)

    access_token = request.headers.get("Authorization")

    if not access_token:
        return JsonResponse({"error": "Missing access token"}, status=401)

    # Debug print
    print("🔹 Raw Access Token from Header:", access_token)

    # Ensure the token is correctly formatted
    if "Bearer" not in access_token:
        access_token = f"Bearer {access_token.strip()}"

    print("🔹 Corrected Access Token:", access_token)  # Debug print

    headers = {"Authorization": access_token}
    response = requests.get(GOOGLE_DRIVE_FILES_URL, headers=headers)

    print("🔹 Google Drive API Response:", response.status_code, response.text)  # Debug print

    return JsonResponse(response.json(), status=response.status_code)
 

GOOGLE_DRIVE_DOWNLOAD_URL = "https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
@csrf_exempt
def download_file_from_drive(request, file_id):
    """Download a file from Google Drive."""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=400)

    access_token = request.headers.get("Authorization")

    if not access_token:
        return JsonResponse({"error": "Missing access token"}, status=401)

    if "Bearer" not in access_token:
        access_token = f"Bearer {access_token.strip()}"

    headers = {"Authorization": access_token}
    download_url = GOOGLE_DRIVE_DOWNLOAD_URL.format(file_id=file_id)

    response = requests.get(download_url, headers=headers, stream=True)

    if response.status_code == 200:
        response_data = HttpResponse(response.content, content_type=response.headers["Content-Type"])
        response_data["Content-Disposition"] = f'attachment; filename="{file_id}.pdf"'  
        return response_data
    else:
        return JsonResponse(response.json(), status=response.status_code)
