# 🌐 Twin-Browser Secure v1.6

<div align="center">
  <p>A custom-built, security-focused web browser developed using Python and PyQt6. Designed specifically for cybersecurity students, researchers, and developers, it integrates essential reconnaissance tools, security protocols, user-agent spoofing, media downloading, and productivity utilities directly into the browsing experience.</p>
</div>

---

## 🚀 Key Features

### 🛡️ Security & Privacy
* **URL Safety Guard:** Built-in security manager that cross-references URLs against a blacklist to block known malicious and phishing sites.
* **Enforced HTTPS:** Automatically upgrades insecure `http://` connections to `https://` to ensure data encryption.
* **User-Agent Spoofing:** Instantly disguise your browser's identity. Built-in profiles include Google Chrome, iPhone Safari, Googlebot, and cURL to seamlessly test how websites respond.
* **Traffic Monitoring:** A real-time dashboard to inspect outgoing HTTP requests, HTTP methods (GET/POST), and server response statuses.
* **History Auditing:** Maintains a local audit trail of browsing activity for session tracking.

### 🔍 Reconnaissance Tools
* **Site Scanner:** One-click tool to passively extract IP addresses, detect server technology (Server headers), check HTTP status codes, and verify security configurations like HSTS of any website.
* **Payload Notebook:** A built-in text editor (`text_editor.py`) for security researchers to jot down notes or temporarily store and quickly access common payloads (e.g., XSS, SQLi strings) without leaving the browser tab.

### ⚡ Media & Productivity
* **Built-in Video Downloader:** Seamlessly download videos from supported sites using the integrated `yt-dlp` module. Features a built-in progress bar, download speed indicator, and dynamic quality selection!
* **Bookmark Manager:** Quickly save, access, and categorize your favorite links or critical research targets.
* **Home Navigation:** Quickly jump back to your standard homepage (`Google`) with a dedicated Home button.

### 🎮 Ultimate UX
* **Cyberpunk UI Theme:** A gorgeous, high-contrast, neon-styled dark theme using clean QSS (Qt Style Sheets) designed for long, eye-strain-free research sessions.
* **Easter Egg:** Feeling exhausted during a bug bounty hunt? Fire up the built-in **Snake Game** for a quick break!

---

## 🛠️ Tech Stack Architecture

* **Language:** `Python 3.11+`
* **GUI Framework:** `PyQt6`
* **Web Engine:** `PyQt6-WebEngine` (Chromium-based rendering)
* **Networking Modules:** `socket`, `requests` (for reconnaissance scanning)
* **Media Handling:** `yt-dlp` (for the multi-threaded video downloader module)

## 📂 Project Structure

| File / Directory | Function |
| :--- | :--- |
| `main.py` | Entry point. Wires the UI, WebEngine, and overarching Cyberpunk styles. |
| `ui_components.py` | Manages the custom Navigation Bar, User-agent ComboBox, & UI layout. |
| `browser_engine.py` | Handles web rendering, traffic signals, and profile manipulation. |
| `security_manager.py` | Logic for URL filtering, HTTPS enforcement, and visit logging. |
| `site_scanner.py` | Module for passive domain information gathering and header checks. |
| `traffic_monitor.py` | Real-time network request logger table GUI. |
| `text_editor.py` | The Payload Notebook and note-taking tool interface. |
| `bookmark_manager.py` | Data persistence and GUI for viewing saved URLs. |
| `video_downloader.py` | Multi-threaded media downloader logic using `yt-dlp`. |
| `snake_game.py` | The internal mini-game logic. |
| `downloads/` | Auto-generated directory where downloaded media is saved. |

---

## ⚙️ Installation & Usage Instructions

### Prerequisites
Make sure you have **Python 3.11** or newer installed on your system.

### 1. Clone the repository:
```bash
git clone https://github.com/Nimesh-Alwis/Twin-Browser.git
cd Twin-Browser
```

### 2. Install required dependencies:
Install the required libraries utilizing pip:
```bash
pip install PyQt6 PyQt6-WebEngine requests yt-dlp
```

### 3. Run the application:
Launch the browser by executing the main script:
```bash
python main.py
```

---

## 💡 Why Twin-Browser?
Twin-Browser bridges the gap between a standard web browser and an offensive security tool. Instead of repeatedly switching windows between your browser, terminal, payload notes, and proxy tools, you get all the fundamental reconnaissance and research tools integrated into a single, cohesive, Cyberpunk-themed interface.
