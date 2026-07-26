# 🌐 Twin-Browser Secure v2.0 (Ethical Hacking & AI Edition)

<div align="center">
  <p>A high-performance, security-focused web browser built using <b>Python</b> and <b>PyQt6</b>. Engineered specifically for ethical hackers, bug bounty hunters, cybersecurity researchers, and power users. It integrates professional web pentesting tools, an ALL AI Hub with 22+ built-in AI tools, ad-blocking, split-screen viewing, custom script injection, user-agent spoofing, and customizable user shortcuts directly into the browsing experience.</p>
</div>

---

## 🚀 Key Features

### 🔌 Offensive Security & Web Pentesting Suite
* **Burp Suite / OWASP ZAP Proxy Switcher:** One-click application-wide HTTP proxy toggle (`127.0.0.1:8080`) to seamlessly route browser traffic to Burp Suite, OWASP ZAP, or Caido without touching Windows proxy settings.
* **Cookie & Session Manager:** Real-time table interface to view, add, edit, and delete active website cookies and session data (`QWebEngineCookieStore`) for testing session hijacking and privilege escalation.
* **HTTP Request Repeater:** Craft custom `GET`, `POST`, `PUT`, `DELETE`, `PATCH` requests with custom headers and body payloads. Inspect response status codes, latency, headers, and body formatting directly in the browser.
* **Tech Stack & WAF Detector:** Passive scanning engine to detect target CMS (WordPress, Joomla, Drupal, Shopify), Backend Frameworks (Laravel, Django, Node.js), Web Servers (Nginx, Apache, IIS), and WAF/CDNs (Cloudflare, Akamai, Imperva).
* **Parameter Fuzzer & Vuln Checker:** Automated GET parameter testing engine for Reflected XSS, Local File Inclusion (LFI - `/etc/passwd`, `win.ini`), and Open Redirect vulnerabilities.
* **Cyber Encoder & Cryptographic Hasher:** CyberChef-style tool with dedicated **🔒 ENCODE** and **🔓 DECODE** buttons for Base64 (with auto-padding fix), URL Encoding, HTML Entities, Hexadecimal, and MD5, SHA-1, SHA-256, SHA-512 hash generation.
* **Site Scanner & Subdomain Finder:** Passive domain reconnaissance extracting server headers, HSTS verification, IP addresses, and crt.sh subdomain lookup.
* **Traffic Monitor:** Real-time network logger inspecting outgoing HTTP/HTTPS requests, methods, and status codes.
* **Payload Notebook:** Built-in text editor (`text_editor.py`) pre-loaded with XSS, SQLi, and Command Injection cheat sheets and payload templates.

### 🤖 ALL AI Hub & Productivity Tools
* **ALL AI Hub (`Ctrl+Shift+A`):** Built-in dashboard containing **22+ leading AI platforms** (ChatGPT, Claude, Gemini, Perplexity, DeepSeek, Poe, Copilot, HuggingChat, Mistral, Phind, Grok, Consensus, SciSpace, Midjourney, ElevenLabs, Suno, Runway, Leonardo, Krea, DeepL, Perchance) categorized with a real-time search filter.
* **Custom Keyboard Shortcuts Manager (`Ctrl+K`):** Rebind browser shortcuts dynamically with persistent storage (`user_shortcuts.json`).
* **Ad-Blocker & Tracker Interceptor:** Built-in network request interceptor that blocks advertising and tracking domains for faster, private browsing.
* **Split-Screen Dual View Mode:** Split tabs side-by-side with a drag-adjustable `QSplitter` and instant URL swapping.
* **Custom CSS & JS Script Injector:** Inject custom CSS stylesheets (e.g., Force Dark Mode) and execute custom JavaScript code on any webpage.
* **Incognito / Private Browsing Mode:** Off-the-record isolated profile tabs that leave no local history or session cache.
* **Dedicated Download Manager:** Track active and completed video downloads with quick "Open File" and "Open Folder" actions.
* **Customizable Speed Dial Startpage:** Glassmorphic startpage (`homepage.html`) with dynamic tiles, custom tile creation modal (`➕ Add Shortcut`) with emoji icons, and hover deletion (`×`).

### 🛡️ Security, Privacy & Data Persistence
* **URL Safety Guard:** Cross-references URLs against a local blacklist to block malicious and phishing destinations.
* **Enforced HTTPS:** Automatically upgrades insecure `http://` connections to `https://`.
* **User-Agent Spoofing:** Disguise browser identity with built-in profiles (Chrome, Safari Mobile, Googlebot, cURL).
* **Install Location Data Persistence:** Uses `path_utils.py` so all bookmarks, notes, downloads, history, and configuration files are stored directly inside the user's chosen installation folder (`C:`, `D:`, `E:`).

