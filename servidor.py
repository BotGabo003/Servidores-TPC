import socket
import selectors

HOST="localhost"
PORT=5050
sockets=[]
clientes={}
selector=selectors.DefaultSelector()

def aceptar(socket_recibido:socket.socket):
    sock,direccion=socket_recibido.accept()
    print(f"[Usuario conectado({direccion})]")
    sock.setblocking(False)
    sockets.append(sock)
    clientes[sock]=direccion
    selector.register(sock,selectors.EVENT_READ,manejar_cliente)



def manejar_cliente(socket_recibido:socket.socket):
    try:
        data=socket_recibido.recv(1024)
        if not data:
            socket_recibido.close()
            selector.unregister(socket_recibido)
            sockets.remove(socket_recibido)
            print(f"[Usuario({clientes[socket_recibido]}) desconectado]")
            del clientes[socket_recibido]
            return
    except ConnectionResetError:
        print(f"[Usuario({clientes[socket_recibido]}) desconectado]")
        selector.unregister(socket_recibido)
        sockets.remove(socket_recibido)
        del clientes[socket_recibido]
        socket_recibido.close()
    else:
        print(f"[Mensaje de Usuario]=",data.decode())
        todos(socket_recibido,data)


def todos(socket_recibido,data):
    for sock in list(sockets):
        if sock != socket_recibido:
            try:
                sock.send(data)
            except Exception:
                selector.unregister(sock)
                sockets.remove(sock)
                del clientes[sock]
                sock.close()





def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    server.bind((HOST,PORT))
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.setblocking(False)
    print("[--Servidor Encendido--]")
    server.listen()

    selector.register(server,selectors.EVENT_READ,aceptar)
    try:
        while True:
            eventos=selector.select(timeout=None)
            for clave,mask in eventos:
                callback=clave.data
                sock=clave.fileobj
                callback(sock)
    except KeyboardInterrupt:
        print("[SERVIDOR APAGADO POR USUARIO]")
    finally:
        for usuario in sockets:
            selector.unregister(usuario)
            usuario.close()

        selector.unregister(server)
        server.close()

if __name__=="__main__":
    main()
    