import socket 

HOST="localhost"
PORT=5050

socket_client=None

BufferSize=4096

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    server.bind((HOST,PORT))
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    server.listen()
    print("[--Servidor Activo--]")


    try:
        socket_cliente,direccion=server.accept()
        print(f"[Usuario Conectado({direccion})]")
        with open("recibido.bin","wb") as archivo:
            while True:
                data=socket_cliente.recv(BufferSize)
                if not data:
                    print(f"[Usuario ({direccion}) cerro la conexion]")
                    break
                archivo.write(data)
    except Exception:
        print("[FALLO DE CONEXION]")
    finally:
        if socket_client is not None:
            socket_cliente.close()
            server.close()
if __name__ == "__main__":
    main()

