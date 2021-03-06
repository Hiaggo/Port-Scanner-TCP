import sys
import socket
import threading
from queue import Queue

portasAbertas = []
portasFechadas = []
portasFiltradas = []
resultadoDasPortas = []
filaDePortas = Queue()


def threader(servidor, tid):
    while True:
        porta = filaDePortas.get()
        verificaPorta(servidor, porta, tid)
        filaDePortas.task_done()

def verificaPorta(servidor, porta, tid):
    try:
        # O programa irá escanear portas de min até max+1
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(20)

        _socket.connect((servidor, porta))
        
    except TimeoutError:  
        portasFiltradas.append(porta)

    except:
        portasFechadas.append(porta)

    else:
        portasAbertas.append(porta)
        
    finally:
        _socket.close()


def main():
    # Recebe as informações de host e da faixa de números de porta a serem analisados
    servidor = socket.gethostbyname(sys.argv[1]) 
    min = int(sys.argv[2])
    max = int(sys.argv[3])
    threadNumber = int(sys.argv[4])

    print("Escaneando o servidor {} no intervalo [{}, {}].".format(servidor, min, max))
    
    # Criamos aqui threadNumber threads para acelerar o processo de análise,
    #  atribuindo para cada thread uma porta da faixa
    for x in range(threadNumber):
        thread = threading.Thread(target=threader, args=(servidor, x,), daemon=True)
        thread.start()
    
    for porta in range(min, max + 1):       
        filaDePortas.put(porta)
    
    filaDePortas.join()

    # Print dos resultados
    print("\n       Portas abertas: {}".format(len(portasAbertas)))
    
    print("-" * (34 + len(str(max))))
    portasAbertas.sort()
    for porta in portasAbertas:
        print("| O status porta {} é aberta. |".format(porta))
    print("-" * (34 + len(str(max))))
    
    print("\n       Portas filtradas: {}".format(len(portasFiltradas)))
    
    print("-" * (34 + len(str(max))))
    portasFiltradas.sort()
    for porta in portasFiltradas:
        print("| O status da porta {} é filtrada. |".format(porta))
    print("-" * (34 + len(str(max))))

    print("\n       Portas fechadas: {}".format(len(portasFechadas)))
    
    print("-" * (34 + len(str(max))))
    portasFechadas.sort()
    for porta in portasFechadas:
        print("| O status da porta {} é fechada. |".format(porta))
    print("-" * (34 + len(str(max))))


main()
