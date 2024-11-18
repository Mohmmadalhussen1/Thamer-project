from django.contrib import admin
from .models import Company

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'local_score',
        'ikteva_score_now',
        'ikteva_score_before',
        'pdf_file_local_display',
        'pdf_file_ikteva_display',
        'status'
    )
    actions = ['approve_companies', 'reject_companies']

    def approve_companies(self, request, queryset):
        queryset.update(status='approved')

    def reject_companies(self, request, queryset):
        queryset.update(status='rejected')


    def pdf_file_local_display(self, obj):
        return obj.pdf_file_local.name if obj.pdf_file_local else 'No PDF'
    pdf_file_local_display.short_description = 'PDF File for Local'

    def pdf_file_ikteva_display(self, obj):
        return obj.pdf_file_ikteva.name if obj.pdf_file_ikteva else 'No PDF'
    pdf_file_ikteva_display.short_description = 'PDF File for Ikteva'




admin.site.register(Company, CompanyAdmin)