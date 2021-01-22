# Create your tests here.
from app.wsgi import *
from cssf.models import *
#from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

print(authenticate(username='admi', password='123456'))

g = Group.objects.all()
print(g)
#import pytz


data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            }
        ]
    }
print(len((data["urls"])))

print(timezone.now())
#print(datetime.now())

#select
#query = Documento.objects.all()
#query = Facultad.objects.all()
#print(query)
#print("x")

#insert
#c = Categoria()
#c.nombre = "Docencia"
#c.descripcion = "Solicitudes de proyetos de aula"
#c.save()
#f = Facultad()
#f.nombre = "Ciencias de la ingenieria"
#f.save()

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
#c = Categoria.objects.filter(nombre__startswith="d")
#print(c)