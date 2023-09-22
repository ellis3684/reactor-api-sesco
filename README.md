# Reactor API
A REST API written in Django detailing US nuclear reactor data and status reports.

## Explanation
This project uses Django REST to create an API that exposes endpoints for data gathered from the nuclear reactor power status .txt file provided, as well as other data gathered from https://www.nrc.gov/. 

Follow the steps below to get started:

## Project setup
* Git clone this repo to your PC:
    ```bash
    git clone git@github.com:ellis3684/reactor-api-sesco.git
    ```
* CD into the project directory
    ```bash
    cd reactor-api-sesco
    ```
* Create a virtual environment:
    ```bash
    python -m venv venv
    ```
* Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```
* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
  
## Database setup
* Run Django migrations:
    ```bash
    python manage.py migrate
    ```
* Import data from .csv and .xlsx files into database (this will take up to a minute):
    ```bash
    python manage.py importdata
    ```

## Start the server and navigate endpoints
* Start the server with the below command:
    ```bash
    python manage.py runserver
    ```
* Access below url for the endpoint documentation:
    ```http request
    http://127.0.0.1:8000/docs/
    ```
* Choose an endpoint in the documentation to navigate to.