---

## 🛠️ Tech Stack Architecture

* **Language:** `Python 3.11+`
* **GUI Framework:** `PyQt6`
* **Web Engine:** `PyQt6-WebEngine` (Chromium rendering engine)
* **Networking & HTTP:** `requests`, `urllib3`, `socket`
* **Media Handling:** `yt-dlp` (multi-threaded video downloader)
* **Packaging & Installation:** `PyInstaller` (Executable compilation), `Inno Setup` (Setup Wizard)

---

## 📂 Project Structure

| File / Directory | Function |
| :--- | :--- |
| `main.py` | Entry point. Wires the UI, WebEngine, shortcuts, and core event loops. |
| `ui_components.py` | Navigation Bar, Tools Sidebar, and modular window layouts. |
| `browser_engine.py` | Web rendering engine, off-the-record profiles, and traffic interceptors. |
| `proxy_manager.py` | One-click Application Proxy Switcher for Burp Suite / OWASP ZAP. |
| `cookie_manager.py` | Interactive Cookie & Session inspection, creation, and deletion GUI. |
| `encoder_decoder.py` | Live Cyber Encoder/Decoder & Cryptographic Hash generator. |
| `request_repeater.py` | Crafting custom HTTP requests (GET/POST/PUT/DELETE) and header inspection. |
| `tech_detector.py` | Passive scanner detecting CMS, Frameworks, Web Servers, and WAF signatures. |
| `vuln_fuzzer.py` | Parameter vulnerability fuzzer for XSS, LFI, and Open Redirects. |
| `ai_hub.py` | Hub integrating 22+ leading AI search tools and models. |
| `shortcut_manager.py` | Dynamic keyboard shortcuts configuration dialog and JSON persistence. |
| `ad_blocker.py` | Network request interceptor blocking ad & tracking domains. |
| `split_screen.py` | Side-by-side dual view browser widget. |
| `script_injector.py` | Custom CSS & JavaScript injector tool. |
| `download_manager.py` | Video and file downloads tracking dashboard. |
| `path_utils.py` | Application installation path resolution for portable data storage. |
| `security_manager.py` | Blacklist URL filtering, HTTPS enforcement, and audit logs. |
| `site_scanner.py` | Domain passive reconnaissance and header inspector. |
| `traffic_monitor.py` | Real-time network request logger table. |
| `text_editor.py` | Payload Notebook pre-loaded with XSS/SQLi cheat sheets. |
| `bookmark_manager.py` | Bookmarks persistence and management interface. |
| `video_downloader.py` | Multi-threaded video downloading backend using `yt-dlp`. |
| `subdomain_finder.py` | Passive subdomain lookup tool via crt.sh API. |
| `theme_manager.py` | Custom QSS Cyberpunk theme generator and manager. |
| `snake_game.py` | Mini retro snake game for downtime breaks. |
| `homepage.html` | Dynamic startpage with speed dial shortcut tiles and modal. |
| `installer_setup.iss` | Inno Setup configuration script for building Windows installer wizard. |
| `TwinBrowser.spec` | PyInstaller standalone executable bundling specification. |

---

## ⚙️ Installation & Usage Instructions

### Option 1: Standalone Installer (.exe)
1. Download `TwinBrowserSetup.exe` or `TwinBrowser.exe` from the `installer_dist/` or `dist/` directory.
2. Run the Setup Wizard and choose your preferred installation drive (`C:`, `D:`, `E:`).
3. All user data, bookmarks, and downloads will be saved directly in the chosen folder.

### Option 2: Run from Python Source
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nimesh-Alwis/Twin-Browser.git
   cd Twin-Browser
   ```

2. **Install dependencies:**
   ```bash
   pip install PyQt6 PyQt6-WebEngine requests yt-dlp
   ```

3. **Launch TwinBrowser:**
   ```bash
   python main.py
   ```

---

## 💡 Why Twin-Browser?
Twin-Browser bridges the gap between a modern web browser and a comprehensive Ethical Hacking Suite. Instead of constantly switching between terminal windows, external proxy software, payload notes, AI web tools, and separate encoding sites, Twin-Browser integrates everything into a single, sleek, Cyberpunk-themed workspace!
