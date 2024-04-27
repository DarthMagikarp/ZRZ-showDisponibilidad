# chat conversation
import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")

    id_user = str(request.json['id_user'])
    sql = "select id, id_bloque, id_user, tipo, día, fechaInicio, fechaFin, repeticiones, horaIni, horaFin, modalidad, frecuencia, detalleServicio, duracionServicio from disponibilidades where id_user="+id_user+";"
    cursor.execute(sql)
    resp = cursor.fetchall()
    print(str(resp))

    arrayDisp=[]
    retorno = {
        "users":{}
    }
    for registro in resp:
        item={
            "id":registro[0],
            "id_bloque":registro[1],
            "id_user":registro[2],
            "tipo":registro[3],
            "día":registro[4],
            "fechaInicio":registro[5],
            "fechaFin":registro[6],
            "repeticiones":registro[7],
            "horaIni":format_timedelta(registro[8]),
            "horaFin":format_timedelta(registro[9]),
            "modalidad":registro[10],
            "frecuencia":registro[11],
            "detalleServicio":registro[12],
            "duracionServicio":registro[13]
        }
        arrayDisp.append(item)
    retorno['users'] = arrayDisp
    print(arrayDisp)
    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

def format_timedelta(td):
    # Obtener la cantidad total de segundos
    total_seconds = td.total_seconds()

    # Calcular horas, minutos y segundos
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formatear en HH:mm:ss
    formatted_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    return formatted_time

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')