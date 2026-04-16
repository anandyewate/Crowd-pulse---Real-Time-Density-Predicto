# Grid and Detection Configuration
GRID_SIZE = 6
CRITICAL_THRESHOLD = 4
RISK_LIMIT = 5
MAX_PEOPLE_PER_GRID = 3

# Multi-Camera Arrays Layer Configuration
CAMERAS = [
    {"id": "CAM-01", "src": 0, "loc": "Main Front Gate"},
    {"id": "CAM-02", "src": "mock_feed_2", "loc": "Back Hallway"} 
    # For a real secondary camera, you could use index '1'
]

# Database Configuration
DB_NAME = "users.db"

# Secret Key for Flask Sessions
SECRET_KEY = "super-secret-hackathon-key"

# Twilio SMS Configuration (leave empty to simulate SMS)
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUM = ""