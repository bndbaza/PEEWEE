import csv
from os import replace
from db import connection
import datetime
from models import Drawing, Order, Point, Part, Weld, Bolt, Nut, Washer, Hole, Chamfer
Y = ('А','Б','В','Г','Д','Е','Ж','З','И','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ы','Э','Ю','Я')

def Tekla(xls,yyy):
  yyy = Order.get_or_create(cas=yyy)
  parts = []
  dates = datetime.datetime.today()
  draw = []
  drawings = []
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[0].replace(' ','') == 'DRAWING' and row[3].replace(' ','') == '1':
        non_drawing = Drawing.get_or_none(cas=yyy[0],assembly=row[1].replace(' ',''))
        if non_drawing != None:
          continue
        d = (row[1].replace(' ',''),float(row[4].replace(' ','')),yyy[0],dates,int(row[5].replace(' ','')))
        draw.append(d)
  with connection.atomic():
    Drawing.insert_many(draw, fields=[Drawing.assembly,Drawing.area,Drawing.cas,Drawing.create_date,Drawing.count]).execute()
    drawings = Drawing.filter(cas=yyy[0])
    draw = []
    print(draw)
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[0].replace(' ','') == 'ASSEMBLY':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[3].replace(' ','').split('/')[0].split('-')[0],row[3].replace(' ','').split('/')[1].split('-')[0],float(row[2].replace(' ','')),dates)
            draw.append(Point.assembly,Point.point_x,Point.point_y,Point.point_z,Point.create_date)





      # if row[0].replace(' ','') == 'PART':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       part = await Part.objects.create(
      #         assembly = col[1],
      #         number = int(row[2].replace(' ','')),
      #         count = int(row[3].replace(' ','')),
      #         profile = row[4].replace(' ',''),
      #         length = float(row[5].replace(' ','')),
      #         weight = float(row[6].replace(' ','')),
      #         mark = row[8].replace(' ',''),
      #         manipulation = row[9].replace(' ',''),
      #         create_date=dates
      #       )
      #       parts.append(part)
      # if row[0].replace(' ','') == 'WELD':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       await Weld.objects.create(
      #         assembly = col[1],
      #         cathet = float(row[2].replace(' ','')),
      #         length = float(row[3].replace(' ','')),
      #         count = int(row[4].replace(' ','')),
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'BOLT':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       await Bolt.objects.create(
      #         assembly = col[1],
      #         profile = row[2].replace(' ',''),
      #         gost = row[3].replace(' ',''),
      #         count = int(row[4].replace(' ','')),
      #         weight = float(row[5].replace(' ','')),
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'NUT':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       await Nut.objects.create(
      #         assembly = col[1],
      #         profile = row[2].replace(' ',''),
      #         gost = row[3].replace(' ',''),
      #         count = int(row[4].replace(' ','')),
      #         weight = float(row[5].replace(' ','')),
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'WASHER':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       await Washer.objects.create(
      #         assembly = col[1],
      #         profile = row[2].replace(' ',''),
      #         gost = row[3].replace(' ',''),
      #         count = int(row[4].replace(' ','')),
      #         weight = float(row[5].replace(' ','')),
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'HOLE':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       part = await Part.objects.get(number=int(row[2].replace(' ','')),assembly=col[1])
      #       await Hole.objects.create(
      #         part = part,
      #         diameter = int(row[3].replace(' ','')),
      #         count = int(row[4].replace(' ','')),
      #         depth = int(row[5].replace(' ','')) / 2,
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'CHAMFER':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       part = await Part.objects.get(number=int(row[2].replace(' ','')),assembly=col[1])
      #       await Chamfer.objects.create(
      #         part = part,
      #         length = float(row[3].replace(' ','')),
      #         create_date=dates
      #       )
      # if row[0].replace(' ','') == 'WEIGHT':
      #   for col in drawings:
      #     if row[1].replace(' ','') == col[0]:
      #       if row[3].replace(' ','') != '':
      #         more = float(row[3].replace(' ','').split(';')[1])  / col[1].count
      #       else:
      #         more = 0
      #       await col[1].update(
      #         weight = float(row[2].replace(' ','')) / col[1].count,
      #         more=more,
      #       )
  return
      
async def Faza_update(order):
  points = await Point.objects.filter(assembly__cas__cas = order).order_by('point_y').order_by('point_x').order_by('point_z').all()
  line=1
  faza=1
  weight=0
  for row in points:
    await row.update(line=line)
    line += 1
    weight += row.assembly.weight
    if weight >= 14000:
      weight = row.assembly.weight
      faza += 1
    await row.update(faza=faza)