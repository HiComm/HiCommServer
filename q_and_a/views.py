from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .forms import PostQuestionForm, PostDiaryForm
from django.utils import timezone
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, DetailView, DeleteView
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator
from django.http import QueryDict

# Create your views here.
class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "OverviewList"
    

    model = PostItem

    ctx = {}


    def get(self, request, *args, **kwargs):
        ctx = {}
        all_q_list = Question.objects.all().order_by("-date_created")
        all_d_list = Diary.objects.all().order_by("-date_created")
        
        n_posts_per_page = 4
        paginator_q = Paginator(all_q_list, n_posts_per_page)
        paginator_d = Paginator(all_d_list, n_posts_per_page)
        p1 = request.GET.get("p1")
        p2 = request.GET.get("p2")

        ctx["Question_list"] = paginator_q.get_page(p1)
        ctx["Diary_list"] = paginator_d.get_page(p2)
        ctx["paginator_q"] = paginator_q

        return render(request, "index.html", ctx)

class AboutView(TemplateView):
    template_name = "about.html"

class ErrorPage(TemplateView):
    template_name = "error.html"

def post_question(request):
    model = Question
    template_name = "post_question.html"
    form_class = PostQuestionForm
    
    ctx = {}

    if request.method == 'POST':#送信時
        form = PostQuestionForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user

            item.is_draft = False
            item.is_solved = False
            item.date_created = timezone.now()
            item.save()

            return redirect(reverse_lazy('q_and_a:index'))

        else:#validじゃないとき（どんなとき？）
            ctx['form'] = form
            return render(request, template_name, ctx)

    else:#入ってきたとき
        ctx['form'] = form_class
        return render(request, template_name, ctx)


def post_diary(request):
    model = Diary
    template_name = "post_article.html"
    form_class = PostDiaryForm
    
    ctx = {}

    if request.method == 'POST':#送信時
        form = PostDiaryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.is_draft = False
            item.date_created = timezone.now()
            item.save()

            return redirect(reverse_lazy('q_and_a:index'))

        else:#validじゃないとき（どんなとき？）
            ctx['form'] = form
            return render(request, template_name, ctx)

    else:#入ってきたとき
        ctx['form'] = form_class
        #ctx['id'] = item.id
        return render(request, template_name, ctx)

def detail_question(request, question_id):
    template_name = "detail_question.html"
    item = Question.objects.get(uuid=question_id)
    answers = Answer.objects.filter(reply_to=question_id).order_by("-point_good", "-date_published")


    context = {"item": item, "answers": answers}

    return render(request, template_name, context)

def detail_diary(request, article_id):
    template_name = "detail_question.html"#あとでかえる
    model = Question

    return render(request, template_name)

#ajax系は以下------------------------------------------------------------

def ajax_submit_good(request):
    if request.is_ajax():
        try:
            rqst = QueryDict(request.body, encoding='utf-8')

            item = (Question if rqst["type"] == "question" else Answer if rqst["type"] == "answer" else Diary if rqst["type"]=="diary" else PostItem).objects.get(uuid=rqst["uuid"])
            user = CustomUser.objects.get(username=rqst["user"])

            if item.author.username == rqst["user"]:#投稿と同一人物はいいねできない
                return HttpResponse("same_person")
            
            if user in item.good_posted_by.all():
                return HttpResponse("double_post")
            item.good_posted_by.add(user)
            item.point_good += 1
            item.save()
            return HttpResponse("true")
        
        except Exception as e:
            print(e)
            return HttpResponse("error")
    return HttpResponse("false")

def ajax_post_answer(request, question_id):
    
    if request.method == 'POST':#送信時

        rqst = QueryDict(request.body, encoding='utf-8')

        question = Question.objects.get(uuid=question_id)

        if Answer.objects.filter(reply_to=question_id, author=request.user):#すでに答えている
            return HttpResponse("answer multi-posting")
        if rqst["body"] == "":#なにもない
            return HttpResponse("null forbidden")

        ans = Answer.objects.create(author=request.user, reply_to=question, body=rqst["body"])
        ans.save()#いる？

        return HttpResponse("true")
        #return redirect(reverse_lazy('q_and_a:detail_question', args=[question_id]))
    else:#error
        return redirect(reverse_lazy("q_and_a:error"))


def ajax_save_draft(request):
    model = Question
    template_name = "post_question.html"
    form_class = PostQuestionForm

    print(request.POST)

    #item = form.save(commit=False)

    if request.method == "POST":
        form = PostQuestionForm(request.POST)
        
        if form.is_valid():
            if Question.objects.filter(pk=request.POST["id"]).exists():
                item = Question.objects.get(pk=request.POST.pk)
                item.author = request.user
                item.is_draft = True
                item.date_created = timezone.now()
                item.save()

            else:
                item = form.save(commit=False)
                item.author = request.user
                item.is_draft = True
                item.date_created = timezone.now()
                item.save()

            return HttpResponse("ok")

        else:
            return HttpResponseBadRequest()

        
    else:
        return HttpResponseBadRequest()