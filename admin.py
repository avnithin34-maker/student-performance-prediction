from django.contrib import admin
from .models import PredictionRecord
@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('student_id','predicted_score','timestamp')
    search_fields = ('student_id',)
