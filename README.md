# Twin-Browser Secure v1.6 🌐🛡️

**Twin-Browser Secure** is a custom-built, security-focused web browser developed using Python and PyQt6. Designed specifically for cybersecurity students and researchers, it integrates essential reconnaissance tools and security protocols directly into the browsing experience.



## 🚀 Features

### 🛡️ Security & Privacy
* **Enforced HTTPS:** Automatically upgrades insecure connections to HTTPS to ensure data encryption.
* **URL Safety Guard:** Built-in security manager that cross-references URLs against a blacklist to block malicious sites.
* **History Logging:** Maintains a local audit trail of browsing activity for session tracking.

### 🔍 Reconnaissance Tools
* **Site Inspector:** One-click tool to extract IP addresses, server headers, and security configurations (HSTS, etc.) of any website.
* **Network Traffic Monitor:** A real-time dashboard to inspect outgoing HTTP requests, methods (GET/POST), and server response statuses.
* **Payload Notebook:** A built-in library for security researchers to store and quickly access common payloads like XSS and SQLi strings.

### ⚡ Productivity & UX
* **Cyberpunk UI:** A high-contrast, neon-styled dark theme designed for long research sessions.
* **Bookmark Manager:** Save and categorize critical research links and tools.
* **Integrated Notes:** A simple text editor to jot down findings without leaving the browser.
* **Easter Egg:** Includes a classic Snake game for quick breaks during intensive tasks.



## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Framework:** PyQt6 (GUI)
* **Web Engine:** QtWebEngine (Chromium-based)
* **Libraries:** Requests, Socket (for network scanning)

## 📂 Project Structure

| File | Function |
| :--- | :--- |
| `main.py` | Entry point and core application controller. |
| `ui_components.py` | Manages the custom navigation bar and UI layout. |
| `browser_engine.py` | Handles web rendering and network signals. |
| `security_manager.py` | Logic for URL filtering and protocol enforcement. |
| `site_scanner.py` | Module for domain information gathering. |
| `traffic_monitor.py` | Real-time network request logger. |
| `text_editor.py` | The Payload Notebook and note-taking tool. |
| `bookmark_manager.py` | Data persistence for saved URLs. |
| `snake_game.py` | The internal mini-game logic. |

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Twin-Browser.git](https://github.com/your-username/Twin-Browser.git)
   cd Twin-Browser

   Install dependencies:

Bash
pip install PyQt6 PyQt6-WebEngine requests
Run the application:

Bash
python main.py


### Pro-Tips for your GitHub:

1.  **Screenshots:** GitHub users love visuals. Since you have that cool Cyberpunk theme, take a screenshot of the browser and the Network Monitor and add them to your repository. You can link them in the README using `![Alt Text](path/to/image.png)`.
2.  **Commit Message:** When you push this file, use a professional message:
    `docs: add comprehensive README with feature list and installation guide`
3.  **License:** It is a good habit to add a `LICENSE` file (like MIT) to your repo so people know how they can use your code.

