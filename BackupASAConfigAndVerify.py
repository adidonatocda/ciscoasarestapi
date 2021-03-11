from pprint import pprint
import requests
import urllib3
import json
import getpass
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
asa_headers = {'Content-Type': 'application/json', 'User-Agent': 'REST API Agent'}
asa_cli_uri = "/api/cli"
asa_backup_uri = "/api/backup"
asa_host = "172.16.122.10"
asa_cfg_url = "https://" + asa_host + asa_cli_uri
asa_backup_url = "https://" + asa_host + asa_backup_uri
asa_user = input("ASA Username: ")
config_payload = {
    "commands": [
        "show run"
    ]
}
backup_payload = {
    "passphrase": "123456",
    "location": "disk0:/backup2.cfg"
}
verify_payload = {
  "commands": [
    "show disk"
  ]
}

#{"commands": ["show run"]}
#https://172.16.122.10/api/backup
#{"passphrase": "123456", "location": "disk0:/backup.cfg"}

try:
    asa_pwd = getpass.getpass(prompt='ASA Password: ', stream=None)
except Exception as error:
    print('ERROR', error)

old_config = ''
config_log = ''
time_str = time.strftime("%Y%m%d-%H%M%S")
job_file = time_str + ".txt"
f = open(job_file, "w", encoding='utf-8')

def get_config():
    asa_config_request = requests.post(asa_cfg_url, auth=(asa_user, asa_pwd), json=config_payload, headers=asa_headers, verify=False)
    #print(asa_config_request)
    print("========Ugly JSON =====================")
    print(asa_config_request.text)
    print("========Pretty JSON==========")
    config_json = json.loads(asa_config_request.text)
    pprint(config_json)
    f.write(asa_config_request.text)
    #str_config_json = json.dumps(config_json, indent=2)

def back_up():
    asa_backup_request = requests.post(asa_backup_url, auth=(asa_user, asa_pwd), json=backup_payload, headers=asa_headers, verify=False)
    #print(asa_backup_request)
    print("==================================================")
    print("Backup Status: ", asa_backup_request.status_code)
    print("==================================================\n")

def verify_backup():
    asa_backup_request = requests.post(asa_cfg_url, auth=(asa_user, asa_pwd), json=verify_payload, headers=asa_headers, verify=False)
    #print(asa_backup_request)
    print("================== Backup Verification ============\n")
    backup_json = json.loads(asa_backup_request.text)
    print(backup_json,'\n')
    print("======Pretty JSON Backup Verification ============\n")
    f.write(asa_backup_request.text)
    pprint(backup_json)



#get_config()
#back_up()
verify_backup()


