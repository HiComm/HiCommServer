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

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.core.paginator import Paginator
from django.http import QueryDict
from django.core import serializers
from django.db.models import Q

import re
import json

# Create your views here.
class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "OverviewList"
    

    model = PostItem

    ctx = {}


    def get(self, request, *args, **kwargs):
        ctx = {}
        all_q_list = Question.objects.filter(is_draft=False).order_by("-date_created")
        all_d_list = Diary.objects.filter(is_draft=False).order_by("-date_created")
        
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
        print(request.POST)

        form = PostQuestionForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.author = request.user

                if request.POST["dftid"] != "initial":
                    item.uuid = request.POST["dftid"]

                item.is_draft = False
                item.is_solved = False
                item.date_created = timezone.now()
                item.date_modified = timezone.now()
                item.date_published = timezone.now()

                item.save()


                for tagname in request.POST["tags"].split(","):
                    if tagname:
                        if Tag.objects.filter(name=tagname).exists():
                            tag = Tag.objects.get(name=tagname)
                            item.tags.add(tag)
                        else:
                            new_tag = Tag.objects.create(name=tagname)
                            item.tags.add(new_tag)
                
                #item.save()

                return redirect(reverse_lazy('q_and_a:index'))
            except Exception as e:
                print(e)
                return redirect(reverse_lazy("q_and_a:error"))

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
        try:
            form = PostDiaryForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.author = request.user
                item.is_draft = False
                item.date_created = timezone.now()
                item.save()
                
                for tagname in request.POST["tags"].split(","):
                    if tagname:
                        if Tag.objects.filter(name=tagname).exists():
                            tag = Tag.objects.get(name=tagname)
                            item.tags.add(tag)
                        else:
                            new_tag = Tag.objects.create(name=tagname)
                            item.tags.add(new_tag)
                            
                return redirect(reverse_lazy('q_and_a:index'))

            else:#validじゃないとき
                return redirect(reverse_lazy("q_and_a:error"))
        except Exception as e:
            print(e)
            return redirect(reverse_lazy("q_and_a:error"))

    else:#入ってきたとき
        ctx['form'] = form_class
        #ctx['id'] = item.id
        return render(request, template_name, ctx)

def detail_question(request, question_id):
    try:
        template_name = "detail_question.html"
        item = Question.objects.get(uuid=question_id)
        answers = Answer.objects.filter(reply_to=question_id).order_by("-point_good", "-date_published")

        is_already_answered = False
        for ans in answers:
            if request.user == ans.author:
                is_already_answered = True

        is_good_posted = False
        for usr in item.good_posted_by.all():
            if request.user == usr:
                is_good_posted = True


        context = {
            "item": item, 
            "answers": answers,
            "already_answered": is_already_answered,
            "good_posted": is_good_posted,
        }

        return render(request, template_name, context)
    except Exception as e:
        print(e)
        return redirect(reverse_lazy("q_and_a:error"))

def detail_diary(request, article_id):
    try:
        template_name = "detail_article.html"#あとでかえる
        item = Diary.objects.get(uuid=article_id)
    
        is_good_posted = False
        for usr in item.good_posted_by.all():
            if request.user == usr:
                is_good_posted = True
        context = {
            "item": item,
            "good_posted": is_good_posted,
        }

        return render(request, template_name, context)
    except Exception as e:
        print(e)
        return redirect(reverse_lazy("q_and_a:error"))

def search_result(request):
    try:
        template_name = "search.html"#
        query = request.GET["query"]
        query_list = re.split(' (?=(?:(?:[^"]*"){2})*[^"]*$)', query)
        
        qobj = Q()

        for q_word in query_list:
            if q_word:
                if q_word[0] == "\"" and q_word[-1] == "\"":
                    qobj |= Q(title__icontains=q_word[1:-1])
                    qobj |= Q(body__icontains=q_word[1:-1])
                else:
                    qobj |= Q(title__icontains=q_word)
                    qobj |= Q(body__icontains=q_word)
        
        print(qobj)
        questions = Question.objects.filter(qobj)
        articles = Diary.objects.filter(qobj)

        context = {
            "query": query,
            "Question_list": questions,
            "Diary_list": articles,
        }
        return render(request, template_name, context)
    except Exception as e:
        print(e)
        return redirect(reverse_lazy("q_and_a:error"))


#ajax系は以下------------------------------------------------------------

def ajax_set_bestanswer(request, question_id):
    if request.is_ajax():
        try:
            ans = Answer.objects.get(uuid=QueryDict(request.body, encoding='utf-8')["id"])
            qst = Question.objects.get(uuid=question_id)
            if qst.author == request.user:#自分の質問
                if not qst.is_solved:
                    ans.is_BestAnswer = True
                    qst.is_solved = True
                    ans.save()
                    qst.save()
                    return HttpResponse("OK1")
                else:#取り消す場合
                    if ans.is_BestAnswer == True:
                        ans.is_BestAnswer = False
                        qst.is_solved = False
                        ans.save()
                        qst.save()
                        return HttpResponse("OK2")
                    return HttpResponse("ERR")
            else:
                return HttpResponse("ERR")



        except Exception as e:
            print(e)
            return HttpResponse("ERR")

    return HttpResponseBadRequest()

