class SecurityManager:
    def __init__(self):
        self.blocked_sites = ["malware.com", "phishing-site.net"]

    def is_url_safe(self, url):
        # 1. මුලින්ම පරීක්ෂා කරනවා URL එක https:// වලින්ද පටන් ගන්නේ කියලා
        if not url.startswith('https://'):
            print(f"Blocked unsecure connection: {url}")
            return False, "Unsecure Connection (HTTP is blocked)"

        # 2. ඊළඟට Blacklist එක පරීක්ෂා කරනවා
        for site in self.blocked_sites:
            if site in url.lower():
                return False, f"Site '{site}' is Blacklisted"
        
        return True, "Safe"