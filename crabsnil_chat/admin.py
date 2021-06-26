from django.contrib import admin
from .models import User, User_Friends
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class user_admin(UserAdmin):
    model = User
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Details',
            {
                'fields': (
                    'userid',
                )
            }
        )
    )


admin.site.register(User, user_admin)
admin.site.register(User_Friends)
