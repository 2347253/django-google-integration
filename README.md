# Django Google Integration

This is a Django-based backend project that integrates:
- **Google OAuth 2.0** for authentication.
- **Google Drive API** for file uploads and retrieval.
- **WebSockets** for real-time chat.

## Features
- **Google Authentication Flow**
  - Initiates Google OAuth 2.0 login.
  - Handles the callback and returns authentication data.
- **Google Drive Integration**
  - Allows users to connect their Google Drive.
  - Supports file uploads and downloads.
- **WebSocket Chat**
  - Enables real-time messaging between users.

---

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/django-google-integration.git
cd django-google-integration
```
### 2️⃣ Create & Activate Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```


### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 4️⃣ Set Up Environment Variables
Create a .env file in the root directory and add:

```ini
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/google/callback/
```
###5️⃣ Run Migrations
```sh

python manage.py migrate
```
### 6️⃣ Run Django Development Server
```sh

python manage.py runserver
```
