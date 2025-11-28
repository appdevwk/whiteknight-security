#!/usr/bin/env python3
"""WhiteKnight AI Fortress - Enterprise SOC Dashboard"""

from flask import Flask, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhiteKnight AI Fortress - SOC Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; height: 100%; font-family: 'Courier New', monospace; background: #0a0e27; color: #0fff0f; overflow-x: hidden; }
        body { display: flex; flex-direction: column; }
        .navbar { background: #1a1f3a; border-bottom: 2px solid #0fff0f; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
        .navbar-brand { font-size: 1.5em; font-weight: bold; color: #0fff0f; text-shadow: 0 0 10px #0fff0f; }
        .navbar-right { display: flex; gap: 20px; align-items: center; font-size: 0.9em; }
        .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #0fff0f; box-shadow: 0 0 5px #0fff0f; margin-right: 5px; }
        .main-container { display: flex; flex: 1; overflow: hidden; }
        .sidebar { width: 250px; background: #1a1f3a; border-right: 2px solid #0fff0f; padding: 20px; overflow-y: auto; }
        .sidebar-section { margin-bottom: 25px; }
        .sidebar-title { color: #0fff0f; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #0fff0f; padding-bottom: 5px; }
        .sidebar-item { padding: 8px 0; color: #00dd00; cursor: pointer; transition: all 0.2s; }
        .sidebar-item:hover { color: #0fff0f; text-shadow: 0 0 5px #0fff0f; }
        .sidebar-item:before { content: "► "; margin-right: 5px; }
        .content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        .header { background: #1a1f3a; border-bottom: 1px solid #0fff0f; padding: 20px; }
        .header h1 { color: #0fff0f; font-size: 1.3em; margin-bottom: 10px; text-shadow: 0 0 10px #0fff0f; }
        .header-info { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 15px; }
        .info-box { background: rgba(15, 255, 15, 0.05); border: 1px solid #0fff0f; padding: 10px; text-align: center; }
        .info-label { font-size: 0.75em; color: #00dd00; text-transform: uppercase; }
        .info-value { font-size: 1.5em; color: #0fff0f; font-weight: bold; margin-top: 5px; text-shadow: 0 0 5px #0fff0f; }
        .dashboard { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 20px; overflow-y: auto; }
        .panel { background: #1a1f3a; border: 2px solid #0fff0f; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 0 15px rgba(15, 255, 15, 0.2); }
        .panel-header { background: #0a0e27; border-bottom: 2px solid #0fff0f; padding: 12px 15px; color: #0fff0f; font-size: 0.9em; text-transform: uppercase; font-weight: bold; text-shadow: 0 0 5px #0fff0f; }
        .panel-content { flex: 1; padding: 15px; overflow-y: auto; }
        .log-entry { font-size: 0.85em; padding: 8px 0; border-bottom: 1px dotted rgba(15, 255, 15, 0.2); }
        .log-entry:last-child { border-bottom: none; }
        .log-time { color: #00dd00; margin-right: 10px; }
        .log-critical { color: #ff0000; font-weight: bold; }
        .log-warning { color: #ffaa00; }
        .log-info { color: #0fff0f; }
        .threat-list { list-style: none; }
        .threat-list li { padding: 10px; margin-bottom: 8px; border-left: 3px solid; background: rgba(15, 255, 15, 0.03); }
        .threat-list li.critical { border-left-color: #ff0000; color: #ff0000; }
        .threat-list li.warning { border-left-color: #ffaa00; color: #ffaa00; }
        .threat-list li.info { border-left-color: #0fff0f; color: #0fff0f; }
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .stat-item { background: rgba(15, 255, 15, 0.05); border: 1px solid #0fff0f; padding: 10px; text-align: center; }
        .stat-label { font-size: 0.75em; color: #00dd00; text-transform: uppercase; }
        .stat-value { font-size: 1.3em; color: #0fff0f; font-weight: bold; margin-top: 5px; }
        .footer { background: #1a1f3a; border-top: 2px solid #0fff0f; padding: 10px 20px; text-align: center; font-size: 0.8em; color: #00dd00; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0a0e27; }
        ::-webkit-scrollbar-thumb { background: #0fff0f; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #00dd00; }
        @media (max-width: 1200px) { .dashboard { grid-template-columns: 1fr; } .header-info { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="navbar-brand">🚨 WhiteKnight AI Fortress</div>
        <div class="navbar-right">
            <span><span class="status-indicator"></span>SYSTEM OPERATIONAL</span>
            <span id="current-time">00:00:00</span>
        </div>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <div class="sidebar-section">
                <div class="sidebar-title">Navigation</div>
                <div class="sidebar-item">Dashboard</div>
                <div class="sidebar-item">Threat Analysis</div>
                <div class="sidebar-item">Network Monitor</div>
                <div class="sidebar-item">Alerts</div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-title">Modules</div>
                <div class="sidebar-item">Real-Time Detection</div>
                <div class="sidebar-item">ML Analysis</div>
                <div class="sidebar-item">Threat Intel</div>
                <div class="sidebar-item">Forensics</div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-title">System</div>
                <div class="sidebar-item">Settings</div>
                <div class="sidebar-item">Reports</div>
                <div class="sidebar-item">Support</div>
            </div>
        </div>
        
        <div class="content">
            <div class="header">
                <h1>ENTERPRISE SECURITY OPERATIONS CENTER</h1>
                <div class="header-info">
                    <div class="info-box"><div class="info-label">System Status</div><div class="info-value">● ACTIVE</div></div>
                    <div class="info-box"><div class="info-label">Threats Detected</div><div class="info-value">3</div></div>
                    <div class="info-box"><div class="info-label">Detection Rate</div><div class="info-value">98.7%</div></div>
                    <div class="info-box"><div class="info-label">Uptime</div><div class="info-value">99.8%</div></div>
                </div>
            </div>
            
            <div class="dashboard">
                <div class="panel">
                    <div class="panel-header">► ACTIVE THREATS</div>
                    <div class="panel-content">
                        <ul class="threat-list">
                            <li class="critical">[CRITICAL] Suspicious Network Activity - Port 443 Data Exfiltration</li>
                            <li class="warning">[WARNING] Brute Force Attack Detected - SSH Protocol 192.168.1.x</li>
                            <li class="info">[INFO] Policy Violation - Unauthorized Application Execution</li>
                        </ul>
                    </div>
                </div>
                
                <div class="panel">
                    <div class="panel-header">► SYSTEM LOG</div>
                    <div class="panel-content">
                        <div class="log-entry"><span class="log-time">[08:35:12]</span> <span class="log-info">WhiteKnight AI Fortress initialized</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:14]</span> <span class="log-info">Loading threat detection modules...</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:16]</span> <span class="log-info">Database connection established</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:18]</span> <span class="log-info">Real-time monitoring activated</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:20]</span> <span class="log-critical">CRITICAL: Network anomaly detected</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:22]</span> <span class="log-warning">WARNING: Brute force attack detected</span></div>
                        <div class="log-entry"><span class="log-time">[08:35:24]</span> <span class="log-info">Threat analysis in progress...</span></div>
                    </div>
                </div>
                
                <div class="panel">
                    <div class="panel-header">► STATISTICS</div>
                    <div class="panel-content">
                        <div class="stats-grid">
                            <div class="stat-item"><div class="stat-label">Total Threats</div><div class="stat-value">12,487</div></div>
                            <div class="stat-item"><div class="stat-label">Blocked Today</div><div class="stat-value">47</div></div>
                            <div class="stat-item"><div class="stat-label">False Positive Rate</div><div class="stat-value">0.3%</div></div>
                            <div class="stat-item"><div class="stat-label">Avg Response Time</div><div class="stat-value">245ms</div></div>
                        </div>
                    </div>
                </div>
                
                <div class="panel">
                    <div class="panel-header">► TECHNOLOGY STACK</div>
                    <div class="panel-content">
                        <div class="log-entry">Backend: Flask / FastAPI / uvicorn</div>
                        <div class="log-entry">Data: Pandas / NumPy / SciPy</div>
                        <div class="log-entry">ML: Scikit-learn / TensorFlow</div>
                        <div class="log-entry">Visualization: Plotly / Streamlit</div>
                        <div class="log-entry">Real-time: WebSockets / Redis</div>
                        <div class="log-entry">Monitoring: Elasticsearch / Loguru</div>
                        <div class="log-entry">Testing: Pytest / Coverage</div>
                        <div class="log-entry">Deployment: Docker / Compose</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        WhiteKnight AI Fortress v1.0.0 | Fighting human trafficking through cybersecurity | Last update: 08:35:24 UTC
    </div>
    
    <script>
        function updateTime() {
            const now = new Date();
            const time = now.toLocaleTimeString('en-US', { hour12: false });
            document.getElementById('current-time').textContent = time;
        }
        updateTime();
        setInterval(updateTime, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    return jsonify({
        'service': 'WhiteKnight Threat Analysis API',
        'status': 'operational',
        'ai_model': 'Perplexity Sonar',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime': '99.8%',
        'threats_detected': 12487,
        'false_positive_rate': 0.3
    })

@app.route('/api/threats')
def api_threats():
    return jsonify({
        'active_threats': [
            {'id': 1, 'severity': 'CRITICAL', 'title': 'Suspicious Network Activity', 'description': 'Unusual data exfiltration detected on port 443', 'timestamp': datetime.now().isoformat()},
            {'id': 2, 'severity': 'WARNING', 'title': 'Brute Force Attempt', 'description': 'Multiple failed SSH login attempts from 192.168.1.x', 'timestamp': datetime.now().isoformat()},
            {'id': 3, 'severity': 'INFO', 'title': 'Policy Violation', 'description': 'Unauthorized application detected on workstation', 'timestamp': datetime.now().isoformat()}
        ]
    })

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════╗")
    print("║  WhiteKnight AI Fortress - Security Operations Center  ║")
    print("║                    v1.0.0 - Active                     ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\n🚀 Dashboard available at: http://localhost:8000")
    print("🔌 API Status endpoint: http://localhost:8000/api/status")
    print("⚠️  Threats endpoint: http://localhost:8000/api/threats")
    print("\n[INFO] Server starting on 0.0.0.0:8000")
    print("[INFO] Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=8888, use_reloader=False)
