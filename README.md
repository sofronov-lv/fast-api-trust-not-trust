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
   ```
   ```bash
   openssl rsa -pubout -in app/core/certs/refresh_token_private.pem -out app/core/certs/refresh_token_public.pem
   ```
   ```bash
   openssl genpkey -algorithm RSA -out app/core/certs/access_token_private.pem -pkeyopt rsa_keygen_bits:2048
   ```
   ```bash
   openssl rsa -pubout -in app/core/certs/access_token_private.pem -out app/core/certs/access_token_public.pem
   ```

5. Create an environment variables file:
   ```bash
   touch app/core/.env
   ```

6. Declare the following variables in the .env file:
   ```text
   IQ_SMS_LOGIN=z123
   IQ_SMS_PASSWORD=123

   DB_USER=postgres
   DB_NAME=trust_db
   DB_PASS=123
   DB_HOST=localhost
   DB_PORT=5432
   
   API_HOST=0.0.0.0
   API_PORT=5000
   ```
(Attention! This application uses a third-party microservice to send SMS. If you do not have an account on the site https://iqsms.ru / - you will have to change part of the code for correct review [STEP 7])

7. Изменение кода:
   Внимание!!! Шаг для пользователей, которые не имеют аккаунта на iq.sms или для тех, кто не хочет получать СМС о подтверждении, а лишь проверить функционал Trust Not Trust.
   7.1 Откройте файл app/routes/auth.py
   7.2 Спуститесь к функции get_one_time_code
   7.3 Закоментируйте следующие строчки:
      ```python3
      utils.check_sms(phone_number, code.code, code.id)
      return JSONResponse(
        status_code=200,
        content={"message": "The code has been sent successfully"}
      )
      ```
      И добавьте вместо них следующий код:
      ```python3
      return JSONResponse(
        status_code=200,
        content={"message": f"Code: {code.code}"}
      )


### The last point (Launching the API):
   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
