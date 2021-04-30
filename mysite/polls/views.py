from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# geneic view는 URL에서 캡처된 기본 키 값이 "pk"라고 기대하기 때문에
# question_id를 generic view를 위해 pk로 변경
# 기본적으로 DetailView generic view는 <app name>/<model name>_detail.html
# 템플릿을 사용 => "polls/question_detail.html"

# 위가 장고의 일반적인 뷰, 아래는 이해를 위한 뷰
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# 모든 뷰에 render() 적용할 시, loader와 HttpResponse를 import하지 않아도 됨.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


# Leave the rest of the views (detail, results, vote) unchanged

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# 위가 장고의 일반적인 뷰, 아래는 이해를 위한 뷰
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})


# from django.shortcuts import get_object_or_404
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# get_object_or_404 처럼 동작하는 get_list_or_404 함수도 존재함
# get() 대신 filter()를 쓰는 것만 다름.(리스트가 비어있을 경우 Http404)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# 위가 장고의 일반적인 뷰, 아래는 이해를 위한 뷰
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # question voting form을 다시 보여줌
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST data가 잘 처리되었으면 언제나 HttpResponseRedirect를 줘서
        # 유저가 뒤로 가기 버튼을 눌렀을 때 2번 전송되는 것을 방지함
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# request.POST의 값은 항상 문자열들임.
# reverse() 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와줌.






