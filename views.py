from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import PredictionForm
from .models import PredictionRecord
import pickle, os, numpy as np
from django.contrib.auth.decorators import login_required

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'prediction_app', 'ml_model', 'model.pkl')

# ✅ Load ML model only when needed (avoids migration errors)
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def home(request):
    return render(request, 'prediction_app/home.html')


def register_view(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            msg = 'User already exists'
        else:
            User.objects.create_user(username=username, password=password)
            msg = 'User created successfully'

    return render(request, 'prediction_app/register.html', {'msg': msg})


def login_view(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

        msg = 'Invalid credentials'

    return render(request, 'prediction_app/login.html', {'msg': msg})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    records = PredictionRecord.objects.all().order_by('-timestamp')[:500]
    ins1 = [r.internal1 for r in records]
    ins2 = [r.internal2 for r in records]
    labels = list(range(len(ins1)))

    return render(request, 'prediction_app/dashboard.html', {
        'labels': labels[:50],
        'ins1': ins1[:50],
        'ins2': ins2[:50],
    })


def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():

            # ✅ Load model when needed
            model = load_model()

            sid = form.cleaned_data.get('student_id')
            attendance = form.cleaned_data['attendance']
            internal1 = form.cleaned_data['internal1']
            internal2 = form.cleaned_data['internal2']
            assignments = form.cleaned_data['assignments']
            study_hours = form.cleaned_data['study_hours']
            previous_marks = form.cleaned_data['previous_marks']  # ✅ New field

            # ✅ Ensure order matches training dataset (6 features)
            features = np.array([[attendance, internal1, internal2, assignments, study_hours, previous_marks]])

            # ✅ Predict final score
            pred = float(model.predict(features)[0])

            # ✅ Save record to DB
            PredictionRecord.objects.create(
                student_id=sid,
                attendance=attendance,
                internal1=internal1,
                internal2=internal2,
                assignments=assignments,
                study_hours=study_hours,
                predicted_score=pred
            )

            return render(request, 'prediction_app/result.html', {
                'student_id': sid,
                'prediction': round(pred, 2)
            })

    else:
        form = PredictionForm()

    return render(request, 'prediction_app/predict.html', {'form': form})
