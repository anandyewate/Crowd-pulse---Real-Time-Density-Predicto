import time
import json
import os
from config import CAMERAS, NOTIFICATION_NUMBER
from sms_service import send_sms
import numpy as np
import threading

video_frames = {}
frame_lock = threading.Lock()

STATE_FILE = "system_state.json"

class GlobalRegistry:
    def __init__(self):
        # List of {"embedding": np.array, "last_seen": timestamp, "cam_id": str}
        self.active_signatures = []
        self.threshold = 0.85 # Similarity threshold for ReID
        
    def match_and_update(self, cam_id, embeddings):
        current_time = time.time()
        
        # 1. Expire old signatures (30s timeout)
        self.active_signatures = [s for s in self.active_signatures if current_time - s["last_seen"] < 30]
        
        for emb in embeddings:
            found_match = False
            for sig in self.active_signatures:
                # Cosine similarity check
                sim = np.dot(emb, sig["embedding"])
                if sim > self.threshold:
                    sig["last_seen"] = current_time
                    sig["cam_id"] = cam_id # Update source cam
                    found_match = True
                    break
            
            if not found_match:
                # Add new signature
                self.active_signatures.append({
                    "embedding": emb,
                    "last_seen": current_time,
                    "cam_id": cam_id
                })
        
        return len(self.active_signatures)

global_registry = GlobalRegistry()

cam_states = {}
for c in CAMERAS:
    cam_states[c["id"]] = {
        "timeline": [],
        "last_critical_start_time": None,
        "is_predictive_alert_active": False,
        "has_sent_predictive_sms": False,
        "payload": {}
    }

def update_state(cam_id, location, people_count, fps, target_risk, panic, prediction, max_capacity=0, resolution="N/A", entropy=0.0, ai_report="", embeddings=[]):
    global cam_states, global_registry
    
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
    elif entropy >= 1.5:
        alert_text = "HIGH CHAOS DETECTED - POSSIBLE DISTURBANCE"
        alert_level = "CRITICAL"
    elif target_risk >= 5:
        alert_text = "Density Increasing"
        alert_level = "CAUTION"
    
    # 10s Predictive Rule scoped by camera ID
    if alert_level == "CRITICAL" or panic or entropy >= 1.5:
        if state["last_critical_start_time"] is None:
            state["last_critical_start_time"] = current_time
        elif (current_time - state["last_critical_start_time"]) >= 10.0:
            if panic:
                 alert_text = "🚨 PANIC STATE DETECTED - SWARM BEHAVIOR"
            elif entropy >= 1.5:
                 alert_text = "🧠 INTELLIGENCE ALERT: HIGH CHAOS DETECTED"
            else:
                 alert_text = "🚨 STAMPEDE EMINENT - PREPARE EVACUATION"
            
            state["is_predictive_alert_active"] = True
            
            if not state["has_sent_predictive_sms"]:
                _log_msg(cam_id, "PREDICTIVE ALARM ACTIVATED")
                print(f"== TRIGGERING EMERGENCY SMS WEBHOOK for {cam_id} ==")
                send_sms(NOTIFICATION_NUMBER, alert_text + f" at {location}")
                state["has_sent_predictive_sms"] = True
    else:
        state["last_critical_start_time"] = None
        state["is_predictive_alert_active"] = False
        state["has_sent_predictive_sms"] = False

    if state["is_predictive_alert_active"]:
        alert_level = "PREDICTIVE_CRITICAL"
    
    # Update Global De-duplication Registry
    unique_count = global_registry.match_and_update(cam_id, embeddings)
        
    state["payload"] = {
        "timestamp": time.strftime("%H:%M:%S"),
        "people_count": int(people_count),
        "fps": int(fps),
        "risk_score": float(round(target_risk, 2)),
        "alert_level": alert_level,
        "message": alert_text,
        "location": location,
        "camera": cam_id,
        "panic": bool(panic),
        "prediction": str(prediction),
        "max_capacity": int(max_capacity),
        "resolution": str(resolution),
        "chaos_score": float(round(entropy, 2)),
        "strategic_report": str(ai_report),
        "global_unique_count": int(unique_count),
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
    # Priority: Return in-memory state for unified execution
    final_payload = {c_id: cam_states[c_id]["payload"] for c_id in cam_states if cam_states[c_id]["payload"]}
    if final_payload:
        return final_payload
        
    # Fallback: Read from file if memory state is empty
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