from __future__ import unicode_literals

from django.db import models
import requests
import bs4
from random import randint
# Create your models here.

class WikiGame(models.Model):
    playername = models.CharField(max_length=30)
    goal_name = models.CharField(max_length=400)
    current_name = models.CharField(max_length=400)
    won = models.BooleanField(default=False)

    potential_goals = {
        'Easy': ['Rome', 'World War II', 'Adolf Hitler'],
        'Medium': ['Barack Obama', 'Fiji'],
        'Hard': ['NBA', 'Kareem Abdul Jabbar'],
    }
    @property
    def goal(self):
        return WikiPage(self.goal_name)

    @property
    def current(self):
        return WikiPage(self.current_name)

    # method that gets path
    def get_path(self):
        raw_steps = list(WikiPathStep.objects.all().filter(game=self))
        raw_steps.sort(key=lambda x: x.id_in_path)
        return raw_steps

    def add_page(self, page_name):
        page = WikiPage(page_name)
        if page == self.goal:
            self.won = True

        next_idx = len(self.get_path())
        self.current_name = page_name
        new_step = WikiPathStep(id_in_path=next_idx, page_name=self.current_name, game=self)
        self.save()
        new_step.save()
        print "bloop"
        return new_step

    def get_ten(self):
        links = WikiPage(self.current_name).get_filtered_links()
        ten_list = []
        paths = min(10, len(links))
        for i in xrange(0, paths):
            rand = randint(0, len(links) - 1)
            ten_list.append(links.pop(rand))
        if self.goal_name in links:
            rand = randint(0, len(ten_list) - 1)
            ten_list[rand] = self.goal_name
        return ten_list

    @classmethod
    def get_a_goal(cls, difficulty):
        try:
            goals_in_diff = cls.potential_goals[difficulty]
        except:
            raise Exception('Difficulty %s does not exist' % difficulty)

        idx = randint(0, len(goals_in_diff) - 1)
        return goals_in_diff[idx]

    @classmethod
    def create(cls, playername, difficulty, start_page):
        goal_page = cls.get_a_goal(difficulty)
        game = cls(playername=playername, goal_name=goal_page, current_name=start_page)
        game.add_page(start_page)
        game.add_page(start_page)
        return game
    '''
    def __init__(self, *args, **kwargs):
        """
        print (difficulty)
        print playername
        print start_page
        """
        super(WikiGame, self).__init__(*args, **kwargs)
        """self.playername = playername
        self.current_name = start_page
        self.goal_name = self.get_a_goal(difficulty)
        # for some reason the first add page doesn't register so we getting it out of the way
        self.add_page(start_page)
        self.add_page(start_page)"""
    '''

class WikiPage(object):

    baseUrl = 'https://en.wikipedia.org/wiki/';
    badLinks = (':', 'wikipedia', 'Wikipedia', 'wikimedia', 'Main_Page', 'wiksource', 'wiktionary')

    def get_soup(self):
        text = requests.get(self.baseUrl + self.url).text
        return bs4.BeautifulSoup(text, "html.parser")

    def get_filtered_links(self):
        soup = self.get_soup()
        raw_hrefs = [a.get('href') for a in soup.select('#bodyContent a')]
        filtered_hrefs = filter(self.link_filter, raw_hrefs)
        pages = [link.split('/')[-1].replace('_', ' ').replace('%E2%80%93', '-') for link in filtered_hrefs]
        return list(set(pages))

    def link_filter(self, href):
        if href is None:
            return False
        for s in self.badLinks:
            if s in href:
                return False
        return '/wiki/' in href

    def __init__(self, name):
        self.name = name

    @property
    def url(self):
        return self.name.replace(' ', '_')

    def __eq__(self, other):
        return self.name == other.name

class WikiPathStep(models.Model):
    id_in_path = models.IntegerField()
    page_name = models.CharField(max_length=500)
    game = models.ForeignKey(WikiGame, blank=True, null=True)

    @property
    def page(self):
        return WikiPage(self.page_name)

    def __str__(self):
        return self.page_name + ": " +  str(self.id_in_path)
