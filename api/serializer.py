from rest_framework import serializers
from django.contrib.auth import authenticate


from .models import User, Client, Occupation, Agent, Ticket


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'role', 'is_active', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'required': True},
            'is_staff': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                msg = 'No se puede iniciar sesión con las credenciales proporcionadas.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = 'La cuenta está desactivada.'
                raise serializers.ValidationError(msg, code='authorization')

            data['user'] = user
            return data
        else:
            msg = 'Se debe incluir "email" y "password".'
            raise serializers.ValidationError(msg, code='authorization')

class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ['id', 'occupation']

class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Client
        fields = ['id', 'name_company', 'address', 'contact_phone', 'registered_date', 'user']

class AgentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    occupation = serializers.PrimaryKeyRelatedField(queryset=Occupation.objects.all())

    class Meta:
        model = Agent
        fields = ['id', 'name', 'last_name', 'phone', 'registered_date', 'user', 'occupation']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'image', 'priority', 'status', 'registered_date', 'delivery_date', 'agent', 'client']
        read_only_fields = ['status', 'registered_date', 'agent', 'priority', 'delivery_date'] 

    def create(self, validated_data):
        validated_data['status'] = 'notificacion'
        return super().create(validated_data)
    
