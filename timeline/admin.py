from django.contrib import admin
from .models import Comentario

class ComentarioAdmin(admin.ModelAdmin):
	list_display = ('estudiante', 'comentario', 'fecha',)

admin.site.register(Comentario, ComentarioAdmin)

