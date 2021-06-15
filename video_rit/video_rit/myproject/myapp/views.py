from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import datetime
import re
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


# Create your views here.

@login_required(login_url='login-h')
def home(request):
    return render(request, 'index.html')


def loginpage(request):
    last_login.objects.all().delete()
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        except:
            messages.warning("Fill the details")
        if user is not None:
            login(request, user)
            chat_model.objects.all().delete()
            var = last_login(username=username, password=password)
            var.save()
            return redirect('home')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def staff_home(request):
    return render(request, 'staff-home.html')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login-h')
    context = {'form': form}
    return render(request, 'user_reg.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login-h')


def upload_video(request):
    person = last_login.objects.all().last()
    id1 = User.objects.get(username=person.username)
    form = UploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

        var = Video.objects.all().last()
        h = video_details(uploader=id1, Date=datetime.datetime.now(), video=var)
        h.save()
        messages.success(request, 'video uploded')
        return redirect('home')
    return render(request, 'upload.html', {'form': form})


def display(request):
    person = last_login.objects.all().last()
    id1 = User.objects.get(username=person.username)
    videos = video_details.objects.all()
    for i in videos:
        print(i.video)
    print("----v----", videos)
    context = {
        'videos': videos
    }
    return render(request, 'videos.html', context)


def view_video(request, id=0):
    person = last_login.objects.all().last()
    id1 = User.objects.get(username=person.username)
    videos = Video.objects.get(id=id)
    context = {
        'video': videos
    }
    df = pd.read_csv("data/feedback.csv", header=0, encoding='unicode_escape')
    df = df.dropna()
    data = []
    for index, rows in df.iterrows():
        a = (rows['statement'], rows['overview'])
        data.append(a)
    cl = NaiveBayesClassifier(data)
    if request.method == 'POST':
        form = feedback_Form(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            pred1 = cl.classify(feedback)
            g = feedback_model(feedback=pred1)
            g.save()
            h = user_feedback(username=id1, feedback=feedback_model.objects.all().last(),
                              Date=datetime.datetime.today(), video=videos)
            h.save()
            context = {
                'video': videos,
                'msg': 'successfully stored'
            }
            return render(request, 'video.html', context)
    return render(request, 'video.html', context)


def user_search(request):
    if request.method == 'POST':
        form = Search_form(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(search)
            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
            print(filtered_sentence)
            list1 = []
            for i in filtered_sentence:
                s = re.sub(r"[^a-z]", "", i.lower())
                if s.isalpha():
                    list1.append(s)
                    id = Search_words.objects.filter(keywords=s).last()
                    if type(id) == type(None):
                        g = Search_words(keywords=s, count=1)
                        g.save()
                    else:
                        g = Search_words(id=id.id, keywords=s, count=int(id.count) + 1)
                        g.save()
            video = Video.objects.all()
            list2 = []
            for i in video:
                str(i.keywords).split(',')
                list2.extend([i for w in list1 if w in str(i.keywords).split(',')])
            print(list2)
            list2 = list(set(list2))
            for i in list2:
                print(i.id)
            context = {
                'videos': list2
            }
            return render(request, 'view_videos.html', context)
    return render(request, 'search.html')


def chat(request):
    person = last_login.objects.all().last()
    id1 = User.objects.get(username=person.username)
    if request.method == 'POST':
        form = Chat_form(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(question)
            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
            print(filtered_sentence)
            list1 = []
            for i in filtered_sentence:
                s = re.sub(r"[^a-z]", "", i.lower())
                if s.isalpha() and s!='explain':
                    list1.append(s)
            print(question)
            print(list1)
            list2 =[]
            for i in list1:
                syns = wordnet.synsets(i)
                try:
                    print("Defination of the said word:")
                    print(syns[0].definition())
                    list2.append(syns[0].definition())
                except:
                    pass
                if i == 'example':
                    try:
                        print("\nExamples of the word in use::")
                        print(syns[0].examples())
                        list2.append(syns[0].examples())
                    except:
                        pass
            try:
                list2=list(set(list2))
            except:
                pass
            if len(list2) == 0:
                list2.append('I could not understand Please ask me a another question')
            g= chat_model(question=question,answer=list2)
            g.save()
            var = chat_model.objects.all()
            return render(request,'chat.html',{'value':var})
    return render(request, 'chat.html')
