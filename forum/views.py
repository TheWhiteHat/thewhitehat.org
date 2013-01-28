from django.shortcuts import render, get_object_or_404
from forum.models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson as json
from whauth.models import User

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
    return render(request,'forum/question/question_list.html',{'questions':q_list})

# displays a question and its respective answers given a question id.
def question_detail(request,slug):
    question = get_object_or_404(Question,slug=slug)
    answers = Answer.objects.select_related().get(question=question)
    return render(request, 'forum/question/question_detail.html',{'question':question,'answers':answers})

# does a string represent an integer?
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def validate_vote_request(objid,direction):
    return (direction == 'up' or direction == 'down') and is_int(objid)

def json_error(msg):
    json_error = {'success':False,'reason':msg}
    return HttpResponse(json.dumps(json_error))

def json_success(msg):
    json_success = {'success':True,'message':msg}
    return HttpResponse(json.dumps(json_success))

# handles a vote from ajax
def handle_vote(request):
    if not request.user.is_authenticated():
        return json_error("user_not_logged_in")
    if request.method == 'POST':
        object_id = object_type = direction = None
        try:
            object_id = request.POST['objid']
            object_type = request.POST['objtype']
            direction = request.POST['dir']
        except KeyError:
            return json_error("invalid_request")


        # make sure object id and direction is valid.
        if not validate_vote_request(object_id,direction):
            return json_error("invalid_vote")

        # handle a vote on a question
        if object_type == 'question':
            try:
                question = Question.objects.get(id=int(object_id))
                try:
                    request.user.vote_on_object(question,direction)
                    return json_success("vote_handled")
                except User.CannotVote:
                    return json_error("user_cannot_vote")
                except User.AlreadyVoted: 
                    return json_error("user_already_voted")

                return json_succcess("vote_handled")

            except Question.DoesNotExist:
                    return json_error("object_does_not_exist")
            
            
        # handle a vote on an answer
        if object_type == 'answer':
            try:
                answer = answer.objects.get(id=int(object_id))
                try:
                    request.user.vote_on_object(answer,direction)
                    return json_success("vote_handled")
                except User.CannotVote:
                    return json_error("user_cannot_vote")
                except User.AlreadyVoted: 
                    return json_error("user_already_voted")

                return json_succcess("vote_handled")

            except Question.DoesNotExist:
                    return json_error("object_does_not_exist")
    else:
        return HttpResponse("not a post")

