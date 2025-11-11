from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import random, time

# --- Random plausible user agent ---
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
]
ua = random.choice(user_agents)

# --- Firefox options (headless for Render) ---
options = Options()
options.headless = False

options.set_preference("general.useragent.override", ua)
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("privacy.resistFingerprinting", True)
options.set_preference("media.peerconnection.enabled", False)
options.set_preference("permissions.default.geo", 2)
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("permissions.default.desktop-notification", 2)
options.set_preference("network.cookie.cookieBehavior", 1)
options.set_preference("browser.privatebrowsing.autostart", True)
options.set_preference("privacy.trackingprotection.enabled", True)
options.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
options.set_preference("datareporting.healthreport.uploadEnabled", False)
options.set_preference("browser.formfill.enable", False)
options.set_preference("privacy.window.maxInnerWidth", 1280)
options.set_preference("privacy.window.maxInnerHeight", 800)

# --- Start Firefox ---
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# --- JS tweaks ---
driver.execute_script("""
try { navigator.permissions.query = (p) => Promise.resolve({state: "denied"}); } catch(e){}
try { if(navigator.getBattery) navigator.getBattery = function(){return Promise.reject('blocked');}; } catch(e){}
try { if(navigator.mediaDevices) navigator.mediaDevices.enumerateDevices = ()=>Promise.resolve([]); } catch(e){}
try {
  HTMLCanvasElement.prototype.getContext = function(){return null;};
  HTMLCanvasElement.prototype.toDataURL = function(){return 'data:image/png;base64,';};
} catch(e){}
""")

# --- Open target page ---
driver.get("https://browserleaks.com/")

print("✅ Browser started successfully!")
print("User-Agent:", ua)
print("Page title:", driver.title)

# --- Wait, then exit ---
time.sleep(5112323)
driver.quit()
