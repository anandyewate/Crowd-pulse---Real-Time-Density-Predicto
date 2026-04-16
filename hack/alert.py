import time
import json
import os
from config import CAMERAS
from sms_service import send_sms

STATE_FILE = "system_state.json"

cam_states = {}
for c in CAMERAS:
    cam_states[c["id"]] = {
        "timeline": [],
        "last_critical_start_time": None,
        "is_predictive_alert_active": False,
        "has_sent_predictive_sms": False,
        "payload": {}
    }

def update_state(cam_id, location, people_count, fps, target_risk, panic, prediction):
    global cam_states
    
    if cam_id not in cam_states:
        return
        
    state = cam_states[cam_id]
    current_time = time.time()
    
    alert_text = "System Nominal"
    alert_level = "SAFE"
    
    if panic:
        alert_text = "PANIC DETECTED - SWARM BEHAVIOR"
        alert_level = "CRITICAL"
        if len(state["timeline"]) == 0 or "PANIC" not in state["timeline"][-1]:
            _log_msg(cam_id, alert_text)
            
    elif target_risk >= 8:
        alert_text = "CRITICAL CROWD SURGE"
        alert_level = "CRITICAL"
    elif target_risk >= 5:
        alert_text = "Density Increasing"
        alert_level = "CAUTION"
    
    # 10s Predictive Rule scoped by camera ID
    if alert_level == "CRITICAL" or panic:
        if state["last_critical_start_time"] is None:
            state["last_critical_start_time"] = current_time
        elif (current_time - state["last_critical_start_time"]) >= 10.0:
            state["is_predictive_alert_active"] = True
            alert_text = "🚨 STAMPEDE EMINENT - PREPARE EVACUATION"
            
            if not state["has_sent_predictive_sms"]:
                _log_msg(cam_id, "PREDICTIVE ALARM ACTIVATED")
                print(f"== TRIGGERING EMERGENCY SMS WEBHOOK for {cam_id} ==")
                send_sms("+1234567890", alert_text + f" at {location}")
                state["has_sent_predictive_sms"] = True
    else:
        state["last_critical_start_time"] = None
        state["is_predictive_alert_active"] = False
        state["has_sent_predictive_sms"] = False

    if state["is_predictive_alert_active"]:
        alert_level = "PREDICTIVE_CRITICAL"
        
    state["payload"] = {
        "timestamp": time.strftime("%H:%M:%S"),
        "people_count": people_count,
        "fps": int(fps),
        "risk_score": round(target_risk, 2),
        "alert_level": alert_level,
        "message": alert_text,
        "location": location,
        "camera": cam_id,
        "panic": panic,
        "prediction": prediction,
        "timeline": state["timeline"][-5:]
    }

    _flush_state()

def _log_msg(cam_id, event):
    t = time.strftime("%H:%M:%S")
    cam_states[cam_id]["timeline"].append(f"{t} -> {event}")
    if len(cam_states[cam_id]["timeline"]) > 20:
        cam_states[cam_id]["timeline"].pop(0)

def _flush_state():
    final_payload = {c_id: cam_states[c_id]["payload"] for c_id in cam_states if cam_states[c_id]["payload"]}
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(final_payload, f)
    except:
        pass

def get_alert():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def log_event(e): pass
def trigger_alert(r, p): pass
def clear_alert(): pass
def get_timeline(): return []