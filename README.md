# Reactor API
A REST API written in Django detailing US nuclear reactor data and status reports.

## Explanation
This project uses Django REST to create an API that exposes endpoints for data gathered from the nuclear reactor power status .txt file provided, as well as other data gathered from https://www.nrc.gov/. 

Follow the steps below to get started:

## Project setup
* Create a virtual environment:
    ```bash
        $ python -m venv venv
    ```
* Activate virtual environment:
    ```bash
        $ source venv/bin/activate
    ```
* Git clone this repo to your PC:
    ```bash
        $ git clone https://github.com/ellis3684/reactor-api-sesco.git
    ```
* Install dependencies:
    ```bash
        $ pip install -r requirements.txt
    ```
  
## Database setup
* Make and run migrations:
    ```bash
        $ python manage.py makemigrations
    ```
    ```bash
        $ python manage.py migrate
    ```
* Import data from .csv and .xlsx files into database:
    ```bash
        $ python manage.py importdata
    ```

## Start the server and navigate endpoints
* Start the server with the below command:
    ```bash
        $ python manage.py runserver
    ```
* Access below url for the endpoint documentation:
    ```http request
        http://127.0.0.1:8000/docs/
    ```
* Choose an endpoint in the documentation to navigate to.