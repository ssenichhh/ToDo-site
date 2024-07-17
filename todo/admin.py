from django.contrib import admin
from .models import Todo


class Admin(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(Todo, Admin)
