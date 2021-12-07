from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from db import connection
from models import Drawing, Order, Part, Point, Hole
from tekla import Tekla, Faza_update


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

# @app.on_event("startup")
# async def startup() -> None:
#   database_ = app.state.database
#   if not database_.is_connected:
#     await database_.connect()

# @app.on_event("shutdown")
# async def shutdown() -> None:
#   database_ = app.state.database
#   if database_.is_connected:
#     await database_.disconnect()


@app.get('/')
def get():
  drawing = Order(cas="3000")
  drawing.save()
  return drawing
  # return await Point.objects.filter(assembly__cas__cas="1000").sum('assembly__weight')

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
  # await Faza_update(order)
  return # await Point.objects.filter(assembly__cas__cas=order,faza=4).sum('assembly__weight')