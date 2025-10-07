#!/bin/bash
set -e

REPO_DIR="/opt/ddos_protection"
TEMPLATES_DIR="$REPO_DIR/templates"

echo "Updating package lists..."
sudo apt-get update
echo "Installing Python and dependencies..."
sudo apt-get install -y python3 python3-pip iptables python3-venv

echo "Installing Python packages..."
sudo pip3 install -r requirements.txt || sudo python3 -m pip install -r requirements.txt

echo "Setting up DDOS Protection files..."
sudo mkdir -p $TEMPLATES_DIR

# Copy all files
for file in ddos_core.py firewall_manager.py ml_detection.py data_collector.py splunk_logger.py retrain_scheduler.py config.py dashboard.py requirements.txt; do
    if [ -f "$file" ]; then
        sudo cp $file $REPO_DIR/
    else
        echo "Warning: $file not found in current directory"
    fi
done

if [ -f templates/dashboard.html ]; then
  sudo cp templates/dashboard.html $TEMPLATES_DIR/
else
  echo "Warning: templates/dashboard.html missing"
fi

# Permissions
sudo chmod +x $REPO_DIR/*.py || true

# Systemd service for main DDOS protection
sudo tee /etc/systemd/system/ddos_protection.service > /dev/null <<EOF
[Unit]
Description=AI DDOS Protection System
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $REPO_DIR/ddos_core.py
Restart=always
RestartSec=5
StandardOutput=append:/var/log/ddos_protection.log
StandardError=append:/var/log/ddos_protection.err

[Install]
WantedBy=multi-user.target
EOF

# Systemd service for dashboard
sudo tee /etc/systemd/system/ddos_dashboard.service > /dev/null <<EOF
[Unit]
Description=AI DDOS Protection Dashboard
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $REPO_DIR/dashboard.py
Restart=always
RestartSec=5
StandardOutput=append:/var/log/ddos_dashboard.log
StandardError=append:/var/log/ddos_dashboard.err

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ddos_protection || true
sudo systemctl enable ddos_dashboard || true
sudo systemctl restart ddos_protection || true
sudo systemctl restart ddos_dashboard || true

echo "AI DDOS protection core and dashboard are set up and running (if no errors above)."