# Gun Detector - Projeto de Visão Computacional

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)


## Descrição do projeto

<p align="justify">Wste projeto é uma aplicação web desenvolvida para detectar armas em tempo real utilizando a webcam ou vídeos enviados pelo usuário. O sistema permite a escolha entre dois modelos de detecção – o modelo YOLO e um modelo personalizado – e salva automaticamente os frames com detecções em uma estrutura de diretórios organizada. Além disso, quando um objeto é identificado, a aplicação envia uma notificação por e-mail utilizando o Brevo Service e transfere as imagens para o AWS S3.</p>

## Funcionalidades

- **Detecção em tempo real:**  
  Captura e análise de frames via webcam.
- **Análise de vídeo:**  
  Permite o upload de vídeos para análise.
- **Seleção de modelo:**  
  O usuário pode escolher entre o modelo YOLO ou um modelo personalizado para a detecção.
- **Salvamento automático:**  
  Frames com detecções são salvos automaticamente com uma estrutura de diretórios baseada em data e hora.
- **Notificação por e-mail:**  
  Quando um objeto é identificado, o sistema envia uma notificação por e-mail utilizando o Brevo Service.
- **Upload para S3:**  
  As imagens com detecções são transferidas automaticamente para o AWS S3, garantindo armazenamento seguro e escalável.

## Tecnologias Utilizadas

- Python 3.x
- Flask
- OpenCV
- Ultralytics (YOLO)
- Torch
- Brevo Service (para notificações por e-mail)
- AWS S3 (para armazenamento de imagens)
- HTML/CSS (utilizando Google Fonts)

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone git@github.com:weberton/gun-detector.git
   cd gun-detector
   ```

2. **Crie e ative um ambiente virtual:**
    ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configuração de Variáveis de Ambiente:**
   Configure as variáveis necessárias para a integração com o Brevo Service e o AWS S3 no arquivo `.env`. Por exemplo:

- BREVO_API_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_S3_BUCKET
- NOTIFICATIONS_RECIPIENTS

## Como os usuários podem utilizá-lo
1. *Inicie a aplicação:**
   - Execute o arquivo `app.py` a partir do terminal:
   ```bash
   python app.py
   ```
2. Acesse a aplicação:
    ```bash
    http://localhost:5000
    ```
## Autores do projeto
- Weberton Faria
- Luiza Fraga
- Adriano Marques
- Rodrigo Zanel 
