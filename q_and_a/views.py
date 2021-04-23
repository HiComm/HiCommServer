from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .forms import PostQuestionForm, PostDiaryForm
from django.utils import timezone
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect

# Create your views here.
class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "OverviewList"
    queryset = PostItem.objects.order_by("-date_created")
    model = PostItem

    paginate_by = 4


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["Question_list"] = Question.objects.order_by("-date_created")[:10]
        context["Diary_list"] = Diary.objects.order_by("-date_created")[:10]

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
        
            item.date_created = timezone.now()
            item.save()

            return redirect(reverse_lazy('q_and_a:index'))

        else:#validじゃないとき（どんなとき？）
            ctx['form'] = form
            return render(request, template_name, ctx)

    else:#入ってきたとき
        ctx['form'] = form_class
        return render(request, template_name, ctx)