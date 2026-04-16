# 🚨 CrowdPulse: AI Crowd Monitoring & Risk Detection System

CrowdPulse is an AI-based system designed to monitor crowd density in real-time and detect potential risks such as overcrowding or stampede situations using computer vision.

Built for hackathons and real-world safety applications, this system processes video input and provides risk analysis with actionable insights.

---

## 🔥 Features

- 🎥 Real-time video processing (CCTV / webcam / video input)
- 🧍 People detection using YOLO / OpenCV
- 📊 Crowd density estimation
- ⚠️ Risk level classification (LOW / MODERATE / HIGH)
- 🧩 Grid-based crowd analysis (optional advanced feature)
- 📈 Visual overlays and analytics
- 🔔 Alert system (SMS / notifications ready)

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **YOLO (Object Detection)**
- **NumPy**
- **MediaPipe (optional)**
- **Flask (if using web interface)**

---

## 📂 Project Structure
CrowdPulse/
│
├── main.py # Entry point
├── detect.py # Person detection logic
├── risk.py # Risk calculation logic
├── utils.py # Helper functions
├── config.py # Configurations (thresholds, etc.)
│
├── models/ # YOLO weights / models
├── static/ # CSS / JS (if web app)
├── templates/ # HTML (if Flask app)
│
├── requirements.txt
└── README.md


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/anandyewate/crowdpulse.git
cd crowdpulse

### Creating environments
python -m venv venv
venv\Scripts\activate   # Windows

###Installing Dependencies
pip install -r requirements.txt

#How to Run
python main.py

🧠 How It Works
Video frames are captured in real-time
YOLO detects people in each frame
Crowd density is calculated based on:
Number of people
Area coverage
Risk is evaluated using thresholds:
LOW → Normal movement
MODERATE → Increasing density
HIGH → Possible danger (stampede risk)
Output is displayed with bounding boxes + alerts

📊 Risk Logic Example
if density < 0.3:
    risk = "LOW"
elif density < 0.6:
    risk = "MODERATE"
else:
    risk = "HIGH"

🎯 Use Cases
Public events (concerts, festivals)
Railway stations / airports
Smart city surveillance
Disaster management systems