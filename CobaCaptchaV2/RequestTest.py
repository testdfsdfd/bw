import requests

url = "https://moodle2.jdlm.qc.ca/login/index.php"

payload = {
    "username": "test",
    "password": "tes",
    "anchor": "",
    "logintoken": "hvEcsDGOPyAOEeYjr05MMPFiHAE9lpBM",
}

res = requests.get(url, data=payload)

print(res.status_code)