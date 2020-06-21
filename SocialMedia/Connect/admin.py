from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.UserDataBase)
admin.site.register(models.Connections)
admin.site.register(models.Company_Model)
admin.site.register(models.Blog_Model)
admin.site.register(models.Post_Likes)