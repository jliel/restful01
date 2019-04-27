from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Toy
from .serializers import ToySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# No es necesario  crearla al usar el wrapper api_view, clase que contiene 
# e implementa sus propios render y parsers
# Renderiza su contenido en JSON
"""
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # Crea una instancia de render y llama su metodo para renderizar a json los datos enviados
        content = JSONRenderer().render(data)
        # agrega la lleva 'content_type' al header de la respuesta con 'application/json' como valor
        kwargs['content_type'] = 'application/json'
        # se llama al iniciador
        super(JSONResponse, self).__init__(content, **kwargs) """


#@csrf_exempt
# el decorador api_view permite especificar cuales son los verbos http que
# la funcion es capaz de procesar, este es capaz de manejar los errores
# que se presenten si algun verbo no admitido es enviado
# convierte una view based-function en una subclase de rest_framework.views.APIView
# la cual es la clase base para todas las views en django REST framework
@api_view(['GET', 'POST'])
def toy_list(request):
    # obtener una lista de toys serializados
    if request.method == 'GET':
        toys = Toy.objects.all()
        # Se crea el serializer con many=True para indicar que son varios toys a serializarse y no solo 1
        toys_serializer = ToySerializer(toys, many=True)
        #return JSONResponse(toys_serializer.data)
        return Response(toys_serializer.data)
    # guardar un nuevo toy con los datos enviados en json
    elif request.method == 'POST':
        # deserializar los datos
        # toy_data = JSONParser().parse(request)
        # crear el serializador
        # toy_serializer = ToySerializer(data=toy_data)
        toy_serializer = ToySerializer(data=request.data)
        # verificar los datos
        if toy_serializer.is_valid():
            # guardar la nueva isntancia
            toy_serializer.save()
            #return JSONResponse(toy_serializer.data, \
            #    status=status.HTTP_201_CREATED)
            return Response(toy_serializer.data, status=status.HTTP_201_CREATED)
        # en caso de que los datos no sean correctos
        #return JSONResponse(toy_serializer.errors, \
        #        status=status.HTTP_400_BAD_REQUEST)
        return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Recupera, actuazliza o borra un toy existente
#@csrf_exempt
# Recibe un HttpRequest y el identificador del toy que sera modificado
# es capaz de procesar tres tipos de verbo Http, GET, PUT y DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def toy_detail(request, id):
    # sin importar el tipo de peticion siempre se intenta obtener el toy de la bd
    try:
        toy = Toy.objects.get(pk=id)
    except Toy.DoesNotExist:
        #return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # si se puede obtener el toy y el metodo es GET
    # se crea una instancia de toyserializer para serializar el toy obtenido previamente
    # despues se devuelve el toy serializado en forma de JSON
    if request.method == 'GET':
        toy_serializer = ToySerializer(toy)
        # return JSONResponse(toy_serializer.data)
        return Response(toy_serializer.data)
    
    # si la peticion es PUT sera usada para actualizar un toy
    elif request.method == 'PUT':
        # se reciben los datos del toy en la httprequest
        # se hace uso del parser para manejar los datos del toy que son enviados en forma de JSON
        # toy_data = JSONParser().parse(request)
        # se crea el serializador con los datos recibidos y el toy obtenido de la base de datos
        # toy_serializer = ToySerializer(toy, data=toy_data)
        """ Al hacer uso de api_view se esta haciendo uso de los parser por default que son
            rest_framework.parsers.JSONParser      application/json
            rest_framework.parsers.FormParser      application/x-www-form-urlencoded
            rest_framework.parsers.MultiPartParser multipart/form-data 
            rest_framework.response.BrowsableAPIRenderer  text/html
            
            cuando se llama a request.data django rest framework examina el valor del header 'Content-Type' 
            y elige el parser adecuado para el tipo de dato """
        toy_serializer = ToySerializer(toy, data=request.data)
        # si los datos son correctos
        if toy_serializer.is_valid():
            # se guarda el toy actualizado
            toy_serializer.save()
            #return JSONResponse(toy_serializer.data)
            return Response(toy_serializer.data)
        # return JSONResponse(toy_serializer.errors, \
        #        status=status.HTTP_400_BAD_REQUEST)
        return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # si la peticion es DELETE se elimina el toy obtenido
    elif request.method == 'DELETE':
        toy.delete()
        # return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)
