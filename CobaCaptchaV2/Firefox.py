from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random, time

# ---------- Choose a random, plausible user-agent ----------
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
]
ua = random.choice(user_agents)

# ---------- Firefox options (visible window) ----------
options = Options()
options.headless = False      # show the browser

# Privacy / anti-fingerprint preferences (no extra downloads required)
options.set_preference("general.useragent.override", ua)
options.set_preference("dom.webdriver.enabled", False)               # try to hide automation
options.set_preference("useAutomationExtension", False)
options.set_preference("privacy.resistFingerprinting", True)         # built-in spoofing
options.set_preference("media.peerconnection.enabled", False)        # disable WebRTC (IP leak prevention)
options.set_preference("permissions.default.geo", 2)                 # block geolocation
options.set_preference("dom.webnotifications.enabled", False)       # block notifications
options.set_preference("permissions.default.desktop-notification", 2)
options.set_preference("network.cookie.cookieBehavior", 1)           # block 3rd-party cookies
options.set_preference("browser.privatebrowsing.autostart", True)    # always private mode
options.set_preference("signon.rememberSignons", False)
options.set_preference("privacy.trackingprotection.enabled", True)  # tracking protection
options.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
options.set_preference("datareporting.healthreport.uploadEnabled", False)
options.set_preference("datareporting.healthreport.service.enabled", False)
options.set_preference("browser.formfill.enable", False)             # disable form autofill
options.set_preference("network.http.referer.spoofSource", True)     # reduce referer leakage

# Optional: keep browser window size consistent (reduces fingerprint variance)
options.set_preference("privacy.window.maxInnerWidth", 1280)
options.set_preference("privacy.window.maxInnerHeight", 800)

# ---------- Launch Firefox ----------
driver = webdriver.Firefox(options=options)

# Remove navigator.webdriver flag in page JS
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Extra defensive JS applied immediately to the loaded pages:
driver.execute_script("""
/* Neutralize some APIs so pages get limited info.
   This runs inside the browser context and helps reduce what pages can see.
*/
try {
  // make permissions.query always return denied
  if (navigator.permissions) {
    navigator.permissions.query = (p) => Promise.resolve({state: "denied"});
  }
} catch(e){}

try{
  // neutralize getBattery
  if(navigator.getBattery) navigator.getBattery = function(){ return Promise.reject('blocked'); };
}catch(e){}

try{
  // remove enumerateDevices labels
  if(navigator.mediaDevices) navigator.mediaDevices.enumerateDevices = ()=>Promise.resolve([]);
}catch(e){}

try{
  // stub out canvas getContext / toDataURL to reduce canvas fingerprinting
  HTMLCanvasElement.prototype.getContext = function(){ return null; };
  HTMLCanvasElement.prototype.toDataURL = function(){ return 'data:image/png;base64,'; };
}catch(e){}
""")

# ---------- Clear any leftover storage (start clean) ----------
try:
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear(); sessionStorage.clear();")
except Exception:
    pass

# ---------- Open a first page for you to check ----------
driver.get("https://browserleaks.com/")   # you can change or remove this

print("Browser opened visibly with privacy prefs set.")
print("User-Agent:", ua)
print("Notes: WebRTC disabled, private mode enabled, 3rd-party cookies blocked.")
print("Reminder: your IP address is still the machine's unless you use a VPN/proxy/Tor.")

# Keep browser open for manual browsing. Close manually or press Enter here to quit.
try:
    input("Press Enter here to close the browser and quit Selenium...")
finally:
    driver.quit()
