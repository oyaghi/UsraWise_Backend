from rest_framework import serializers
from .models import  CustomUser, Child, Hobbies, BehaviorChallenges, StandardTestScore
from django.db import transaction,IntegrityError



from rest_framework import serializers
from django.db import transaction, IntegrityError
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    phone = serializers.CharField(write_only=True)
    age = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)
    occupation = serializers.CharField(write_only=True)
    education_level = serializers.CharField(write_only=True)
    number_of_children = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'phone',
            'age',
            'gender',
            'occupation',
            'education_level',
            'number_of_children',
            'password',
        ]
        
    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'].lower(),
            'name': validated_data['name'],
            'phone': validated_data['phone'],
            'password': validated_data['password'],
            'age': validated_data['age'],
            'gender': validated_data['gender'],
            'occupation': validated_data['occupation'],
            'education_level': validated_data['education_level'],
            'number_of_children': validated_data['number_of_children']
        }

        with transaction.atomic():
            try:
                # Creating the user with the validated data
                user = CustomUser.objects.create_user(**user_data)
                
                # Serializing the created user
                serializer = CustomUserSerializer(user)
                return user_data
                
            except IntegrityError as e:
                raise serializers.ValidationError({"error": str(e)})


        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = CustomUser
        
        fields = ['email','password']
        
        



# class SeekerSerializer(serializers.ModelSerializer):

#     email = serializers.EmailField(write_only=True)   # Write only for fields that shouldn't be represented and just wants to used for update or create 
#     first_name = serializers.CharField(write_only=True)  # We have used write_only = True on all the fields that are being inheirted since we sys can't find them in the Provider model, and we want to tell him that we just want to use them for create or update 
#     last_name = serializers.CharField(write_only=True)
#     password = serializers.CharField(write_only=True, style={'input_type': 'password'})
#     ed_level = serializers.CharField()  # Added for Provider's work_email field
        

#     class Meta:
#         model = Seeker
        
#         fields = [
#             'email',
#             'first_name',
#             'last_name',
#             'ed_level',
#             'password',
            
            
#         ]
        
    
#     def create(self, validated_data):
#         user_data = {
#             'email': validated_data['email'].lower(),
#             'first_name': validated_data['first_name'],
#             'last_name': validated_data['last_name'],
#             'password': validated_data['password'],
#             'is_seeker':True
#         }
#         with transaction.atomic():
#             try:
    
#                 user = CustomUser.objects.create_user(**user_data)
                
#                 seeker = Seeker.objects.create(
#                     user=user,
#                     ed_level=validated_data['ed_level']
#                 )
#                 serializer = SeekerSerializer(seeker) # when you try to serialize the object for the response, it is still in an unsaved state and therefore cannot be converted to JSON correctly.
#                 data = serializer.data
#                 group = Group.objects.get(name='Seeker')

#                     # Add the user to the group
#                 group.user_set.add(user)

#                 return user_data
#             except IntegrityError as e:
#                 return ({"Error Message": str(e)})
        
        

