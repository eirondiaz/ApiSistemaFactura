from fastapi import FastAPI
from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

db = SqliteDatabase('dataa.db')

class Invoice(BaseModel):
    nombreCliente: Optional[str] = None
    rnc: Optional[str] = None
    fecha: Optional[str] = None
    descripcion: Optional[str] = None
    detalle: Optional[str] = None
    subtotal: Optional[str] = None
    itbis: Optional[str] = None
    total: Optional[str] = None

class Factura(Model):
    id = IntegerField(primary_key=True)
    nombreCliente = CharField()
    rnc = CharField()
    fecha = CharField()
    descripcion = CharField()
    detalle = CharField()
    subtotal = CharField()
    itbis = CharField()
    total = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Factura])

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return 'Bienvenido al api de la tarea 9 7 10 de Prog Web. By Eiron'

@app.get('/factura')
def get_facturas():
    factList = []
    for fact in Factura.select():
        factList.append(fact.__data__)
    return {'ok': True, 'facturas': factList}

@app.get('/factura/{id}')
def getFacturaById(id: str):
    try:
        fact = Factura.get(Factura.id == id)
        return {'ok': True, 'factura': fact.__data__}
    except:
        return {'ok': False, 'factura': None, 'msg': 'Not Found'}       

@app.post('/factura')
def create_factura(factura: Invoice):
    fact = Factura(
            nombreCliente = factura.nombreCliente,
            rnc = factura.rnc,
            fecha = factura.fecha,
            descripcion = factura.descripcion,
            detalle = factura.detalle,
            subtotal = factura.subtotal,
            itbis = factura.itbis,
            total = factura.total
            )
    fact.save()
    return {'ok': True, 'msg': 'Factura creada'}

@app.delete('/factura/{id}')
def deleteFactura(id: str):
    Factura.delete().where(Factura.id == id).execute()
    return {'ok': True, 'msg': 'factura eliminada'}

@app.put('/factura/{id}')
def updateFatura(id: str, fact: Invoice):
    try:
        Factura.update(
            nombreCliente = fact.nombreCliente,
            rnc = fact.rnc,
            descripcion = fact.descripcion,
            detalle = fact.detalle,
            subtotal = fact.subtotal,
            itbis = fact.itbis,
            total = fact.total
        ).where(Factura.id == id).execute()
        return {'ok': True, 'msg': 'factura actualizada'}
    except:
        return {'ok': False, 'msg': 'error'}
