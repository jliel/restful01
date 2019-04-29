from rest_framework import serializers
from .models import DroneCategory, Drone, Pilot, Competition
import drones.views


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    # related name
    drones = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='drone-detail'
    )

    class Meta:
        model = DroneCategory
        fields = (
            'url',
            'pk',
            'name',
            'drones'
        )


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    # slugrelatedfield es un campo de lectura/escritura que representa el objetivo de la relacion por un atributo slug unico
    # la descripcion
    # se quiere mostrar el nombre del drone_category como una descripcion (slug field)
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')

    class Meta:
        model = Drone
        fields = (
            'url',
            'name',
            'drone_category',
            'manufacturing_date',
            'has_it_completed',
            'inserted_timestamp'
        )



class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    # drone es una llave foranea en el modelo
    # asi que tambien se debe serializar los datos de dicho dron
    drone = DroneSerializer()
    # se evita poner el campo de piloto para no serializar esos datos aun
    # dado que se usara PilotSerializer como master y competitionserializer como detalle
    class Meta:
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_archivement_date',
            'drone'
        )

# se usa para serializar los datos de los pilotos
class PilotSerializer(serializers.HyperlinkedModelSerializer):
    # se hara uso del competitionserializer para serializar los datos de las competiciones 
    # en las que ha participado el piloto
    # many = True dado que es un piloto puede tener varias competiciones
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Pilot.GENDER_CHOICES
    )
    gender_description = serializers.CharField(
        # esta contituido por el prefijo get_ seguido del nombre del campo y el sufijo _display
        # de esta manera gender_description renderizara la descripcion de las opciones de genero en lugar
        # de las opciones char que fueron almacenadas
        source='get_gender_dislay',
        read_only=True
    )

    class Meta:
        model = Pilot
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'races_count',
            'inserted_timestamp',
            'competitions'
        )


class PilotCompetitionSerializer(serializers.ModelSerializer):
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')

    class Meta:
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_archivement_date',
            'pilot',
            'drone'
        )
