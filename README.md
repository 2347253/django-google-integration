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
### 5️⃣ Run Migrations
```sh

python manage.py migrate
```
### 6️⃣ Run Django Development Server
```sh

python manage.py runserver
```
## 📌 API Endpoints

### 🔹 Google Authentication
| Method | Endpoint | Description |
|--------|----------|------------|
| GET | `/auth/google/login/` | Initiates Google login |
| GET | `/auth/google/callback/` | Handles OAuth callback |

### 🔹 Google Drive
| Method | Endpoint | Description |
|--------|----------|------------|
| GET | `/auth/google/drive/list/` | Fetches user’s Google Drive files |
| POST | `/auth/google/drive/upload/` | Uploads a file to Google Drive |
| GET | `/auth/google/download/<file_id>/` | Downloads a file from Google Drive |

### 🔹 WebSocket (Real-time Chat)
**Steps to Test WebSocket:**
1. Open a WebSocket client like [Postman](https://www.postman.com/) or [wss.io](https://www.piesocket.com/websocket-tester).
2. Connect to `ws://127.0.0.1:8001/ws/chat/`.
3. Send a message in JSON format:
   ```json
   {
     "username": "Alice",
     "message": "Hello, world!"
   }
   ```
4. Receive a real-time response.

---

## 🚀 Deployment
This project is hosted on **Render**.


## 📌 Postman Collection
- Import the **Postman collection** from [Postman Link](#).
- Ensure your `.env` is set up before testing.

---

## 💜 License
This project is for **assessment purposes only** for Hrenfund.io.

---

