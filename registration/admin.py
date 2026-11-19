from django.contrib import admin

from .models import student


@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'contact_number',
    )
    list_filter = ('gender',)
    search_fields = ('student_id', 'first_name', 'last_name')
