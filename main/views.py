from django.shortcuts import render, redirect
from random import choice, sample
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Option, QuestionSet
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from .forms import QuizForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error = "Foydalanuvchi nomi yoki parol noto'g'ri."
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


def is_admin(user):
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper


def index(request):
    return render(request, 'base.html')


#Quiz----------------------------------------------------------------------------------
def list_quiz(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


def read_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quiz/read_quiz.html', {'quiz': quiz})

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})


def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('/')


def list_question(request):
    questions = Question.objects.all()
    return render(request, 'question/question_list.html', {'questions': questions})


def questionCreate(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')

        question_set, created = QuestionSet.objects.get_or_create(quiz=quiz) 

        question = Question(name=question_text, set=question_set) 
        question.save()

        options = [option1, option2, option3, option4]
        correct_index = ['option1', 'option2', 'option3', 'option4'].index(correct_answer)

        for i, option in enumerate(options):
            Option(name=option, question=question, correct=i==correct_index).save()

        return redirect('index')
    return render(request, 'question/question_create.html', {'quiz': quiz})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    options = Option.objects.filter(question=question)
    return render(request, 'question/question_detail.html', {'question': question, 'options': options})


def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('index')


def delete_option(request, pk):
    option = get_object_or_404(Option, pk=pk)
    option.delete()
    return redirect('index')
