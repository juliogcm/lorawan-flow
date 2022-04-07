cache = []
stop_thread = False         #key to stop all threads
time_thread = False         #key to save data to the database
expire_thread = False       #key to expire data to the database

marcos_fluxos = [0]          #armazena os tempos de iníco de um fluxo
numero_fluxos = 0           #conta quantos fluxos existiram até agora
numero_mensagens = 0        #número total de imagens

#Tempo definido em segundos
t = 1800                       #30 minutos (1800 s) é o tempo que um fluxo passa na cache.
cache_max_size = 65536              #Number of entries to maintain in the NetFlow cache. The valid range is 1024 to 524288 entries. The default is 65536 (64 K).
expire_time = 16

#Url recebe o endereço do servidor do websocket.
url = "ws://localhost:8765"

info_database = "banco_lora"
info_user = "postgres"
info_password = "123010"
info_host = "localhost"
info_port = "5432"




