from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404


from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.

def index(request):
    return render(request, 'l_i/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'l_i/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'l_i/topic.html', context)

@login_required
def new_topic(request):
    """"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('l_i:topics'))

    context = {'form':form}
    return render(request, 'l_i/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('l_i:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'l_i/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.owner != request.owner:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('l_i:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'l_i/edit_entry.html', context)