# AI-DDOS-Firewall prototype

An educational Python prototype for DDoS detection and firewall responses on Linux. The machine-learning component is a placeholder.

## Prototype components
- Placeholder LSTM detection component.
- Configurable block policies and whitelisting (IP + subnet)
- Firewall responses, with further rate-limiting and protocol/port rules listed as future work.
- Flask dashboard prototype.
- External log integration stub (Splunk HTTP Event Collector)
- Model retraining scaffold.

> This is an educational scaffold. The model is a placeholder; the project does not establish production DDoS protection.

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
The ML component is a placeholder. Further work on sequence modelling would include:
1. Aggregate sliding window feature vectors (e.g., packets/sec, unique IPs, entropy metrics)
2. Shape training data: (batch, timesteps, features)
3. Save labelled datasets for supervised training.

## Security Considerations
- Validate Splunk endpoint + use HTTPS.
- Restrict dashboard (add auth / firewall).
- Limit iptables rule growth (consider ipset / nftables).
- Run packet capture with least privileges (e.g., dedicated user + capabilities).

## Roadmap
- Review alternatives to the current iptables rules before making performance claims.
- Add rate limiting responses
- Add protocol/port specific mitigation strategies
- Implement rolling dataset + incremental model training
- Add Prometheus metrics export
