from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from qanda.models import *
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
import markdown2
import bleach
from .forms import QuestionForm


def index(request):
    context = {}
    context['questions'] = Question.objects.all()
    return render(request, 'qanda_index.html', context)

@login_required
def askquestion(request):
    if request.method == 'POST':
        # title = request.POST.get('title')
        # question = request.POST.get('question')
        # posted_by = request.POST.get('posted_by')
        # q = Question(question_title=title, question_text=question, posted_by=posted_by)
        # q.save()

        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.posted_by = request.user
            q = form.instance
            form.save()
            return redirect(reverse('qanda:view-question',kwargs={'qid':q.qid , 'qslug':q.slug} ))
    else:
        form = QuestionForm()
        return render(request, 'ask_question.html', {'form': form})

def viewquestion(request, qid, qslug):
    context = {}
    question = Question.objects.get(qid=qid, slug=qslug)
    # assuming obj is a model instance
    question_json = json.loads(serializers.serialize('json', [ question ]))[0]['fields']
    question_json['date_posted'] = question.date_posted
    question_json['qid'] = question.qid
    question_json['posted_by'] = question.posted_by
    question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
    context['question'] = question_json
    context['answers'] = []
    answers = Answer.objects.filter(qid=qid)
    for answer in answers:
        answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
        context['answers'].append(answer)
    return render(request, 'view_question.html', context)

@login_required
@csrf_exempt
def ajaxanswerquestion(request):
    if request.method == 'POST':
        try:

            json_data = json.loads(request.body)
            answer = json_data['answer']
            posted_by = request.user
            qid = json_data['qid']
            a = Answer(answer_text=answer, posted_by=posted_by, qid=Question.objects.get(qid=qid))
            a.save()
            return JsonResponse({'Success': 'Answer posted successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'Something went wrong when posting your answer.'})
