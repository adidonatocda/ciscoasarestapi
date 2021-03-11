#You will need to have HashiCorp Vault Setup use Vaulting

import random
import string
import requests
import urllib3
from pprint import pprint
import json
import getpass
from CDAASARESTAPIVaultCreds import token
#For the sake of demonstration I created a  CDAASARESTAPIVaultCreds.py file in the same directory to import ("from CDAASARESTAPIVaultCreds import token"). One variable defined: "token = 's.ZcfJ4QXOg2YmS7QtAjwYpE5c'
#All creds including this token are not real credentials anymore. I just posted for example purposes.


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_VAULT_URL = 'http://127.0.0.1:8200/v1/secret/data/'
VAULT_HEADERS = {"X-Vault-Token": token}
#VAULT_JSON_DATA = {"data": {"pword": "MySuperSecretPassword)(*&^%$#@!!"}}
#VAULT_R = requests.post(url = 'http://127.0.0.1:8200/v1/secret/data/SecOps500', json=json_data, headers = HEADERS)


log_file = "fwbackuplog.txt"
link_log_file = "lnk.log"
user_log = "user.log"
headers = {'Content-Type': 'application/json', 'User-Agent':'REST API Agent'}
cli_path = "/api/cli/"
api_path = "/api/mgmtaccess/hosts/"
user_path = "/api/objects/localusers/"
openlog = open(log_file, "w")
payload = {"commands":["show run user"]}
backup_payload = {"commands": ["show run"]}


fw_user=input("Username: ")
try:
    fw_pwd=getpass.getpass(prompt='Password: ', stream=None)
    en_pwd=getpass.getpass(prompt='Enable Password: ', stream=None)
except Exception as error:
    print ('ERROR',error)


def get_backups():
    #openlog=open(log_file, "a")
    fw_openlog = open(log_file, "a")
    hosts_file = open('hosts.txt', 'r+')
    with open('hosts.txt') as hosts_file:
        hosts_array = hosts_file.read().splitlines()
        for host in hosts_array:
                url = "https://"+ host + cli_path
                print(" ")
                backupresponse = requests.post(url, auth=(fw_user, fw_pwd), data=json.dumps(backup_payload), headers=headers, verify=False)
                #DEMO without PrettyPrint
                #print(backupresponse.content)
                print('###### SEPARATOR ##############')
                print(backupresponse.text)
                print('###### SEPARATOR ##############')
                backup_data = json.loads(backupresponse.text)
                #DEMO with PrettyPrint
                pprint(backup_data['response'])
                fw_openlog.write(backupresponse.text)
    openlog.close()
    print(" ")
    pass


def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for p in range(length))
    print(password)
    return password


def get_mgmtdata():
    openlog = open(link_log_file, "a")
    hosts_file = open('hosts.txt', 'r+')
    with open('hosts.txt') as hosts_file:
        hosts_array = hosts_file.read().splitlines()
        for host in hosts_array:
                url = "https://"+ host + api_path
                print(" ")
                mgmtresponse = requests.get(url,auth=(fw_user, fw_pwd),verify=False)
                data = json.loads(mgmtresponse.text)
                print(data['selfLink'])
                for i in data['items']:
                    print("type : " + i["type"],i["ip"]["value"],i["netmask"]["value"],i["interface"]["name"])
                    strType=i["type"]
                    strIP=i["ip"]["value"]
                    strNM=i["netmask"]["value"]
                    strInt=i["interface"]["name"]
                    openlog.write("Type: %s\tIP: %s\tNetmask: %s\tInterface: %s \n" % (strType,strIP,strNM,strInt))
                    openlog.write("\n")
    openlog.close()
    print(" ")


def update_passwords():
    openlog=open(user_log, "a")
    hosts_file = open('hosts.txt', 'r+')
    with open('hosts.txt') as hosts_file:
        hosts_array = hosts_file.read().splitlines()
        for host in hosts_array:
                url = "https://"+ host + user_path
                print("")
                print(url)
                userreq = requests.get(url, auth=(fw_user, fw_pwd), headers=headers, verify=False)
                #usernameres = json.loads(userreq.text)
                usernameres = userreq.json()
                for i in usernameres['items']:
                    print("Username : " + i["name"], ",Privilege Level : ", i["privilegeLevel"])
                    str_username =i["name"]
                    str_privilegeLevel = i["privilegeLevel"]
                    openlog.write("Url: %s \tUsername: %s\tPrivelege Level: %s \n" % (url,str_username,str_privilegeLevel))

                print("")
                for j in usernameres['items']:
                    username = j["name"]
                    privilege = j["privilegeLevel"]
                    password = get_random_password_string(16)
                    cmdline = f"username {username} password {password} privilege {privilege}"
                    newcli = '"'+ cmdline + '"'
                    _jsonpayload = "{"+ '"'+"commands"+'"'+':'+"[" + newcli +"]}"
                    print(_jsonpayload)
                    openlog.write(_jsonpayload)
                    # 3/7/2021
                    #UPDATES with Vault
                    VAULT_JSON_DATA = {"data": {"pword": password}}
                    VAULT_Cred_Path = BASE_VAULT_URL+host+"_"+username
                    VAULT_R = requests.post(url=VAULT_Cred_Path, json=VAULT_JSON_DATA, headers=VAULT_HEADERS)
                    VAULT_R_response = VAULT_R.json()
                    print(VAULT_R.content)
                    #
                    for host in hosts_array:
                        pwdurl = "https://"+ host + cli_path
                        #print(pwdurl)
                        requests.post(pwdurl, auth=(fw_user, fw_pwd), data=_jsonpayload, headers=headers, verify=False)
                    openlog.write("\n")
                print("")
    openlog.close()
print(" ")


if __name__ == "__main__":
  #You will need to uncomment the functions to get them to run!
    # get_random_password_string(64)
    #get_backups()# Back it up before you start.
    #get_mgmtdata()#Get Management Access Information
    #update_passwords()#This will change all passwords returned for any local accounts on the ASA!
