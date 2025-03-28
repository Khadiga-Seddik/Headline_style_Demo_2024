from django.contrib import admin
from survey_app.models import News_article, Personal_info
# from import_export.admin import ImportExportModelAdmin
from django import forms
import csv
from django.http import HttpResponse

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()



def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = description
    return export_as_csv



# @admin.register(Personal_info)
class Personal_infoAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'selected_articles_list', 'headline_style')
    actions = [export_as_csv_action("CSV Export")]

# @admin.register(Personal_info)
class News_articlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'aid', 'title', 'style', 'manipulated_title')
    actions = [export_as_csv_action("CSV Export")]



# Register your models here.
admin.site.register(News_article, News_articlesAdmin)
admin.site.register(Personal_info, Personal_infoAdmin)