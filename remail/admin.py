from django.contrib import admin
from remail.models import Email, EmailAdmin

admin.site.register(Email, EmailAdmin)
