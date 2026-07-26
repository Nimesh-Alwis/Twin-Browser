from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class AdBlockerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, enabled=True):
        super().__init__()
        self.enabled = enabled
        self.ad_domains = [
            "doubleclick.net",
            "googlesyndication.com",
            "google-analytics.com",
            "adservice.google.com",
            "adnxs.com",
            "popads.net",
            "popcash.net",
            "adform.net",
            "rubiconproject.com",
            "outbrain.com",
            "taboola.com",
            "criteo.com",
            "pubmatic.com",
            "openx.net",
            "mediavine.com",
            "exoclick.com",
            "propellerads.com",
            "scorecardresearch.com"
        ]

    def interceptRequest(self, info):
        if not self.enabled:
            return
        url_str = info.requestUrl().toString().lower()
        for domain in self.ad_domains:
            if domain in url_str:
                info.block(True)
                return

    def set_enabled(self, enabled):
        self.enabled = enabled
