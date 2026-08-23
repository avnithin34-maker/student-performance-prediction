from django import forms

class PredictionForm(forms.Form):
    student_id = forms.CharField(
        required=False,
        max_length=50,
        label='Student ID (optional)'
    )
    attendance = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Attendance (%)'
    )
    internal1 = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Internal Test 1'
    )
    internal2 = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Internal Test 2'
    )
    assignments = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Assignments Score'
    )
    study_hours = forms.FloatField(
        min_value=0,
        label='Daily Study Hours'
    )
    previous_marks = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Previous Semester Marks'
    )


