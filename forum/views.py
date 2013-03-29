from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson as json
from whauth.models import User
from forum.models import Vote, Question, Answer, SubmitAnswerForm, \
    NewQuestionForm, Thread, Post, Board, NewThreadForm, ThreadIcon,\
    NewPostForm
from blog.models import Tag
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


# the index for the forum page.
# links to questions, discussions, and polls.
# shows the latest q's, d's, and p's and lists popular tags.
def forum_index(request):
    latest_questions = Question.objects.order_by('-date_posted')[:5]
    return render(request, 'forum/index.html', {'questions': latest_questions})


# paginates questions, with optional filters.
def question_list(request, page_number, **kwargs):
    # note: django does lazy query fetching so it does not
    # *actually* fetch all just yet.
    questions = Question.objects.select_related(
    ).order_by('-date_posted').all()

    # page these questions
    paginator = Paginator(questions, 10)
    if page_number == '':
        page_number = 1
    try:
        q_list = paginator.page(page_number)
    except PageNotAnInteger:
        q_list = paginator.page(1)
    except EmptyPage:
        q_list = paginator.page(paginator.num_pages)
    return render(request,
                  'forum/question/question_list.html',
                  {'questions': q_list}
                  )


# displays a question and its respective answers given a question id.
def question_detail(request, slug):
    question = get_object_or_404(Question, slug=slug)
    # get all answers for the question and order them by respective vote score.
    answers = Answer.objects.extra(
        select={'votesum':
                'forum_votable.upvotes - forum_votable.downvotes'},
        order_by=('-votesum',)
    ).select_related().filter(question=question)

    request.session['current_question'] = question.id

    if request.user.is_authenticated():
        # filter things that user has voted on, use Q to build the query.
        vote_filter = Q(object_id=question.id)
        vote_filter = (vote_filter) & Q(user=request.user)
        for answer in answers:
            vote_filter = vote_filter | Q(object_id=answer.id)
        user_votes = Vote.objects.filter(vote_filter).all()

        # send the template something that it can index into without
        # making voting objects
        object_vote_ids = [v.content_type.model + str(v.object_id) + v.direction
                           for v in user_votes]
    else:
        object_vote_ids = None

    form = SubmitAnswerForm()
    return render(request, 'forum/question/question_detail.html',
                  {'question': question,
                   'answers': answers,
                   'form': form,
                   'votes': object_vote_ids})


# does a string represent an integer?
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def validate_vote_request(objid, direction):
    return (direction == 'up' or direction == 'down') and is_int(objid)


def json_error(msg):
    json_error = {'success': False, 'reason': msg}
    return HttpResponse(json.dumps(json_error))


def json_success(msg):
    json_success = {'success': True, 'message': msg}
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
        if not validate_vote_request(object_id, direction):
            return json_error("invalid_vote")

        obj = None

        # handle a vote on a question
        if object_type == 'question':
            try:
                obj = Question.objects.get(id=int(object_id))
            except Question.DoesNotExist:
                return json_error("object_does_not_exist")

        # handle a vote on an answer
        elif object_type == 'answer':
            try:
                obj = Answer.objects.get(id=int(object_id))
            except Answer.DoesNotExist:
                return json_error("object_does_not_exist")

        # invalid object
        else:
            return json_error("invalid_vote")

        # vote on the object
        try:
            request.user.vote_on_object(obj, direction)
            return json_success("vote_handled")
        except User.CannotVote:
            return json_error("user_cannot_vote")
        except User.AlreadyVoted:
            return json_error("user_already_voted")

    else:
        return HttpResponse("not a post")


@login_required
def handle_answer(request):
    """handle an answer to a question"""
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
                        return render(request, "error.html",
                                      {'error':
                                       'Nonmatching question and session id'}
                                      )
                except KeyError:
                    return render(request, "error.html",
                                  {'error': 'Session trouble'}
                                  )

                question = Question.objects.get(id=qid)
                answer = Answer()
                answer.question = question
                answer.body_markdown = answer_body
                answer.author = request.user
                answer.save()
                return HttpResponseRedirect(reverse('question_detail',
                                                    kwargs={'slug': question.slug})
                                            )
            except Question.DoesNotExist:
                return render(request, "error.html",
                              {'error': 'Question does not exist'}
                              )
        else:
            return render(request, "error.html", {'error': 'Invalid form post'})


@login_required
def new_question(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.body_markdown = form.cleaned_data['body_text']
            question.question_text = form.cleaned_data['question_text']
            question.author = request.user
            question.save()

            tags = form.cleaned_data['tagslist'].split(",")
            for tag in tags:
                tag_name = slugify(tag)
                tag_object, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag_object)

            question.save()
            return HttpResponseRedirect(reverse('question_detail', kwargs={'slug': question.slug}))
    else:
        form = NewQuestionForm()

    tags = Tag.objects.all()
    return render(request, "forum/question/new_question.html", {'form': form, 'tags': tags})


def validate_edit_request(objid, objtype, body_text):
    return is_int(objid) and (objtype != "") and (body_text != "")


