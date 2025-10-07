import subprocess
import ipaddress
import time

class FirewallManager:
    def __init__(self, whitelist, block_policies):
        self.whitelist = whitelist
        self.blocked_ips = {}
        self.block_policies = block_policies

    def is_whitelisted(self, ip):
        for entry in self.whitelist:
            if '/' in entry:
                try:
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(entry, strict=False):
                        return True
                except ValueError:
                    continue
            elif ip == entry:
                return True
        return False

    def block_ip(self, ip, protocol=None, port=None, rate_limit=None):
        if self.is_whitelisted(ip):
            print(f"[FIREWALL] Skip whitelisted {ip}")
            return False
        if ip in self.blocked_ips:
            return False
        duration = self.block_policies.get(ip, self.block_policies['default'])
        self.blocked_ips[ip] = {"start": time.time(), "duration": duration}
        cmd = ["sudo", "iptables", "-I", "INPUT", "-s", ip]
        if protocol:
            cmd += ["-p", protocol]
        if port:
            cmd += ["--dport", str(port)]
        if rate_limit:
            cmd += ["-m", "limit", "--limit", rate_limit]
        cmd += ["-j", "DROP"]
        try:
            subprocess.run(cmd, check=True)
            print(f"[FIREWALL] Blocked {ip} for {duration}s")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[FIREWALL][ERROR] Failed to block {ip}: {e}")
            self.blocked_ips.pop(ip, None)
            return False

    def unblock_expired(self):
        now = time.time()
        for ip in list(self.blocked_ips.keys()):
            meta = self.blocked_ips[ip]
            if now - meta['start'] > meta['duration']:
                cmd = ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
                try:
                    subprocess.run(cmd, check=True)
                    print(f"[FIREWALL] Unblocked {ip}")
                except subprocess.CalledProcessError:
                    print(f"[FIREWALL][WARN] Could not remove rule for {ip} (may already be gone)")
                finally:
                    self.blocked_ips.pop(ip, None)
