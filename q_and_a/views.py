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

from django.core.paginator import Paginator

# Create your views here.
class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "OverviewList"
    model = PostItem

    ctx = {}


    def get(self, request, *args, **kwargs):
        ctx = {}
        all_q_list = Question.objects.all().order_by("-date_created")
        all_d_list = Diary.objects.all()
            
        paginator_q = Paginator(all_q_list, 2)
        paginator_d = Paginator(all_d_list, 2)
        p1 = request.GET.get("p1")
        p2 = request.GET.get("p2")

        ctx["Question_list"] = paginator_q.get_page(p1)
        ctx["Diary_list"] = paginator_d.get_page(p2)
        ctx["paginator_q"] = paginator_q

        return render(request, "index.html", ctx)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        n_posts_per_page = 4
        all_q_list = Question.objects.all()
        all_d_list = Diary.objects.all()
            
        Question_list = Question.objects.order_by("-date_created")[:10]
        Diary_list = Diary.objects.order_by("-date_created")[:10]
        paginator_q = Paginator(all_q_list, n_posts_per_page)
        paginator_d = Paginator(all_d_list, n_posts_per_page)

        context["Question_list"] = Question_list
        context["Diary_list"] = Diary_list
        context["paginator_q"] = paginator_q

        return context

class AboutView(TemplateView):
    template_name = "about.html"

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

    return render(request, template_name)

def detail_diary(request, article_id):
    template_name = "detail_question.html"#あとでかえる

    return render(request, template_name)

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