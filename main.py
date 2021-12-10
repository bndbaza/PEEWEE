from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from db import connection
from models import Drawing, Order, Part, Point, Hole
from tekla import Tekla
from faza import Faza_update
from peewee import fn
from schemas import OrderBase, DrawingBase


app = FastAPI()
app.state.database = connection


origins = [
  "http://localhost",
  "http://127.0.0.1:8080",
  "http://192.168.0.75:8080",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get('/',response_model=DrawingBase)
def get():
  # drawing = Order(cas="3000")
  # drawing.save()
  # print((Drawing.select(((Drawing.area) + (Drawing.weight)).alias('aaa')).first()).aaa)
  aaa = (Drawing.select().join(Order).where(Order.cas == "2000").dicts()[0])
  print(aaa)
  return aaa

# @app.post('/',response_model=Drawing)
# async def postDrawing(drawing: Drawing):
#   await drawing.save()
#   return drawing

@app.post('/order')
async def postTekla(
  file: UploadFile = File(...),
  order: str = Form(...)
):
  Tekla(file,order)
  Faza_update(order)
  return # await Point.objects.filter(assembly__cas__cas=order,faza=4).sum('assembly__weight')