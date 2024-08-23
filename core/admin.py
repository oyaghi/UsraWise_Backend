from django.contrib import admin
from .models import CustomUser
from .models import Child
from .models import Hobbies
from .models import BehaviorChallenges
from .models import StandardTestScore, TestScoreThroughModel 
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Child)
admin.site.register(Hobbies)
admin.site.register(BehaviorChallenges)
admin.site.register(StandardTestScore)
admin.site.register(TestScoreThroughModel)

