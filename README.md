# 🎬 Cinema API

API REST para gerenciamento de ingressos de cinema desenvolvida com **Django REST Framework**.

## 🚀 Funcionalidades

* Cadastro e login com JWT
* Listagem de filmes
* Listagem de sessões por filme
* Visualização do mapa de assentos
* Reserva temporária de assento (lock de 10 minutos)
* Checkout e geração de ingresso digital
* Listagem de ingressos do usuário

## 🔐 Autenticação

A API utiliza JWT.

Após login, envie o token:

Authorization: Bearer SEU_TOKEN

## 📄 Documentação

A documentação da API está disponível via **Postman Collection**:

📁 `Cinema API.postman_collection.json`

Importe no Postman para testar todos os endpoints.

## ▶️ Como rodar o projeto

```bash
git clone https://github.com/GustavoInagaki/cine-reserve-api.git
cd cine-reserve-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Acesse:

http://127.0.0.1:8000/
