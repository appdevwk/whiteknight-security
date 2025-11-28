from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

class CaseData(BaseModel):
    title: str
    description: str
    investigator: str
    priority: Optional[str] = "medium"

class ThreatSignal(BaseModel):
    signal_type: str
    location: str
    strength: int
    timestamp: Optional[str] = None
    source_id: Optional[str] = None

cases_db = {}
threats_db = {}
signals_db = {}
recommendations_db = {}

app = FastAPI(
    title="WhiteKnight Security Platform",
    description="Digital Forensics for Human Trafficking Investigation",
    version="1.0.0"
)

@app.get("/")
async def root():
    return JSONResponse({"platform": "WhiteKnight Security", "version": "1.0.0", "status": "online", "mission": "Digital Forensics for Human Trafficking Investigation"})

@app.get("/health")
async def health():
    return JSONResponse({"status": "healthy"})

@app.get("/api/info")
async def api_info():
    return JSONResponse({"name": "WhiteKnight Security Platform", "version": "1.0.0", "endpoints": ["/", "/health", "/api/info", "/api/case", "/api/cases", "/api/cases/{case_id}", "/api/cases/{case_id}/evidence", "/api/threat", "/api/threats", "/api/signal", "/api/signals", "/api/ai/recommend", "/api/dashboard", "/docs", "/redoc"]})

@app.post("/api/case")
async def create_case(case_data: CaseData):
    case_id = str(uuid.uuid4())
    case = {"case_id": case_id, "title": case_data.title, "description": case_data.description, "investigator": case_data.investigator, "priority": case_data.priority, "created_at": datetime.now().isoformat(), "status": "active", "evidence_count": 0, "evidence": [], "threats_detected": 0, "signals_tracked": 0}
    cases_db[case_id] = case
    return JSONResponse({"success": True, "message": "Case created successfully", "case": case})

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str):
    if case_id not in cases_db:
        return JSONResponse({"success": False, "message": f"Case {case_id} not found"}, status_code=404)
    return JSONResponse({"success": True, "case": cases_db[case_id]})

@app.get("/api/cases")
async def list_cases():
    return JSONResponse({"success": True, "total_cases": len(cases_db), "cases": list(cases_db.values())})

@app.post("/api/cases/{case_id}/evidence")
async def add_evidence(case_id: str, evidence_data: dict):
    if case_id not in cases_db:
        return JSONResponse({"success": False, "message": f"Case {case_id} not found"}, status_code=404)
    cases_db[case_id]["evidence_count"] += 1
    cases_db[case_id]["evidence"].append({"evidence_id": str(uuid.uuid4()), "data": evidence_data, "added_at": datetime.now().isoformat()})
    return JSONResponse({"success": True, "message": "Evidence added successfully", "case_id": case_id, "evidence_count": cases_db[case_id]["evidence_count"]})

@app.put("/api/cases/{case_id}")
async def update_case(case_id: str, case_data: CaseData):
    if case_id not in cases_db:
        return JSONResponse({"success": False, "message": f"Case {case_id} not found"}, status_code=404)
    cases_db[case_id].update({"title": case_data.title, "description": case_data.description, "investigator": case_data.investigator, "priority": case_data.priority})
    return JSONResponse({"success": True, "message": "Case updated successfully", "case": cases_db[case_id]})

@app.delete("/api/cases/{case_id}")
async def delete_case(case_id: str):
    if case_id not in cases_db:
        return JSONResponse({"success": False, "message": f"Case {case_id} not found"}, status_code=404)
    deleted_case = cases_db.pop(case_id)
    return JSONResponse({"success": True, "message": "Case deleted successfully", "case": deleted_case})

@app.post("/api/signal")
async def log_signal(signal: ThreatSignal, case_id: Optional[str] = None):
    signal_id = str(uuid.uuid4())
    timestamp = signal.timestamp or datetime.now().isoformat()
    signal_entry = {"signal_id": signal_id, "signal_type": signal.signal_type, "location": signal.location, "strength": signal.strength, "source_id": signal.source_id or f"source_{signal_id[:8]}", "timestamp": timestamp, "case_id": case_id}
    signals_db[signal_id] = signal_entry
    if case_id and case_id in cases_db:
        cases_db[case_id]["signals_tracked"] += 1
    return JSONResponse({"success": True, "message": f"Signal logged: {signal.signal_type}", "signal": signal_entry})

