# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:44:18 2024

@author: Prorumus Marketing
"""

import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Defina o caminho onde os arquivos serão salvos
UPLOAD_FOLDER = './downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Pega a mensagem enviada pelo usuário
    incoming_msg = request.values.get("Body", "").lower() # Mensagem recebida
    num_media = int(request.form.get('NumMedia')) # Quantos arquivos foram enviados
    sender = request.form.get('From') # Número do remetente
    
    # Faça algo com a mensagem
    print(f"Mensagem recebida de {sender}: {incoming_msg}")
    
    # Inicializa a resposta
    resp = MessagingResponse()
    msg = resp.message()
    
    if num_media > 0:
        # Processar cada mídia enviada
        for i in range(num_media):
            media_url = request.form.get(f'MediaUrl{i}') # URL do arquivo
            media_type = request.form.get(f'MediaContentType{i}') # Tipo do arquivo
            
            # Baixar e salvar o arquivo
            file_extension = media_type.split('/')[-1] # Extrair extensão do arquivo
            file_name = f'file_{i}.{file_extension}' # Nome do arquivo salvo
            file_path = os.path.join(UPLOAD_FOLDER, file_name) # Caminho completo para salvar o arquivo
            
            # Baixar o arquivo da URL fornecida pelo Twilio
            download_file(media_url, file_path)
            
        # Reponder ao usuário com a URL do arquivo
        resp.message(f"Recebemos seu arquivo: {media_url}")
    
    # Lógica do bot
    if "1" in incoming_msg:
        msg.body("Os nossos cursos:\n* Formação Inicial de Formadores\n* Vigilante Principal - Intensivo\n* GPTBusiness\n* Cibersegurança\n...")
    elif "2" in incoming_msg:
        msg.body("Nossa localização:\nTalatona, Luanda-Sul, Edificio Prometeus, Escritório nº4!")
    elif "3" in incoming_msg:
        msg.body("Sobre Nós:\n\nEmpresa: PRORUMUS - FORMAÇÃO E CONSULTORIA\nNif: 5417635723\nNúmero: +244 938 768 111\nEmail: info@prorumus.ao")
    else:
        msg.body(f"Cordiais Saudações! \nBem-Vindo a PRORUMUS - FORMAÇÃO E CONSULTORIA \n\nComo posso ajudar você hoje? \n\nEscolha um número das opções abaixo: \n1-Lista de Cursos\n2-Localização\n3-Sobre Nós")
    
    return str(resp)

def download_file(url, file_path):
    """Função para baixar e salvar um arquivo a partir de uma URL."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Arquivo salvo: {url}')
    else:
        print(f'Falha ao baixar o arquivo: {url}')

if __name__=='__main__':
    app.run(debug=True)