import time
from firewall_manager import FirewallManager
from ml_detection import MLDetector
from data_collector import TrafficCollector
from splunk_logger import SplunkLogger
from config import WHITELIST, BLOCK_POLICIES, SPLUNK_URL, SPLUNK_TOKEN, MODEL_PATH

CHECK_INTERVAL = 5  # seconds between collection cycles

firewall = FirewallManager(WHITELIST, BLOCK_POLICIES)
detector = MLDetector(model_path=MODEL_PATH)
collector = TrafficCollector(interval=CHECK_INTERVAL)
logger = SplunkLogger(url=SPLUNK_URL, token=SPLUNK_TOKEN)

def main():
    detector.load_or_init()
    print("[CORE] AI DDOS Protection Engine started.")
    while True:
        try:
            features, ip_counts = collector.collect_metrics()
            attack, attackers = detector.detect_attack(features, ip_counts)
            if attack:
                print(f"[ALERT] Potential attack detected. Suspects: {attackers}")
                for ip in attackers:
                    if firewall.block_ip(ip):
                        logger.log_block(ip)
            firewall.unblock_expired()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
