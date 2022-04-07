import pandas as pd
import json
import websockets
import asyncio
import time

speed = 1
df = pd.read_csv("dados_filtrados.csv")
df['params.payload'].fillna('', inplace=True)
df['params.encrypted_payload'].fillna('', inplace=True)
lista = []

async def echo(websocket):
    async for message in websocket:
        #Função para retornar uma Series do DataFrame.
        for indx, fila in df.iterrows():
            outdated = fila['meta.outdated']
            tipo = fila['type']
            if(str(tipo) == "downlink"):
                
                fila.drop(['params.tx_time', 'params.max_size', 'params.message',
                        'params.code', 'params.duplicate', 'params.radio.hardware.immediately', 
                        'params.counter_up', 'params.rx_time', 'meta.outdated'], inplace=True)
            else:
                if(str(tipo) == "uplink"):
                    if(outdated != True):
                        fila.drop(['meta.outdated'], inplace=True)
                    fila.drop(['params.tx_time', 'params.max_size', 'params.message',
                            'params.code', 'params.radio.modulation.inverted', 'params.radio.hardware.immediately',
                            'params.counter_down', 'params.radio.hardware.power', 'params.radio.datr'], inplace=True)
                else:
                    if(str(tipo) == "downlink_request"):

                        fila.drop(['meta.outdated', 
                                'params.payload', 'params.encrypted_payload', 'params.rx_time',
                                'params.counter_up', 'params.port', 
                                'params.radio.time', 'params.radio.freq',
                                'params.radio.modulation.type', 'params.radio.modulation.bandwidth',
                                'params.radio.modulation.spreading', 'params.radio.modulation.coderate',
                                'params.radio.hardware.chain','params.radio.hardware.power', 'params.radio.hardware.immediately', 
                                'params.radio.hardware.channel', 'params.radio.hardware.tmst', 'params.radio.hardware.status',
                                'params.radio.hardware.rssi', 'params.radio.hardware.snr',
                                'params.radio.datarate', 'params.radio.delay', 'params.radio.size',
                                'params.radio.modulation.inverted',
                                'params.radio.hardware.gps.lat', 'params.radio.hardware.gps.lng',
                                'params.radio.hardware.gps.alt', 'params.radio.datr',
                                'params.radio.gps_time', 'params.message', 'params.code',
                                'params.duplicate'], inplace=True)
                    else:
                        if(str(tipo) == "error"):

                            fila.drop(['meta.outdated', 
                                    'params.payload', 'params.encrypted_payload', 'params.rx_time',
                                    'params.counter_up', 'params.counter_down', 'params.port', 
                                    'params.radio.time', 'params.radio.freq',
                                    'params.radio.modulation.type', 'params.radio.modulation.bandwidth',
                                    'params.radio.modulation.spreading', 'params.radio.modulation.coderate',
                                    'params.radio.hardware.chain','params.radio.hardware.power', 'params.radio.hardware.immediately', 
                                    'params.radio.hardware.channel', 'params.radio.hardware.tmst', 'params.radio.hardware.status',
                                    'params.radio.hardware.rssi', 'params.radio.hardware.snr',
                                    'params.radio.datarate', 'params.radio.delay', 'params.radio.size',
                                    'params.radio.modulation.inverted',
                                    'params.radio.hardware.gps.lat', 'params.radio.hardware.gps.lng',
                                    'params.radio.hardware.gps.alt', 'params.radio.datr',
                                    'params.radio.gps_time', 'params.tx_time', 'params.max_size',
                                    'params.duplicate'], inplace=True)

            checked = {}
    
                #Retornar os valor e indices da Series criada
            for col_label,v in fila.items():
                #Separar os campos do JSON em Keys de um Dict reconhecendo o "." como separador
                keys = col_label.split(".")

                atual = checked
                        
                for i, k in enumerate(keys):
                    if i==len(keys)-1:
                        atual[k] = v
                    else:
                        if k not in atual.keys():
                            atual[k] = {}
                        atual = atual[k]

            print(indx)
            print(json.dumps(checked, indent = 1).replace(': NaN', ': null'))
            await websocket.send(json.dumps(checked, indent = 1).replace(': NaN', ': null'))
            tempo = df.iloc[indx+1]['meta.time'] - df.iloc[indx]['meta.time']
            time.sleep(tempo / speed)
            
async def main():
    async with websockets.serve(echo, "localhost", 8765,ping_interval=None):
        await asyncio.Future()

asyncio.run(main())