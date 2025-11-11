from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# --- Configure Chrome options ---
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# --- Load local HTML page ---
driver.get("file:///c%3A/Users/AS%20Gaming/Documents/CobaCaptchaV2/Info.html")  # replace with your HTML path

# --- Inject JS to fully neutralize fingerprinting and deny all permissions ---
neutralize_js = """
// --- Navigator ---
if(navigator){
    navigator.userAgent = null;
    navigator.userAgentData = null;
    navigator.platform = null;
    navigator.appVersion = null;
    navigator.vendor = null;
    navigator.hardwareConcurrency = 0;
    navigator.deviceMemory = 0;
    navigator.maxTouchPoints = 0;
    navigator.doNotTrack = null;
    navigator.webdriver = false;
    navigator.cookieEnabled = false;
    navigator.onLine = null;
    navigator.productSub = null;
    navigator.language = null;
    navigator.languages = [];
}

// --- Screen (set everything to 0) ---
if(screen){
    screen.width = 0;
    screen.height = 0;
    screen.availWidth = 0;
    screen.availHeight = 0;
    screen.colorDepth = 0;
    screen.pixelDepth = 0;
    screen.orientation = null;
    window.innerWidth = 0;
    window.innerHeight = 0;
    window.devicePixelRatio = 0;
}

// --- Time / Locale ---
Intl.DateTimeFormat = ()=>({resolvedOptions:()=>({timeZone:null})});
Date.prototype.getTimezoneOffset = ()=>0;
Date.prototype.toString = ()=>"";

// --- Connection ---
if(navigator.connection){ 
    navigator.connection.effectiveType = null;
    navigator.connection.downlink = 0;
    navigator.connection.rtt = 0;
    navigator.connection.saveData = false;
}

// --- Battery API ---
navigator.getBattery = undefined;

// --- Permissions API: auto deny everything ---
if(navigator.permissions){
    navigator.permissions.query = (params)=>Promise.resolve({state:"denied"});
}

// --- Storage API ---
if(navigator.storage){
    navigator.storage.estimate = ()=>Promise.resolve({quota:0, usage:0});
    navigator.storage.persisted = ()=>Promise.resolve(false);
}

// --- Media Devices ---
if(navigator.mediaDevices){
    navigator.mediaDevices.enumerateDevices = ()=>Promise.resolve([]);
}

// --- Canvas/WebGL ---
HTMLCanvasElement.prototype.toDataURL = ()=>'';
HTMLCanvasElement.prototype.getContext = ()=>null;

// --- Audio fingerprinting ---
window.OfflineAudioContext = function(){
    return {
        createOscillator: ()=>({connect:()=>{}, start:()=>{}}),
        createDynamicsCompressor: ()=>({connect:()=>{}}),
        startRendering: ()=>Promise.resolve({getChannelData:()=>[]})
    };
};

// --- WebRTC ---
window.RTCPeerConnection = function(){
    return {createDataChannel:()=>{}, createOffer:()=>Promise.resolve({}), setLocalDescription:()=>Promise.resolve({}), onicecandidate:null, close:()=>{}};
};

// --- Fetch / Public IP ---
window.fetch = function(url, opts){
    return Promise.resolve({json:()=>Promise.resolve({ip:"0.0.0.0"})});
};

// --- Storage tests ---
try{ localStorage.clear(); sessionStorage.clear(); } catch{}
"""

driver.execute_script(neutralize_js)

# --- Give page time to render normally ---
time.sleep(5123)

# --- Example: get sanitized page content ---
html_content = driver.page_source
print(html_content[:500])  # first 500 chars

# --- Close browser ---
driver.quit()
