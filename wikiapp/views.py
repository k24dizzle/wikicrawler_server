from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import WikiPathStep
from .models import WikiGame

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
    print request.path
    if request.method == "POST":
        form = StartForm(request.POST)
        if form.is_valid():
            print 'it valid'
            difficulty = request.POST.__getitem__('difficulty')
            name = request.POST.__getitem__('name')
            starting_page = request.POST.__getitem__('starting_page')
            game = WikiGame.create(name, difficulty, starting_page)
            game.save()
            pages = game.get_ten()
        else:
            print 'form wasnt valid'
            return render(request, 'index.html')
    both = {}
    for page in pages:
        both[page] = page.replace(' ', '_')
    context = {'pages': both,
               'game': game}
    return render(request, 'go.html', context)

def step(request, game_id, page_name):
    game = WikiGame.objects.get(pk=game_id)
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
        return HttpResponseRedirect('/win/' + game_id)

def win(request, game_id):
    context = {'game': WikiGame.objects.get(pk=game_id)}
    return render(request, 'win.html', context)
