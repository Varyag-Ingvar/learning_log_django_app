from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required  # add decorator "login_required"
from django.http import Http404


def index(request):
    """learning_log app homepage"""
    return render(request, 'learning_logs/index.html')


@login_required  # it means that only authorized users can do, whatever function does; or redirect user to login page.
def topics(request):
    """Display list of topics"""
    # 'owner=request.user' means that only user, who created topics, can see it. Otherwise, user will see empty page.
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Display topic and all entries in it"""
    topic = Topic.objects.get(id=topic_id)
    # check that topic was added with current user, if not - raises an error 'page not found'
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Create a new topic"""
    if request.method != 'POST':
        # data did not sent; creating a new form
        form = TopicForm()
    else:
        # POST data sent; processing data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # show empty or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Create a new entry in the specific topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # data did not sent; creating a new form
        form = EntryForm()
    else:
        # POST data sent; processing data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # show empty or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Editing an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # check that entry was added with current user, if not - raises an error 'page not found'
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # sending POST data; processing data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