@app.get("/api/signals")
async def list_signals(signal_type: Optional[str] = None, case_id: Optional[str] = None):
    filtered_signals = list(signals_db.values())
    if signal_type:
        filtered_signals = [s for s in filtered_signals if s["signal_type"] == signal_type]
    if case_id:
        filtered_signals = [s for s in filtered_signals if s["case_id"] == case_id]
    return JSONResponse({"success": True, "total_signals": len(filtered_signals), "signals": filtered_signals})

@app.get("/api/signals/{signal_id}")
async def get_signal(signal_id: str):
    if signal_id not in signals_db:
        return JSONResponse({"success": False, "message": f"Signal {signal_id} not found"}, status_code=404)
    return JSONResponse({"success": True, "signal": signals_db[signal_id]})

@app.post("/api/threat")
async def detect_threat(signal_id: str, threat_level: str = "medium", case_id: Optional[str] = None):
    if signal_id not in signals_db:
        return JSONResponse({"success": False, "message": f"Signal {signal_id} not found"}, status_code=404)
    threat_id = str(uuid.uuid4())
    signal = signals_db[signal_id]
    threat_entry = {"threat_id": threat_id, "signal_id": signal_id, "threat_level": threat_level, "signal_type": signal["signal_type"], "location": signal["location"], "detected_at": datetime.now().isoformat(), "case_id": case_id, "status": "detected", "ai_recommendations": [], "mitigation_applied": False}
    threats_db[threat_id] = threat_entry
    if case_id and case_id in cases_db:
        cases_db[case_id]["threats_detected"] += 1
    return JSONResponse({"success": True, "message": f"Threat detected: {threat_level}", "threat": threat_entry})

@app.get("/api/threats")
async def list_threats(threat_level: Optional[str] = None, case_id: Optional[str] = None):
    filtered_threats = list(threats_db.values())
    if threat_level:
        filtered_threats = [t for t in filtered_threats if t["threat_level"] == threat_level]
    if case_id:
        filtered_threats = [t for t in filtered_threats if t["case_id"] == case_id]
    return JSONResponse({"success": True, "total_threats": len(filtered_threats), "threats": filtered_threats})

@app.get("/api/threats/{threat_id}")
async def get_threat(threat_id: str):
    if threat_id not in threats_db:
        return JSONResponse({"success": False, "message": f"Threat {threat_id} not found"}, status_code=404)
    return JSONResponse({"success": True, "threat": threats_db[threat_id]})

def get_mitigation_commands(signal_type: str, threat_level: str) -> List[str]:
    commands = {
        "ble": {"critical": ["sudo hcitool down", "sudo bluetoothctl power off", "iwconfig wlan0 power off", "sudo iptables -P INPUT DROP", "alert_law_enforcement()"], "high": ["sudo hcitool reset", "sudo bluetoothctl disconnect all", "enable_network_monitoring()"], "medium": ["sudo hcitool scan --flush", "enable_logging()"], "low": ["log_signal()"]},
        "cell": {"critical": ["sudo airplane_mode_on()", "sudo disable_2g_3g_4g()", "alert_fcc_enforcement()", "enable_gps_logging()"], "high": ["sudo disable_4g()", "enable_cell_monitoring()"], "medium": ["enable_signal_strength_monitoring()"], "low": ["monitor_cell_activity()"]},
        "wifi": {"critical": ["sudo iwconfig wlan0 txpower off", "sudo iptables -P INPUT DROP", "disable_auto_connect()", "alert_network_security()"], "high": ["sudo iwconfig wlan0 mode managed", "disconnect_all_networks()"], "medium": ["enable_wifi_monitoring()"], "low": ["monitor_wifi_networks()"]},
        "cell_tower": {"critical": ["sudo gpsd stop", "disable_location_services()", "alert_fbi_field_office()"], "high": ["reduce_location_accuracy()"], "medium": ["monitor_tower_locations()"], "low": ["track_tower_changes()"]}
    }
    return commands.get(signal_type, {}).get(threat_level, ["log_signal()"])

def get_threat_analysis(signal_type: str, threat_level: str) -> str:
    analysis = {"ble": "BLE signal detected. Unauthorized pairing device or tracking beacon.", "cell": "Cellular signal anomaly. IMSI catcher or unauthorized network access.", "wifi": "WiFi network anomaly. Man-in-the-middle attack or rogue access point.", "cell_tower": "Cell tower signal pattern. Possible location tracking or surveillance."}
    threat_context = {"critical": "IMMEDIATE ACTION REQUIRED", "high": "URGENT action needed", "medium": "ELEVATED monitoring", "low": "INFORMATIONAL"}
    return f"{analysis.get(signal_type, 'Unknown signal')} - {threat_context.get(threat_level, '')}"

