# Definir los metodos encargados de serializar los datos
# datos primitivos a JSON
from rest_framework import serializers
from .models import Toy


class ToySerializer(serializers.Serializer):
    # Campos que seran serializados
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=250)
    toy_category = serializers.CharField(max_length=200)
    release_date = serializers.DateTimeField()
    was_included_in_home = serializers.BooleanField(required=False)

    # Siempre sobreescribir estos dos metodos o una excepcion NotImplementedError sera lanzada
    # cada metodo recibe los datos validados como argumento
    # Crea una nueva instancia de Toy y la devuelve
    def create(self, validated_data):
        # Se crea un nuevo toy basado en los datos enviados
        return Toy.objects.create(**validated_data)

    # Recibe un toy ya creado y los datos con los que sera actualizdo
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.toy_category = validated_data.get('toy_category', instance.toy_category)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.was_included_in_home = validated_data.get('was_included_in_home', instance.was_included_in_home)
        # Actualiza la isntancia y devuelve el objeto actualizado
        instance.save()
        return instance
