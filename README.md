# AI-DDOS Protection Firewall

A modular, AI-powered DDoS protection system for Linux servers.

## Features
- Machine learning based anomaly detection (LSTM placeholder – extend with real time-series windows)
- Configurable block policies and whitelisting (IP + subnet)
- Flexible firewall responses (future: rate limiting / protocol / port specific rules)
- Web dashboard (Flask) for viewing blocked IPs & recent logs
- External log integration stub (Splunk HTTP Event Collector)
- Automated model retraining scaffold

> NOTE: This project is a reference / educational scaffold. Production DDoS mitigation requires hardening, performance tuning, kernel/network stack optimizations, and thorough security review. Use cautiously.

## Quick Start
```bash
sudo ./setup_ddos_protection.sh
```
Dashboard: http://YOUR_SERVER:5000

## Configuration
Edit `config.py`:
```python
WHITELIST = {"192.168.1.1", "10.0.0.0/24"}
BLOCK_POLICIES = {"default": 600, "192.168.1.100": 1800}
SPLUNK_URL = "http://splunk-server:8088"
SPLUNK_TOKEN = "YOUR_TOKEN"
```

## Systemd Services
- ddos_protection (core engine)
- ddos_dashboard (web UI)

## Data & Model
Current ML implementation is a minimal placeholder. Real sequence modeling would:
1. Aggregate sliding window feature vectors (e.g., packets/sec, unique IPs, entropy metrics)
2. Shape training data: (batch, timesteps, features)
3. Persist labeled datasets for supervised refinement.

## Security Considerations
- Validate Splunk endpoint + use HTTPS.
- Restrict dashboard (add auth / firewall).
- Limit iptables rule growth (consider ipset / nftables).
- Run packet capture with least privileges (e.g., dedicated user + capabilities).

## Roadmap
- Replace iptables with nftables + ipset for performance
- Add rate limiting responses
- Add protocol/port specific mitigation strategies
- Implement rolling dataset + incremental model training
- Add Prometheus metrics export

## License
MIT (add a LICENSE file if desired)
