from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import WikiPathStep
from .models import WikiGame
import operator
from .forms import StartForm

# Create your views here.
def index(request):
    print 'yo'
    games = WikiGame.objects.all()
    form = StartForm()
    context = {'games': games,
                'form': form}
    return render(request, 'index.html', context)

def go(request):
    print 'yo'
    if request.method == "POST":
        form = StartForm(request.POST)
        if form.is_valid():
            print 'it valid'
            difficulty = request.POST.__getitem__('difficulty')
            name = request.POST.__getitem__('name')
            starting_page = request.POST.__getitem__('starting_page')
            game = WikiGame.create(name, difficulty, starting_page)
            game.save()
            return HttpResponseRedirect('/' + str(game.pk) + '/')
        else:
            print 'form wasnt valid'
            form = StartForm()
            games = WikiGame.objects.all()
            context = {'form': form,
                        'games': games,
                        'alert': True}
            return render(request, 'index.html', context)
    return HttpResponseRedirect('/')

def step(request, game_id):
    game = WikiGame.objects.get(pk=game_id)
    print request.method
    print 'hey!'
    if request.method=="POST":
        page_name = request.POST['page_name']
        page_name = page_name.replace('_', ' ')
        game.add_page(page_name)
        if game.won is not True:
            pages = game.get_ten()
            both = {}
            for page in pages:
                both[page] = page.replace(' ', '_')
            context = {'game': game,
                    'pages': both}
            return render(request, 'go.html', context)
        else:
            context = {'game': game}
            return render(request, 'go.html', context)
    else:
        pages = game.get_ten()
        both = {}
        for page in pages:
            both[page] = page.replace(' ', '_')
        context = {'game': game,
                    'pages': both}
        return render(request, 'go.html', context)

def stat(request):
    games = WikiGame.objects.all()
    pages = WikiPathStep.objects.all()
    maxx = 0
    max_game = None
    for game in games:
        steps = len(game.get_path())
        if steps > maxx:
            maxx = steps
            max_game = game
    page_visits = {}
    for page in pages:
        if page.page_name in page_visits:
            page_visits[page.page_name] = page_visits[page.page_name] + 1
        else:
            page_visits[page.page_name] = 1
    page_sort = sorted(page_visits.items(), key=operator.itemgetter(1), reverse=True)
    if len(page_sort) >= 11:
        del page_sort[-(len(page_sort) - 10):]
    context = {'max': max_game,
                'visits': page_sort,
                }
    return render(request, 'stat.html', context)
