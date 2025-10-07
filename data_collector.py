from scapy.all import sniff
from collections import defaultdict

class TrafficCollector:
    def __init__(self, interval=5):
        self.interval = interval

    def collect_metrics(self):
        ip_counts = defaultdict(int)
        def process(pkt):
            if pkt.haslayer('IP'):
                try:
                    src = pkt['IP'].src
                    ip_counts[src] += 1
                except Exception:
                    pass
        sniff(timeout=self.interval, prn=process, store=0)
        total_packets = sum(ip_counts.values())
        unique_ips = len(ip_counts)
        features = [total_packets, unique_ips]
        return features, ip_counts
