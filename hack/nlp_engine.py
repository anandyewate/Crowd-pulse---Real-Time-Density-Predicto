import random

def generate_assessment(cam_id, people, risk, entropy, prediction):
    """
    Simulates a high-level NLP Situational Assessment Engine.
    Converts telemetry into tactical intelligence reports.
    """
    
    severity_map = {
        "SAFE": "Low-level background activity.",
        "CAUTION": "Elevation in thermal density detected.",
        "CRITICAL": "Critical threshold violation. Imminent threat status.",
        "PREDICTIVE_CRITICAL": "Predictive models indicate high probability of stampede."
    }
    
    # Analyze Chaos/Entropy (The NLP "Logic" part)
    chaos_analysis = ""
    if entropy > 1.5:
        chaos_analysis = "Extreme kinetic turbulence (High Entropy). Swarm behavior observed."
    elif entropy > 1.0:
        chaos_analysis = "Instability detected in crowd flow vectors."
    else:
        chaos_analysis = "Coherent movement patterns maintained."

    # Analyze Predictions
    tactical_insight = ""
    if "ACCELERATING" in prediction:
        tactical_insight = "Neural models suggest immediate evacuation may be necessary."
    elif "INCREASE" in prediction:
        tactical_insight = "Monitoring for continued density accumulation."
    elif "STABLE" in prediction or "MONITORING" in prediction:
        tactical_insight = "No tactical changes recommended at this interval."

    # Compile the "AI Strategic Report"
    report_pool = [
        f"Node {cam_id} Intelligence: {severity_map.get(risk, 'Analyzing...')}",
        f"Kinetic State: {chaos_analysis}",
        f"Strategic Outlook: {tactical_insight}",
        f"Current throughput: {people} entities tracked with persistent IDs."
    ]
    
    return " | ".join(report_pool)