def get_recommended_action(threat_level: str) -> str:
    actions = {"critical": "LOCKDOWN: Disable all wireless, enable GPS logging, contact law enforcement", "high": "ISOLATE: Disable systems, begin detailed logging, contact incident response", "medium": "MONITOR: Increase logging, alert supervisor", "low": "LOG: Maintain standard monitoring"}
    return actions.get(threat_level, "Monitor and log")

@app.post("/api/ai/recommend")
async def ai_recommend(threat_id: str):
    if threat_id not in threats_db:
        return JSONResponse({"success": False, "message": f"Threat {threat_id} not found"}, status_code=404)
    threat = threats_db[threat_id]
    signal_type = threat["signal_type"]
    threat_level = threat["threat_level"]
    mitigation_commands = get_mitigation_commands(signal_type, threat_level)
    ai_analysis = get_threat_analysis(signal_type, threat_level)
    recommended_action = get_recommended_action(threat_level)
    recommendation_id = str(uuid.uuid4())
    recommendation = {"recommendation_id": recommendation_id, "threat_id": threat_id, "threat_level": threat_level, "threat_description": f"{signal_type.upper()} threat", "ai_analysis": ai_analysis, "mitigation_commands": mitigation_commands, "recommended_action": recommended_action, "generated_at": datetime.now().isoformat(), "status": "pending"}
    recommendations_db[recommendation_id] = recommendation
    threat["ai_recommendations"].append(recommendation_id)
    return JSONResponse({"success": True, "message": "AI recommendation generated", "recommendation": recommendation})

@app.get("/api/ai/recommendations")
async def list_recommendations(threat_id: Optional[str] = None):
    filtered_recs = list(recommendations_db.values())
    if threat_id:
        filtered_recs = [r for r in filtered_recs if r["threat_id"] == threat_id]
    return JSONResponse({"success": True, "total_recommendations": len(filtered_recs), "recommendations": filtered_recs})

@app.post("/api/ai/recommendations/{recommendation_id}/apply")
async def apply_mitigation(recommendation_id: str):
    if recommendation_id not in recommendations_db:
        return JSONResponse({"success": False, "message": f"Recommendation {recommendation_id} not found"}, status_code=404)
    rec = recommendations_db[recommendation_id]
    threat_id = rec["threat_id"]
    rec["status"] = "applied"
    threats_db[threat_id]["mitigation_applied"] = True
    threats_db[threat_id]["status"] = "mitigated"
    return JSONResponse({"success": True, "message": "Mitigation applied", "recommendation": rec, "commands_executed": rec["mitigation_commands"]})

@app.get("/api/dashboard")
async def get_dashboard(case_id: Optional[str] = None):
    case_data = None
    if case_id and case_id in cases_db:
        case_data = cases_db[case_id]
    total_signals = len(signals_db)
    total_threats = len(threats_db)
    threat_levels = {"critical": len([t for t in threats_db.values() if t["threat_level"] == "critical"]), "high": len([t for t in threats_db.values() if t["threat_level"] == "high"]), "medium": len([t for t in threats_db.values() if t["threat_level"] == "medium"]), "low": len([t for t in threats_db.values() if t["threat_level"] == "low"])}
    signal_breakdown = {}
    for signal in signals_db.values():
        sig_type = signal["signal_type"]
        signal_breakdown[sig_type] = signal_breakdown.get(sig_type, 0) + 1
    mitigated = len([t for t in threats_db.values() if t["mitigation_applied"]])
    active = total_threats - mitigated
    dashboard = {"timestamp": datetime.now().isoformat(), "case": case_data, "real_time_status": {"total_signals_detected": total_signals, "total_threats": total_threats, "active_threats": active, "mitigated_threats": mitigated}, "threat_analysis": {"by_level": threat_levels, "critical_count": threat_levels["critical"], "high_count": threat_levels["high"]}, "signal_landscape": {"by_type": signal_breakdown, "ble_signals": signal_breakdown.get("ble", 0), "cell_signals": signal_breakdown.get("cell", 0), "wifi_signals": signal_breakdown.get("wifi", 0), "cell_tower_signals": signal_breakdown.get("cell_tower", 0)}, "recent_signals": list(signals_db.values())[-5:], "active_threats": [t for t in threats_db.values() if not t["mitigation_applied"]][:5]}
    return JSONResponse({"success": True, "dashboard": dashboard})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
