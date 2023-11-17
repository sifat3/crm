from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Completed_Project)
admin.site.register(Ongoing_project)
admin.site.register(Freelancer)
admin.site.register(Token)