def get_edit_object(object_id, object_type):
    # they are editing a forum post
    if object_type == "post":
        try:
            return Post.objects.get(id=int(object_id))
        except Post.DoesNotExist:
            return None

    # they are editing a question
    elif object_type == "question":
        try:
            return Question.objects.get(id=int(object_id))
        except Question.DoesNotExist:
            return None

    # they are editing a question answer
    elif object_type == "answer":
        try:
            return Answer.objects.get(id=int(object_id))
        except Answer.DoesNotExist:
            return None

    # they are h4x0r
    else:
        return None

@login_required
def handle_edit(request):
    """ handle an AJAX edit for post, question, or answer."""

    # they are requesting an edit, send text to edit.
    if request.method == "GET":
       object_id = object_type = None

       try:
           object_id = request.GET['objid']
           object_type = request.GET['objtype']
       except KeyError:
           return json_error("invalid_request")

       # validate their request
       if not is_int(object_id) or (object_type == ""):
           return json_error("invalid_request")

       obj = get_edit_object(object_id, object_type)

       if obj is None:
           return json_error("object_does_not_exist")

       if obj.author != request.user:
           return json_error("not_author")

       return json_success(obj.body_markdown)


    # they are submitting an edit
    if request.method == "POST":
        if not request.is_ajax():
            return json_error("invalid_request")

        #parse what object they're modifying.
        object_id = object_type = body_text = None

        try:
            object_id = request.POST['objid']
            object_type = request.POST['objtype']
            body_text = request.POST['body_text']
        except KeyError:
            return json_error("invalid_request")

       # make sure the request is valid
        if not validate_edit_request(object_id, object_type, body_text):
            return json_error("invalid_request")

        obj = get_edit_object(object_id, object_type)

        if obj is None:
            return json_error("object_does_not_exist")

        if obj.author != request.user:
            return json_error("not_author")

        # apply edit
        try:
            obj.body_markdown = body_text
            obj.save()
            return json_success(obj.body_html)
        except:
            json_error("save_error")

def board_list(request):
    """Lists discussion boards."""
    boards = DiscussionBoard.objects.all()
    return render(request,"forum/discussion/board_list.html",{"boards":boards})


def thread_list(request, page_number, **kwargs):
    """Lists discussion threads, with optional board filter."""

    threads = Thread.objects.select_related('author','icon').order_by(
            '-date_posted').all()
    filtered = None

    if 'board_slug' in kwargs:
        board = get_object_or_404(Board,slug=kwargs['board_slug'])
        threads = get_list_or_404(threads.filter(board=board))
        filtered = board.name

    if filtered is None:
        boards = Board.objects.all()
    else:
        boards = None

    # page these threads
    paginator = Paginator(threads, 10)
    if page_number == '':
        page_number = 1
    try:
        thread_list = paginator.page(page_number)
    except PageNotAnInteger:
        thread_list = paginator.page(1)
    except EmptyPage:
        thread_list = paginator.page(paginator.num_pages)
    return render(request,
                  'forum/discussion/thread_list.html',
                  {'threads': thread_list,'filtered':filtered, 'boards':boards}
                  )

def thread_detail(request, page_number, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug)
    replies = Post.objects.filter(thread=thread).select_related()

    # page these replies
    # TODO: paging breaks the tree structure for some reason.
    #paginator = Paginator(replies, 10)
    #if page_number == '':
    #    page_number = 1
    #try:
    #    replies_list = paginator.page(page_number)
    #except PageNotAnInteger:
    #    replies_list = paginator.page(1)
    #except EmptyPage:
    #    replies_list = paginator.page(paginator.num_pages)

    return render(request, "forum/discussion/thread_detail.html",
                  {"thread": thread, "replies": replies}
                  )

@login_required
def new_thread(request,board_slug):
    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            thread = Thread()
            thread.subject = form.cleaned_data['thread_subject']
            thread.board = Board.objects.get(
                    id = form.cleaned_data['board_id']
                    )
            thread.author = request.user
            icon_id = form.cleaned_data['thread_icon']
            thread.icon = ThreadIcon.objects.get(id=icon_id)
            thread.save()

            post = Post()
            post.thread = thread
            post.body_markdown = form.cleaned_data['body_text']
            post.subject = form.cleaned_data['thread_subject']
            post.author = request.user
            post.save()

            post.save()
            return HttpResponseRedirect(reverse('thread_detail', 
                    kwargs={'thread_slug': thread.slug,'page_number':1}
                    ))
    else:
        board = get_object_or_404(Board,slug=board_slug)
        icons = ThreadIcon.objects.all()
        form = NewThreadForm()

    return render(request, "forum/discussion/new_thread.html",
            {'form': form,'board':board,'icons':icons}
            )

@login_required
def handle_reply(request):
    """Handle a reply to a post"""
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            parent = Post.objects.get(id=form.cleaned_data['reply_to'])
            post = Post()
            post.parent = parent
            post.thread = parent.thread
            post.author = request.user
            post.body_markdown = form.cleaned_data['body_text']
            post.save()

            return json_success(post.body_html)
        else:
            return json_error("invalid_request")