def ajax_submit_good(request):
    if request.is_ajax():
        try:
            rqst = QueryDict(request.body, encoding='utf-8')

            item = (Question if rqst["type"] == "question" else Answer if rqst["type"] == "answer" else Diary if rqst["type"]=="diary" else Comment).objects.get(uuid=rqst["uuid"])
            user = CustomUser.objects.get(username=rqst["user"])

            if item.author == request.user:#投稿と同一人物はいいねできない
                return HttpResponse("same_person")
            
            if user in item.good_posted_by.all():#いいねしている場合→減算
                item.good_posted_by.remove(user)
                item.point_good -= 1
                item.save()
                return HttpResponse("02E"+str(item.point_good))

            else:#いいねしていない場合
                item.good_posted_by.add(user)
                item.point_good += 1
                item.save()
                return HttpResponse("01E"+str(item.point_good))
        
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
        question.num_answers += 1
        ans.save()#いる？
        question.save()

        return HttpResponse("true")
        #return redirect(reverse_lazy('q_and_a:detail_question', args=[question_id]))
    else:#error
        return redirect(reverse_lazy("q_and_a:error"))


def ajax_save_draft(request):

    if request.method == "POST":
        try:
            rqst = QueryDict(request.body, encoding='utf-8')
            Model = Question if rqst["type"]=="question" else Diary if rqst["type"]=="article" else PostItem

            if Model == PostItem:
                return HttpResponseBadRequest("unsupported model type")
            
            if rqst["id"] == "initial":
                ans = Model.objects.create(author=request.user, title=rqst["title"], body=rqst["body"], is_draft=True)
                ans.date_created = timezone.now()
                ans.save()
            else:
                ans = Model.objects.get(uuid=rqst["id"])

                #自分のものである認証(勝手に書き換えないように)
                if ans.author != request.user:
                    return HttpResponseBadRequest("internal server error")

                ans.date_modified = timezone.now()
                ans.title = rqst["title"]
                ans.body = rqst["body"]
                ans.save()

            uuid = str(ans.uuid.hex)
            uuid = "{}-{}-{}-{}-{}".format(uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])

            return HttpResponse(uuid)
        
        except Exception as e:
            return HttpResponseBadRequest("internal server error")
        
    else:
        return HttpResponseBadRequest()

def ajax_get_q_drafts(request):
    output = []
    if request.method == "POST":
        try:
            drafts = Question.objects.filter(author=request.user, is_draft=True).order_by("-date_modified")
            #draft_list = serializers.serialize('json', drafts)
            for draft in drafts:
               data = {}
               uuid = str(draft.uuid.hex)
               data["uuid"] = "{}-{}-{}-{}-{}".format(uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])
               data["date_created"] = str(draft.date_created)
               data["date_modified"] = str(draft.date_modified)
               data["title"] = draft.title
               data["body"] = draft.body
               output.append(data)
            
            return HttpResponse(json.dumps(output))
            
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("internal server error")
        
    else:
        return HttpResponseBadRequest()

def ajax_get_d_drafts(request):
    output = []
    if request.method == "POST":
        try:
            drafts = Diary.objects.filter(author=request.user, is_draft=True).order_by("-date_modified")
            #draft_list = serializers.serialize('json', drafts)
            for draft in drafts:
               data = {}
               uuid = str(draft.uuid.hex)
               data["uuid"] = "{}-{}-{}-{}-{}".format(uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])
               data["date_created"] = str(draft.date_created)
               data["date_modified"] = str(draft.date_modified)
               data["title"] = draft.title
               data["body"] = draft.body
               output.append(data)
            
            return HttpResponse(json.dumps(output))
            
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("internal server error")
        
    else:
        return HttpResponseBadRequest()

def ajax_post_comment(request):
    if request.method == "POST":
        try:
            rqst = QueryDict(request.body, encoding='utf-8')
            id = rqst["id"]

            if Question.objects.filter(uuid=id).exists():
                item = Question.objects.get(uuid=id)
                comment = Comment(author=request.user, body=rqst["body"], is_draft=False, post_to=item)
                comment.save()
            elif Answer.objects.filter(uuid=id).exists():
                item = Answer.objects.get(uuid=id)
                comment = Comment(author=request.user, body=rqst["body"], is_draft=False, post_to=item)
                comment.save()
            elif Diary.objects.filter(uuid=id).exists():
                item = Diary.objects.get(uuid=id)
                comment = Comment(author=request.user, body=rqst["body"], is_draft=False, post_to=item)
                comment.save()
            else:
                return HttpResponseBadRequest("internal server error")

            return HttpResponse("OK")

        except Exception as e:
            print(e)
            return HttpResponseBadRequest("internal server error")

    else:
        return HttpResponseBadRequest()

def ajax_get_tags_json(request):
    if request.method == "POST":
        try:
            tags = Tag.objects.all()
            data = json.dumps([tag for tag in tags.values()])
            return HttpResponse(data)

        except Exception as e:
            print(e)
            return HttpResponseBadRequest("internal server error")

    else:
        return HttpResponseBadRequest()