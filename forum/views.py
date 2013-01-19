from django.shortcuts import render, get_object_or_404
from forum.models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# the index for the forum page.
# links to questions, discussions, and polls.
# shows the latest q's, d's, and p's and lists popular tags.
def forum_index(request):
    latest_questions = Question.objects.order_by('-date_posted')[:5]
    return render(request,'forum/index.html',{'questions':latest_questions})

# paginates questions, with optional filters.
def question_index(request,page_number, **kwargs):
    # note: django does lazy query fetching so it does not *actually* fetch all just yet.
    questions = Question.objects.order_by('-date_posted').all()

    # page these questions
    paginator = Paginator(questions,10)
    if page_number == '':
        page_number = 1
    try:
        q_list = paginator.page(page_number)
    except PageNotAnInteger:
        q_list = paginator.page(1)
    except EmptyPage:
        q_list = paginator.page(paginator.num_pages)
    return render(request,'forum/question/index.html',{'questions':q_list})

# displays a question and its respective answers given a question id.
def question_detail(request,qid):
    question = get_object_or_404(Question,id=qid)
    answers = Answer.objects.select_related().get(question=question)
    return render(request, 'form/question/question.html',{'question':question,'answers':answers})

# handles a vote for a question
def handle_vote_question(request):
    if request.user.can_vote_item(direction=
