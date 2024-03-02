import socket
import threading

# Función para recibir mensajes del servidor
def receive_messages(client_socket):
    while True:
        try:
            # Recibir mensajes del servidor
            message = client_socket.recv(1024).decode("utf-8")
            # Imprimir mensaje recibido del servidor
            print(message)
        except:
            print("Error al recibir mensajes del servidor.")
            break

# Función principal para iniciar el cliente
def start_client(server_port):
    # Crear un socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Conectar el cliente al servidor utilizando la dirección IP de loopback y el puerto especificado
        client_socket.connect(("127.0.0.1", server_port))
        # Imprimir mensaje de conexión exitosa al servidor
        print(f"Conectado al servidor en el puerto {server_port}.")
    except Exception as e:
        # Imprimir mensaje de error si no se puede conectar al servidor
        print(f"No se pudo conectar al servidor: {e}")
        return

    # Crear un hilo para recibir mensajes del servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    # Iniciar el hilo
    receive_thread.start()

    while True:
        # Esperar la entrada del usuario
        message = input()
        # Enviar mensaje al servidor
        client_socket.send(message.encode("utf-8"))

if __name__ == "__main__":
    # Solicitar al usuario que ingrese el puerto del servidor
    server_port = int(input("Ingresa el puerto del servidor: "))
    # Iniciar el cliente con el puerto del servidor especificado
    start_client(server_port)