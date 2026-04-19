import socket
import requests

class SiteScanner:
    def scan(self, url):
        # URL එකෙන් Domain එක පමණක් වෙන් කර ගැනීම
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        
        report = f"--- Scan Report for: {domain} ---\n\n"
        try:
            # 1. IP Address එක සෙවීම
            ip_addr = socket.gethostbyname(domain)
            report += f"[+] IP Address: {ip_addr}\n"
            
            # 2. Server Header පරීක්ෂාව
            response = requests.get(url, timeout=5)
            server = response.headers.get('Server', 'Not Disclosed')
            report += f"[+] Server Type: {server}\n"
            report += f"[+] Status Code: {response.status_code}\n"
            
            # 3. Security Headers පරීක්ෂාව
            hsts = "Enabled" if 'Strict-Transport-Security' in response.headers else "Disabled"
            report += f"[+] HSTS Security: {hsts}\n"
            
        except Exception as e:
            report += f"[-] Error during scan: {str(e)}\n"
            
        return report