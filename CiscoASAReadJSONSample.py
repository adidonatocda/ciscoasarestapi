import json

mgmt_access_json = """{
  "kind": "collection#DevMgmtTraffic",
  "selfLink": "https://192.168.0.105/api/mgmtaccess/hosts/",
  "rangeInfo": {
    "offset": 0,
    "limit": 2,
    "total": 2
  },
  "items": [
    {
      "kind": "object#DevMgmtTraffic",
      "selfLink": "https://192.168.0.105/api/mgmtaccess/hosts/3969558105",
      "type": "http",
      "ip": {
        "kind": "AnyIPAddress",
        "value": "any"
      },
      "netmask": {
        "kind": "IPv4NetMask",
        "value": "0.0.0.0"
      },
      "interface": {
        "kind": "objectRef#Interface",
        "refLink": "https://192.168.0.105/api/interfaces/physical/GigabitEthernet0_API_SLASH_0",
        "objectId": "GigabitEthernet0_API_SLASH_0",
        "name": "inside"
      },
      "objectId": "3969558105"
    },
    {
      "kind": "object#DevMgmtTraffic",
      "selfLink": "https://192.168.0.105/api/mgmtaccess/hosts/177896665",
      "type": "ssh",
      "ip": {
        "kind": "IPv4Address",
        "value": "192.168.0.0"
      },
      "netmask": {
        "kind": "IPv4NetMask",
        "value": "255.255.255.0"
      },
      "interface": {
        "kind": "objectRef#Interface",
        "refLink": "https://192.168.0.105/api/interfaces/physical/GigabitEthernet0_API_SLASH_0",
        "objectId": "GigabitEthernet0_API_SLASH_0",
        "name": "inside"
      },
      "objectId": "177896665"
    }
  ]
}"""
data = json.loads(mgmt_access_json)
#print(data)
#print(" ")
for i in data['items']:
    print("type : " + i["type"], i["ip"]["value"], i["netmask"]["value"], i["interface"]["name"])





