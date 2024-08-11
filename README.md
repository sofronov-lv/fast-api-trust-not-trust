# Trust Not Trust

## Installation (Linux) 🛠️
To install this project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/sofronov-lv/fast-api-trust-not-trust.git
   ```

2. Go to the directory and create a virtual environment:  
   ```bash
   cd fast-api-trust-not-trust
   ```
   ```bash
   python3 -m venv venv
   ```
   
3. Activate the virtual environment and install the necessary packages:  
   ```bash
   source venv/bin/activate
   ```
   ```bash
   pip install -r requirements.txt
   ```

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
   IQ_SMS_LOGIN=login
   IQ_SMS_PASSWORD=password123

   DB_USER=username
   DB_NAME=database_name
   DB_PASS=db_password
   DB_HOST=localhost
   DB_PORT=1234
   
   API_HOST=0.0.0.0
   API_PORT=5000
   ```
(Attention!!! This application uses a third-party microservice to send SMS. If you do not have an account on the site https://iqsms.ru / - you will have to change part of the code for correct review [STEP 7])

7. Changing the code:  
   This step is for users who do not have an account on iq.sms or for those who do not want to receive SMS confirmation, but only check the functionality of Trust Not Trust.
   Open file app/routes/auth.py Go down to the function get_one_time_code.
   
   Comment out the following lines:  
      ```python3
      utils.check_sms(phone_number, code.code, code.id)
      return JSONResponse(
        status_code=200,
        content={"message": "The code has been sent successfully"}
      )
      ```
      
      And add the following code instead:  
      ```python3
      return JSONResponse(
        status_code=200,
        content={"message": f"Code: {code.code}"}
      )

8. PostgreSQL:  
   Create a database in postgresql that will match the variables created in the .env file
   
9. Launching the API:  
   Run the following command in the terminal:
   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

## Documentation 📑
   All the functionality after launching the API will be located at the following address: http://0.0.0.0:8000/docs.
   When you create an application on FastAPI, it automatically generates OpenAPI documentation based on your routes and annotations.
   FastAPI provides embedded documentation (Swagger UI and ReDoc) where you can see and test the API using the OpenAPI specification.
