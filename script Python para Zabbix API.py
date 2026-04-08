import requests
import json

# === CONFIGURAÇÕES ===
ZABBIX_URL = "http://SEU_ZABBIX/zabbix/api_jsonrpc.php"  # URL do seu Zabbix
ZABBIX_USER = "admin"
ZABBIX_PASS = "senha"

HOST_ID = "10105"  # ID do host no qual vai criar o item
ITEM_NAME = "Check CPU Load"
ITEM_KEY = "system.cpu.load[percpu,avg1]"
ITEM_TYPE = 0  # 0 = Zabbix agent
ITEM_VALUE_TYPE = 3  # 3 = numeric float

TRIGGER_NAME = "CPU Load too high"
TRIGGER_EXPRESSION = f"{{{{{HOST_ID}:{ITEM_KEY}.last()}}}} > 5"

# === LOGIN NA API ===
def login():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"user": ZABBIX_USER, "password": ZABBIX_PASS},
        "id": 1
    }
    response = requests.post(ZABBIX_URL, json=payload)
    return response.json()['result']

# === CRIAR ITEM ===
def create_item(auth_token):
    payload = {
        "jsonrpc": "2.0",
        "method": "item.create",
        "params": {
            "name": ITEM_NAME,
            "key_": ITEM_KEY,
            "hostid": HOST_ID,
            "type": ITEM_TYPE,
            "value_type": ITEM_VALUE_TYPE,
            "delay": "30s"
        },
        "auth": auth_token,
        "id": 2
    }
    response = requests.post(ZABBIX_URL, json=payload)
    return response.json()

# === CRIAR TRIGGER ===
def create_trigger(auth_token):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.create",
        "params": {
            "description": TRIGGER_NAME,
            "expression": TRIGGER_EXPRESSION,
            "priority": 4  # High
        },
        "auth": auth_token,
        "id": 3
    }
    response = requests.post(ZABBIX_URL, json=payload)
    return response.json()

# === EXECUÇÃO ===
if __name__ == "__main__":
    token = login()
    print("Token de login:", token)

    item_result = create_item(token)
    print("Resultado da criação do item:", json.dumps(item_result, indent=4))

    trigger_result = create_trigger(token)
    print("Resultado da criação do trigger:", json.dumps(trigger_result, indent=4))