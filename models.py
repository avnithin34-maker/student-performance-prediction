from django.db import models
class PredictionRecord(models.Model):
    student_id = models.CharField(max_length=50, null=True, blank=True)
    attendance = models.FloatField()
    internal1 = models.FloatField()
    internal2 = models.FloatField()
    assignments = models.FloatField()
    study_hours = models.FloatField()
    predicted_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student_id} - {self.predicted_score}"
