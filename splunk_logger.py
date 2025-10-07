import requests

class SplunkLogger:
    def __init__(self, url, token):
        self.url = url.rstrip('/') + '/services/collector'
        self.token = token

    def log_block(self, ip):
        if not self.token or 'YOUR_TOKEN' in self.token:
            return  # disabled
        headers = {'Authorization': f'Splunk {self.token}'}
        data = {'event': {'action': 'block', 'ip': ip}}
        try:
            requests.post(self.url, json=data, headers=headers, timeout=2)
        except Exception:
            pass
