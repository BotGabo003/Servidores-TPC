import socket

HOST="localhost"
PORT=5050
BUFFER=4096
ARCHIVO="Archivo.pdf"


def main():
    cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        print(f"[Conectando al servidor...]")
        cliente.connect((HOST,PORT))
        print("[Servidor conectado]")

        with open(ARCHIVO,"rb") as archivo:
            while True:
                data=archivo.read(BUFFER)
                if not data:
                    break
                cliente.sendall(data)
                print(f"[Archivo Enviado]")
    except FileNotFoundError:
        print(f"[ARCHIVO NO ENCONTRADO]")
    except ConnectionRefusedError:
        print("[SERVIDOR APAGADO]")
    except Exception:
        print("[ERROR DE CONEXION]")
    finally:
        cliente.close()
        print("[CONEXION TERMINADA]")
if __name__== "__main__":
    main()