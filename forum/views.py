from django.shortcuts import render, get_object_or_404
from forum.models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import simplejson as json
from whauth.models import User
from forum.models import *
from django.db.models import Q
from django.template.defaultfilters import slugify

# the index for the forum page.
# links to questions, discussions, and polls.
# shows the latest q's, d's, and p's and lists popular tags.
def forum_index(request):
    latest_questions = Question.objects.order_by('-date_posted')[:5]
    return render(request,'forum/index.html',{'questions':latest_questions})

# paginates questions, with optional filters.
def question_index(request,page_number, **kwargs):
    # note: django does lazy query fetching so it does not *actually* fetch all just yet.
    questions = Question.objects.select_related().order_by('-date_posted').all()

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
    answers = Answer.objects.select_related().filter(question=question)
    request.session['current_question'] = question.id
    if request.user.is_authenticated():
        # filter things that user has voted on.
        vote_filter = Q(object_id=question.id)
        for answer in answers:
            vote_filter = vote_filter | Q(object_id=answer.id)
        vote_filter = (vote_filter) & Q(user=request.user)
        user_votes = Vote.objects.filter(vote_filter).all()

        # send the template something that it can index into without
        object_vote_ids = [v.content_type.model+str(v.id)+v.direction for v in user_votes]
    else:
        object_vote_ids = None

    form = SubmitAnswerForm()
    return render(request, 'forum/question/question_detail.html',{'question':question,'answers':answers,'form':form,'votes':object_vote_ids})

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

        obj = None

        # handle a vote on a question
        if object_type == 'question':
            try:
                obj = Question.objects.get(id=int(object_id))
            except Question.DoesNotExist:
                    return json_error("object_does_not_exist")

        # handle a vote on an answer
        if object_type == 'answer':
            try:
                obj = Answer.objects.get(id=int(object_id))
            except Answer.DoesNotExist:
                    return json_error("object_does_not_exist")

        # vote on the object
        try:
            request.user.vote_on_object(obj,direction)
            return json_success("vote_handled")
        except User.CannotVote:
                return json_error("user_cannot_vote")
        except User.AlreadyVoted: 
                return json_error("user_already_voted")

    else:
        return HttpResponse("not a post")


# handle an answer to a question
@login_required
def handle_answer(request):
    if request.method == 'POST':
        form = SubmitAnswerForm(request.POST)
        if form.is_valid():
            try:
                qid = form.cleaned_data['qid']
                answer_body = form.cleaned_data['answer_body']
                # make sure that users aren't 'answering' questions that
                # that they aren't looking at.
                try:
                    if request.session['current_question'] != qid:
                        return render(request,"error.html",{'error':'Nonmatching question and session id'})
                except KeyError:
                        return render(request,"error.html",{'error':'Session trouble'})

                question = Question.objects.get(id=qid)
                answer = Answer()
                answer.question = question
                answer.body_markdown = answer_body
                answer.author = request.user
                answer.save()
                return HttpResponseRedirect(reverse('question_detail',kwargs={'slug':question.slug}))
            except Question.DoesNotExist:
               return render(request,"error.html",{'error':'Question does not exist'})
        else:
            return render(request,"error.html",{'error':'Invalid form post'})

@login_required
def new_question(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.body_markdown = form.cleaned_data['body_text']
            question.author = request.user

            tags = form.cleaned_data['tags'].split(",")
            tag_objects = []
            for tag in tags:
                tag_name = slugify(tag)
                tag_object = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag_object)

            question.save()
    else:
        form = NewQuestionForm()

    tags = Tag.objects.all()
    return render(request,"forum/question/new_question.html",{'form':form,'tags':tags})
