from flask import Flask
import os
from flask_basicauth import BasicAuth
import pymysql
from flask import abort
import json
from flask import request
import math
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/openapi.yaml',
)


# we get details of a pet from animal_id (<animal_id>): 
app = Flask(__name__)
app.config.from_file("flask_config.json", load=json.load)
app.register_blueprint(swaggerui_blueprint)

PAGE_SIZE=100
def remove_null_fields(obj):
        return {k:v for k, v in obj.items() if v is not None}

@app.route("/pets/<animal_id>")

def pet(animal_id):
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('SQL'),
                                database="paws",
                              cursorclass=pymysql.cursors.DictCursor)
    with db_conn.cursor() as cursor:
        cursor.execute("""SELECT * 
                       FROM shelter_in_out s WHERE s.animal_id=%s""", (animal_id, ))
        pet = cursor.fetchone()
        if not pet:
            abort(404)
    db_conn.close() 
    return remove_null_fields(pet)


# main shelter_in_out table :

@app.route("/pets")
# @auth.required
def pets():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', PAGE_SIZE))
    page_size = min(page_size, PAGE_SIZE)
    # include_details= bool(request.args.get('include_details', 1))

    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('SQL'),
                              database="paws",
                              cursorclass=pymysql.cursors.DictCursor)
    
    with db_conn.cursor() as cursor:
        
        cursor.execute("""SELECT s.animal_id,
                       s.breed, 
                       s.age,
                       s.days_in_shelter, 
                       s.intake_condition,
                       s. outcome_type
                       FROM shelter_in_out s
                       ORDER BY s.days_in_shelter DESC
                       LIMIT %s
                       OFFSET %s""", 
                       (PAGE_SIZE, (page-1) * PAGE_SIZE))
                       
        pets = cursor.fetchall()
        if not pets:
            abort(404)

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM shelter_in_out")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)

    db_conn.close()
    if page==last_page:
        return {'total_pets': total,'pets': pets,'next_page': None,
                'last_page': f'/pets?page={last_page}&page_size={page_size}'}
    else:
        return {'total_pets': total,'pets': pets,'next_page': f'/pets?page={page+1}&page_size={page_size}','last_page': f'/pets?page={last_page}&page_size={page_size}'}


# get the animal_id 

@app.route("/get_animal_ids")
# @auth.required
def animal_ids():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', PAGE_SIZE))
    page_size = min(page_size, PAGE_SIZE)
    # include_details= bool(request.args.get('include_details', 1))

    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('SQL'),
                              database="paws",
                              cursorclass=pymysql.cursors.DictCursor)
    
    with db_conn.cursor() as cursor:
        
        cursor.execute("""SELECT s.breed, 
                       s.animal_id
                       FROM shelter_in_out s
                       ORDER BY s.days_in_shelter DESC
                       LIMIT %s
                       OFFSET %s""", 
                       (PAGE_SIZE, (page-1) * PAGE_SIZE))
                       
        animal_ids = cursor.fetchall()
        if not animal_ids:
            abort(404)

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM shelter_in_out")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)

    db_conn.close()

    if page==last_page:
        return {'animal_ids': animal_ids, 'next_page': None,'last_page': f'/get_animal_ids?page={last_page}&page_size={page_size}'}
    else:
        return {'animal_ids': animal_ids, 'next_page': f'/get_animal_ids?page={page+1}&page_size={page_size}','last_page': f'/get_animal_ids?page={last_page}&page_size={page_size}'}