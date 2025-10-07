from flask import Flask, render_template, jsonify
from firewall_manager import FirewallManager
from config import WHITELIST, BLOCK_POLICIES

app = Flask(__name__)
# This dashboard instance has an isolated firewall manager; for a unified state,
# consider IPC or shared state (e.g., Redis) between core engine and dashboard.
firewall = FirewallManager(WHITELIST, BLOCK_POLICIES)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/blocked_ips')
def blocked_ips():
    return jsonify([
        {"ip": ip, "remaining": max(0, meta['duration'] - (time.time() - meta['start']))}
        for ip, meta in firewall.blocked_ips.items()
    ])

@app.route('/api/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    import time
    app.run(host='0.0.0.0', port=5000)
