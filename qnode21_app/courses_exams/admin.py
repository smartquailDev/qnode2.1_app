from django.contrib import admin
from .models import SubjectTest, Test , Instrucciones

@admin.register(Instrucciones)
class InstruccionesAdmin(admin.ModelAdmin):
    list_display = ['Title_A', 'Title_B', 'Title_C', 'Title_D']


@admin.register(SubjectTest)
class SubjectTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['subject_test','slug', 'value', 'available']
    list_filter = ['available']
    list_editable = ['value','available']
    prepopulated_fields = {'slug': ('question',)}
