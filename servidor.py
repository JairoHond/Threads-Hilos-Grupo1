import socket
import threading

# Función para manejar la comunicación con un cliente específico
def handle_client(client_socket, client_address):
    while True:
        try:
            # Recibir mensajes del cliente
            message = client_socket.recv(1024).decode("utf-8")
            # Verificar si el cliente se desconectó
            if not message:
                print(f"[{client_address[0]}:{client_address[1]}] se desconectó.")
                break
            # Imprimir mensaje recibido del cliente
            print(f"Recibido de [{client_address[0]}:{client_address[1]}]: {message}")
            # Difundir el mensaje a todos los clientes
            broadcast(message, client_socket)
        except:
            print(f"Error al recibir mensajes de [{client_address[0]}:{client_address[1]}]")
            break
    client_socket.close()

# Función para difundir un mensaje a todos los clientes excepto al remitente
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                # Enviar mensaje a cada cliente
                client.send(message.encode("utf-8"))
            except:
                # Eliminar clientes que no puedan recibir el mensaje
                clients.remove(client)

# Función principal para iniciar el servidor
def start_server():
    global clients
    # Crear un socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enlazar el socket a una dirección IP y un puerto aleatorio
    server_socket.bind(("0.0.0.0", 0))
    # Escuchar conexiones entrantes
    server_socket.listen(5)
    # Obtener el puerto al que se ha enlazado el servidor
    server_port = server_socket.getsockname()[1]
    # Imprimir mensaje de inicio del servidor
    print(f"Servidor iniciado. Esperando conexiones en el puerto {server_port}...")

    # Lista para almacenar los sockets de los clientes conectados
    clients = []

    while True:
        # Aceptar conexiones entrantes de los clientes
        client_socket, client_address = server_socket.accept()
        # Imprimir mensaje de conexión establecida
        print(f"Conexión establecida desde [{client_address[0]}:{client_address[1]}]")
        # Agregar el socket del cliente a la lista de clientes
        clients.append(client_socket)
        # Crear un hilo para manejar la comunicación con el cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        # Iniciar el hilo
        client_thread.start()

if __name__ == "__main__":
    start_server()
