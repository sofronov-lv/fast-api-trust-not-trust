# Trust Not Trust

## Installation (Linux) 🛠️
To install this project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/sofronov-lv/fast-api-trust-not-trust.git

2. Go to the directory and create a virtual environment:
   ```bash
   cd fast-api-trust-not-trust
   python3 -m venv venv
   
3. Activate the virtual environment and install the necessary packages:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt

4. Create private and public keys for the refresh and access tokens:
   ```bash
   openssl genpkey -algorithm RSA -out app/core/certs/refresh_token_private.pem -pkeyopt rsa_keygen_bits:2048
   openssl rsa -pubout -in app/core/certs/refresh_token_private.pem -out app/core/certs/refresh_token_public.pem

   openssl genpkey -algorithm RSA -out app/core/certs/access_token_private.pem -pkeyopt rsa_keygen_bits:2048
   openssl rsa -pubout -in app/core/certs/access_token_private.pem -out app/core/certs/access_token_public.pem

6. Create an environment variables file:
   ```bash
   touch .env
   ```
   

### The last point (Launching the API):
   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
