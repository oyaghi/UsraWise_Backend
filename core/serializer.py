from rest_framework import serializers
from .models import  CustomUser, Child, Hobbies, BehaviorChallenges, StandardTestScore, TestScoreThroughModel
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
    parenting_style = serializers.CharField(write_only=True)

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
            'parenting_style',
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
            'number_of_children': validated_data['number_of_children'],
            'parenting_style': validated_data['parenting_style']
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
    def update(self, instance, validated_data):
        # If password is being updated, handle it separately
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # Update the rest of the fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance


        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = CustomUser
        
        fields = ['email','password']
        
        

class TestScoreThroughModelSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=StandardTestScore.objects.all())
    score = serializers.IntegerField()

    class Meta:
        model = TestScoreThroughModel
        fields = ['id', 'score']


class ChildSerializer(serializers.ModelSerializer):
    hobbies = serializers.PrimaryKeyRelatedField(many=True, queryset=Hobbies.objects.all())
    behavior_challenges = serializers.PrimaryKeyRelatedField(many=True, queryset=BehaviorChallenges.objects.all())
    standard_test_score = TestScoreThroughModelSerializer(many=True, source='testscorethroughmodel_set')

    class Meta:
        model = Child
        fields = [
            'parent', 'name', 'age', 'gender', 'learning_style', 'gpa', 'grade', 
            'hobbies', 'behavior_challenges', 'standard_test_score'
        ]

    def create(self, validated_data):
        child_data = {
            'parent': validated_data['parent'],
            'name': validated_data['name'],
            'age': validated_data['age'],
            'gender': validated_data['gender'],
            'learning_style': validated_data['learning_style'],
            'gpa': validated_data['gpa'],
            'grade': validated_data['grade'],
        }
        
        # Create the Child instance
        child = Child.objects.create(**child_data)
        # Handle many-to-many relationships for hobbies and behavior challenges
        if 'hobbies' in validated_data:
            child.hobbies.set(validated_data['hobbies'])
        if 'behavior_challenges' in validated_data:
            child.behavior_challenges.set(validated_data['behavior_challenges'])
        # Handle the many-to-many relationship for standard_test_score using the through model
        print(validated_data)
        if 'testscorethroughmodel_set' in validated_data:
            for test_score_data in validated_data['testscorethroughmodel_set']:
                standard_test_score_id = test_score_data['id'].id
                score = test_score_data['score']
                                
                # Create the TestScoreThroughModel instance
                TestScoreThroughModel.objects.create(
                    child=child,
                    standard_test_score_id=standard_test_score_id,
                    score=score
                )
        return child
    def update(self, instance, validated_data):
    # Update basic child data directly on the instance
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.learning_style = validated_data.get('learning_style', instance.learning_style)
        instance.gpa = validated_data.get('gpa', instance.gpa)
        instance.grade = validated_data.get('grade', instance.grade)

        # Save the updated instance
        instance.save()

        # Update many-to-many relationships
        if 'hobbies' in validated_data:
            instance.hobbies.set(validated_data['hobbies'])
        if 'behavior_challenges' in validated_data:
            instance.behavior_challenges.set(validated_data['behavior_challenges'])
        # Handle the many-to-many relationship for standard_test_score using the through model
        print(validated_data)
        if 'testscorethroughmodel_set' in validated_data:
            for test_score_data in validated_data['testscorethroughmodel_set']:
                standard_test_score_id = test_score_data['id'].id
                score = test_score_data['score']
                                
                # Create the TestScoreThroughModel instance
                TestScoreThroughModel.objects.create(
                    child=instance,
                    standard_test_score_id=standard_test_score_id,
                    score=score
                )

        return instance




class GetParentSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    name = serializers.CharField()
    phone = serializers.CharField()
    age = serializers.CharField()
    gender = serializers.CharField()
    occupation = serializers.CharField()
    education_level = serializers.CharField()
    number_of_children = serializers.IntegerField()
    parenting_style= serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Keep this write-only

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
            'parenting_style',
            'password',
        ]

# class GetChildserializer(serializers.ModelSerializer):
    
#     hobbies = serializers.PrimaryKeyRelatedField(many=True, queryset=Hobbies.objects.all())
#     behavior_challenges = serializers.PrimaryKeyRelatedField(many=True, queryset=BehaviorChallenges.objects.all())
#     standard_test_score = TestScoreThroughModelSerializer(many=True, source='testscorethroughmodel_set')

#     class Meta:
#         model = Child
#         fields = [
#             'parent', 'name', 'age', 'gender', 'learning_style', 'gpa', 'grade', 
#             'hobbies', 'behavior_challenges', 'standard_test_score'
#         ]




#Child retrival +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



class ChildTestScoreThroughModelSerializer(serializers.ModelSerializer):
    standard_test_score_id = serializers.IntegerField(source='standard_test_score.id')
    standard_test_score_name = serializers.CharField(source='standard_test_score.name')

    class Meta:
        model = TestScoreThroughModel
        fields = ['standard_test_score_id', 'standard_test_score_name', 'score']

class ChildHobbiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobbies
        fields = ['id', 'name']


class ChildBehaviorChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorChallenges
        fields = ['id', 'name']


class ChildChildSerializer(serializers.ModelSerializer):
    standard_test_score = ChildTestScoreThroughModelSerializer(many=True, source='testscorethroughmodel_set')
    hobbies = ChildHobbiesSerializer(many=True)
    behavior_challenges = ChildBehaviorChallengesSerializer(many=True)

    class Meta:
        model = Child
        fields = [
            'parent',
            'name',
            'age',
            'gender',
            'learning_style',
            'gpa',
            'grade',
            'hobbies',
            'behavior_challenges',
            'standard_test_score'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['standard_test_score'] = [
            {
                'id': test_score['standard_test_score_id'],
                'name': test_score['standard_test_score_name'],
                'score': test_score['score']
            }
            for test_score in representation['standard_test_score']
        ]
        # Format the hobbies field to include both id and name
        representation['hobbies'] = [
            {'id': hobby['id'], 'name': hobby['name']}
            for hobby in representation['hobbies']
        ]
        
        # Format the behavior_challenges field to include both id and name
        representation['behavior_challenges'] = [
            {'id': challenge['id'], 'name': challenge['name']}
            for challenge in representation['behavior_challenges']
        ]

        return representation
    
    
    
# AI data structure 
"""
{
    "age": 9,
    "grade_level": "4th",
    "gender": "Female",
    "learning_style": "Kinesthetic",
    "hobbies": ["Playing Piano", "Swimming"],
    "education_level": "High School Diploma",
    "occupation": "Teacher",
    "parenting_style": "Supportive",
    "overall_performance_level": "Average",
    "standardized_test_scores": {
        "Math": "70th percentile",
        "Reading": "65th percentile",
        "Science": "72nd percentile"
    },
    "behavioral_challenges": "Struggles with organization, occasionally disruptive in class, needs encouragement to participate",
    "response_json": json.dumps(RESPONSE_JSON)
})
    
"""

"""
Parent:
education_level 
occupation
parenting_style: ??????!

"""


"""
Child:
age
grade_level
learning_style 
hobbies 
gpa (overall_performance_level)
standard_test_score (standardized_test_scores)
behavioral_challenges 

"""