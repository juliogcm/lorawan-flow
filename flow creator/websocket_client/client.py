import cache
import timer
import lora
import websockets
import asyncio
import threading
import keyboard
import timestamp

def thread_function():
    while (not cache.stop_thread):
        timer.countdown(cache.t)  

def thread_function_killer():
    while (not cache.stop_thread): 
        record = keyboard.record(until = 'q')
        record = str(record[0])

        if record == "KeyboardEvent(q down)" or record == "KeyboardEvent(q up)":  
            print('\nYou terminated the program!\nGoodbye\n.')
            cache.stop_thread = True
            break 

def thread_function_bdreg():
    while (not cache.stop_thread):    
        if cache.time_thread == True:
            time = timestamp.timestamp()
            cache_len = len(cache.cache)
            if cache_len > 0:
                print("\n[CACHE FLUSH]")
                lora.cacheClear(time)  
            else:
                print("\n[CACHE FLUSH EMPTY]")
            cache.marcos_fluxos.append(time)
            cache.numero_fluxos += 1
            cache.time_thread = False
        
        #if cache.expire_thread == True:
        #    time = timestamp.timestamp()
        #    cache_len = len(cache.cache)
        #    if cache_len > 0:
        #        lora.reg_expire(time)  
        #    cache.expire_thread = False

        if len(cache.cache) >= cache.cache_max_size :
            time = timestamp.timestamp()
            cache_len = len(cache.cache)
            if cache_len > 0:
                print("\n[CACHE SIZE FLUSH]")
                lora.cacheClear(time)  
            print("\n[CACHE SIZE FLUSH EMPTY]")
            cache.marcos_fluxos.append(time)
            cache.numero_fluxos += 1

    return

def main():
    x = threading.Thread(target=thread_function)
    #y = threading.Thread(target=thread_function_killer)
    z = threading.Thread(target = thread_function_bdreg)
    #y.start()
    z.start()
    x.start()

    #Define uma função assíncrona que se conecta ao seridor e lida com as informações que chegam.
    async def listen():    
        #Conecta ao servidor.
        async with websockets.connect(cache.url, ping_interval=None) as ws:
            await ws.send("") #conexão de testes
            #Faz com que a execução seja contínua e que se escute todas as mensagens que chegam.
            while (not cache.stop_thread):
                print("Listening")
                if cache.stop_thread == True:
                    return
                msg = await ws.recv()

                #Verifica se é uma mensagem de erro. Caso não seja, criar fluxo e armazena na cache.
                fluxo = lora.createFlow(msg)
                    
                if fluxo != None:
                    cache.cache.append(fluxo)

                print("\nFLOW UPDATED TO CACHE:\n---------------------------")
                print(f"\n Último fluxo em: {cache.marcos_fluxos} | Fluxos registrados: {cache.numero_fluxos} | Mensagens totais: {cache.numero_mensagens}\n")
    #It will run the function "listen()" and it will wait until it is completed.
    #We need a connection wich is asyn, and we need a received message wich is also async.
    asyncio.get_event_loop().run_until_complete(listen())
if __name__ == "__main__":
    main()