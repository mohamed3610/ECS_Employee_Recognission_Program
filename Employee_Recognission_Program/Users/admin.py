from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import User
from .resources import UsersResource

# Register your models here.



@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = UsersResource
