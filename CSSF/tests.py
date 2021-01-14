# Create your tests here.
from app.wsgi import *
from CSSF.models import *
#from datetime import datetime
from django.utils import timezone
#import pytz

print(timezone.now())
#print(datetime.now())

#select
#query = Documento.objects.all()
#query = Categoria.objects.all()
#print(query)
#print("x")

#insert
#c = Categoria()
#c.nombre = "Docencia"
#c.descripcion = "Solicitudes de proyetos de aula"
#c.save()
f = Facultad()
f.nombre = "Ciencias de la ingenieria"
f.save()

#ediccion
#obtener objecto mediante valor unico
#c = Categoria.objects.get(nombre = "Docencia")
#c = Categoria.objects.get(id = 1)
#c.fecha_creacion = timezone.now()
#c.save()
#print(c)


#eliminacion
#c = Categoria.objects.get(nombre = "Docencia")
#c.delete()

#consultas personalizadas
c = Categoria.objects.filter(nombre__startswith="d")
print(c)