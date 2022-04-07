import json
import psycopg2
import sys
import timestamp
import cache

class Flow:
    def __init__(self, gateway, device, device_addr, application, port, type_message, message_quantity, size, active_time):
        
        self.gateway = gateway
        self.device = device
        self.device_addr = device_addr
        self.application = application
        self.port = port
        self.type_message = type_message
        self.message_quantity = message_quantity
        self.size = size
        self.active_time = active_time

def reg_database(flow, time):

    #Inicia conexão com o banco de dados.
    con = psycopg2.connect(
        database = cache.info_database,
        user = cache.info_user,
        password = cache.info_password,
        host = cache.info_host,
        port = cache.info_port)
    
    cur = con.cursor()

    gateway = str(flow.gateway)
    device = str(flow.device)
    device_addr = str(flow.device_addr)
    application = str(flow.application)
    port = str(flow.port)
    type_message = str(flow.type_message)
    message_quantity = int(flow.message_quantity)
    size_bytes = int(flow.size)
    time_stamp = time
    
    cur.execute("INSERT INTO fluxos (gateway, device, device_addr, application, port, type_message, message_quantity, size_bytes, time_stamp) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)", (gateway, device, device_addr, application, port, type_message, message_quantity, size_bytes, time_stamp))
    #Se compromete com as mudanças
    con.commit()
    #Finaliza a conexão com o banco de dados.
    cur.close()
    con.close()

def createFlow(lora):
    size = sys.getsizeof(lora)
    active_time = timestamp.timestamp()
    key = True

    lora_json = json.loads(lora)
    meta = json.dumps(lora_json["meta"])
    params = json.dumps(lora_json["params"])
    meta_json = json.loads(meta)
    params_json = json.loads(params)

    type_message = lora_json["type"]
    device = meta_json["device"]

    try:
        gateway = meta_json["gateway"]
    except:
        gateway = "null"

    try:
        device_addr = meta_json["device_addr"]
    except:
        device_addr = "null"
    
    try:
        port = str(int(params_json["port"]))
    except:
        port = "null"
    
    try:
        application = meta_json["application"]
    except:
        application = "null"
    
    for x in range(len(cache.cache)):
        if device_addr == cache.cache[x].device_addr and port == cache.cache[x].port:
            if gateway == cache.cache[x].gateway:
                if type_message == cache.cache[x].type_message:
                    cache.cache[x].message_quantity += 1
                    cache.cache[x].size += size
                    cache.cache[x].active_time = active_time
                    key = False

    cache.numero_mensagens += 1
    if key == True:            
        flow = Flow(gateway, device, device_addr, application, port, type_message, 1, size, active_time)
        return flow
    else:
        return None

def cacheClear(time):
    for i in range(len(cache.cache)):
        reg_database(cache.cache.pop(0), time)
    return

def reg_expire(time):
    key = True
    lenght = len(cache.cache)
    expire_time = cache.expire_time
    setup_time = timestamp.timestamp()
    flowing = False

    while(key):
        for x in range(lenght):
            if (setup_time - cache.cache[x].active_time) >= expire_time:
                reg_database(cache.cache.pop(x), time) #reg_database
                flowing = True
                break
        lenght -= 1

        if lenght == 0:
            key = False
    if flowing == True:
        cache.marcos_fluxos.append(time)
        cache.numero_fluxos += 1
        print(f"\n[CACHE EXPIRE FLUSH]")
    return