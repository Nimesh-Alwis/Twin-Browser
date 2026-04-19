from datetime import datetime

class SecurityManager:
    def __init__(self):
        self.blocked_sites = ["malware.com", "phishing-site.net"]
        self.log_file = "history_log.txt"

    def is_url_safe(self, url):
        # මුලින්ම ලොග් එක සටහන් කරගමු
        self.log_visit(url)

        if not url.startswith('https://'):
            return False, "Unsecure Connection (HTTP is blocked)"

        for site in self.blocked_sites:
            if site in url.lower():
                return False, f"Site '{site}' is Blacklisted"
        
        return True, "Safe"

    def log_visit(self, url):
        # වර්තමාන වෙලාව ලබා ගැනීම
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # history_log.txt එකට දත්ත එකතු කිරීම (Append mode)
        with open(self.log_file, "a") as f:
            f.write(f"[{now}] Visited: {url}\n")