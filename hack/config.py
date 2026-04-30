# ================= GRID & RISK CONFIG =================
GRID_SIZE = 6
CRITICAL_THRESHOLD = 4
RISK_LIMIT = 5
MAX_PEOPLE_PER_GRID = 3


# ================= MULTI-CAMERA CONFIG =================
CAMERAS = [
    {
        "id": "Cam1",
        "src": 0,  # Laptop webcam
        "loc": "Entrance"
    },
    {
        "id": "Cam2",
        "src": "http://192.168.168.149:8080/video",  # Mobile 1
        "loc": "Left Zone"
    },
    {
        "id": "Cam3",
        "src": "http://192.168.168.12:8080/video",  # Mobile 2
        "loc": "Center Zone"
    }
]


# ================= DATABASE =================
DB_NAME = "users.db"


# ================= SECURITY =================
SECRET_KEY = "super-secret-hackathon-key"


# ================= SMS (OPTIONAL) =================
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUM = ""
NOTIFICATION_NUMBER = "917709555439" # WhatsApp destination