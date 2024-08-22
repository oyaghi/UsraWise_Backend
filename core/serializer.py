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
        
        

class HobbiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobbies
        fields = ['id', 'name']

class BehaviorChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorChallenges
        fields = ['id', 'name']

class StandardTestScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardTestScore
        fields = ['id', 'name', 'score']

class ChildSerializer(serializers.ModelSerializer):
    hobbies = serializers.PrimaryKeyRelatedField(queryset=Hobbies.objects.all(), many=True)
    behavior_challenges = serializers.PrimaryKeyRelatedField(queryset=BehaviorChallenges.objects.all(), many=True)
    standard_test_score = StandardTestScoreSerializer(many=True)

    class Meta:
        model = Child
        fields = [
            'id', 'parent', 'name', 'age', 'gender', 'learning_style', 
            'gpa', 'grade', 'hobbies', 'behavior_challenges', 
            'standard_test_score', 'adding_date', 'is_active'
        ]
        read_only_fields = ['adding_date']

    def create(self, validated_data):
        hobbies_data = validated_data.pop('hobbies')
        behavior_challenges_data = validated_data.pop('behavior_challenges')
        standard_test_scores_data = validated_data.pop('standard_test_score')
        
        # Create the Child instance
        child = Child.objects.create(**validated_data)
        
        # Add the ManyToMany relationships
        child.hobbies.set(hobbies_data)
        child.behavior_challenges.set(behavior_challenges_data)
        
        # Handle the StandardTestScore with subject and score
        for score_data in standard_test_scores_data:
            subject = StandardTestScore.objects.get(id=score_data['id'])
            child.standard_test_score.add(subject, through_defaults={'score': score_data['score']})
        
        return child

