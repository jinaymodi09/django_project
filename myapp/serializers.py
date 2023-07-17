from rest_framework import serializers
from .models import User, Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_level','password']
    
    def create(self, validated_data):
        # Create a new user instance with the validated data
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_level=validated_data['user_level'],
        )
        # Set the password for the user
        user.set_password(validated_data['password'])
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
