import socket
import threading

HOST="localhost"
PORT=5050

def recibir(datos:socket.socket):
   
   while True:
        try:
            data=datos.recv(1024)
            if not data:
                print("[ERROR DE CONEXION]")
        except Exception:
            print("[ERROR DE CONEXION]")
        else:
            mensaje=data.decode()
            print("[Nuevo mensaje]= ",mensaje)
    


def main():
    usuario=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        print("[Conectando al servidor...]")
        usuario.connect((HOST,PORT))
    except ConnectionRefusedError:
        print("[-Servidor no responde-]")
    else:
        print("[Conexion exitosa]")
        print("[Escriba"," salir"," para cerrar. ")

    hilo=threading.Thread(target=recibir,args=usuario,daemon=True)

    try:
        while True:
            mensajes=input("<Mensaje>= ")
            if mensajes.strip().lower()=="salir":
                usuario.close()
                break
            try:
                usuario.send(mensajes.encode())
            except Exception:
                print("[No se pudo enviar el mensaje]")
                break
    except KeyboardInterrupt:
        usuario.close()
    finally:
        usuario.close()
main()