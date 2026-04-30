# 🚨 CrowdPulse: AI Crowd Monitoring & Risk Detection System

CrowdPulse is an AI-driven surveillance system designed to monitor crowd density in real time and detect potential risks such as overcrowding or stampede situations using computer vision techniques.

Built for hackathons and scalable real-world deployment, the system processes live or recorded video streams and provides actionable risk insights to improve public safety.

---

## 🔥 Features

- 🎥 Real-time video processing (CCTV / webcam / video input)
- 🧍 Person detection using YOLO (OpenCV integration)
- 📊 Crowd density estimation
- ⚠️ Risk level classification (LOW / MODERATE / HIGH)
- 🧩 Grid-based crowd analysis *(advanced feature)*
- 📈 Visual overlays (bounding boxes, density indicators)
- 🔔 Alert system (SMS / notifications ready for integration)
- 🌐 Optional web dashboard (Flask-based)

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **YOLO (Object Detection)**
- **NumPy**
- **MediaPipe** *(optional enhancements)*
- **Flask** *(for web interface)*

---

## 📂 Project Structure
CrowdPulse/
│
├── main.py # Application entry point
├── detect.py # Person detection logic (YOLO)
├── risk.py # Risk calculation & classification
├── utils.py # Helper functions
├── config.py # Thresholds and configuration
│
├── models/ # YOLO weights / model files
├── static/ # CSS / JS (for web UI)
├── templates/ # HTML templates (Flask)
│
├── requirements.txt # Dependencies
└── README.md # Documentation


---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anandyewate/crowdpulse.git
cd crowdpulse

### 2.Create Venv
python -m venv venv


🧠 How It Works
🎥 Captures video frames in real time
🧍 Detects people using YOLO model
📊 Calculates crowd density based on:
Number of detected individuals
Spatial distribution / frame area
⚠️ Evaluates risk levels using predefined thresholds
📈 Displays output with bounding boxes, density metrics, and alerts

🎯 Use Cases
🎤 Public events (concerts, festivals)
🚉 Railway stations & airports
🏙️ Smart city surveillance systems
🚨 Disaster prevention & emergency response
🏫 Campus safety monitoring
🚀 Future Improvements
Multi-camera integration
Cloud deployment (AWS / GCP)
Real-time dashboard analytics
AI-based anomaly detection (beyond density)
Mobile app integration for alerts


This project was developed collaboratively by:

- **Anand Vilas Yewate**
- **Pratham Bodke**
- **Rohan Suryawanshi**
- **Rushikesh Babar**

---

## 🤝 Contributions

Each team member contributed to different aspects of the project including:

- Computer Vision & Detection Models  
- Risk Analysis & Logic Design  
- Backend Development (Flask)  
- Frontend & Visualization  
- System Integration & Testing  
