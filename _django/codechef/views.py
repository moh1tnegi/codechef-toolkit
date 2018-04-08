# from django.views import generic
# from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.core.paginator import PageNotAnInteger, InvalidPage
from .models import User
import logging


# LOG_FORMAT = "%()s"
logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()
logger.debug("# logging start")

top_rated = User.objects.all().order_by('-ratings')
cities = []
states = []
ins = []

city_counter = 1
stat_counter = 1
inst_counter = 1

for info in top_rated:
    if info.city != 'NULL':
        cities.append(str(city_counter)+'. '+info.city)
        city_counter += 1

    if info.state != 'NULL':
        states.append(str(stat_counter)+'. '+info.state)
        stat_counter += 1

    if info.inst != 'NULL':
        ins.append(str(inst_counter)+'. '+info.inst)
        inst_counter += 1


def index(request):
    context = {'cities': cities[:10], 'states': states[:10],
               'instit': ins[:10]}
    return render(request, 'codechef/index.html', context)


def get_details(request, toppers):
    paginator = Paginator(toppers, 10)
    page = request.GET.get('page', 1)

    try:
        top_paged = paginator.get_page(page)
    except PageNotAnInteger:
        top_paged = paginator.get_page(1)
    except (EmptyPage, InvalidPage):
        top_paged = paginator.get_page(paginator.num_pages)

    yield paginator
    yield top_paged


def get_page_range(paged, paginated):
    indx = paginated.number-1
    mx_indx = len(paged.page_range)

    start = indx - 3 if indx >= 3 else 0
    end = indx + 3 if indx <= mx_indx-3 else mx_indx

    return list(paged.page_range)[start:end]


def search(request):
    if request.method == 'GET':
        srh = request.GET['srch']
        select_input = request.GET['query']
        requested_for = 'Usernames from ' + srh

        if select_input in 'City':
            match = User.objects.all().filter(city__exact=srh).order_by('-ratings')
        elif select_input in 'State':
            match = User.objects.all().filter(state__exact=srh).order_by('-ratings')
        elif select_input in 'Institution':
            match = User.objects.all().filter(inst__exact=srh).order_by('-ratings')
        if select_input not in 'Username':
            details_paginator, paged = get_details(request, match)
            page_range = get_page_range(details_paginator, paged)
            return render(request, 'codechef/details.html',
                            {'detail': paged, 'page_range': page_range,
                            'requested_for': requested_for})
        if srh:
            try:
                match = User.objects.get(Q(username__exact=srh))
                return render(request, 'codechef/search.html', {'sr': match})
            except ObjectDoesNotExist:
                error_message = "No results found for "+srh+'. '+"""Try 
                    checking for mispelled words. The user might be banned
                    or not registered."""
                messages.error(request, error_message)
        else:
            return HttpResponseRedirect('codechef/index.html')

    return render(request, 'codechef/search.html', {'sr': 0})


def top_details(request):
    requested_content = request.path_info

    if requested_content == '/city-details/':
        requested_content = cities
        requested_for = 'Cities'
    elif requested_content == '/state-details/':
        requested_content = states
        requested_for = 'States'
    else:
        requested_content = ins
        requested_for = 'Institution'

    details_paginator, paged = get_details(request, requested_content)
    page_range = get_page_range(details_paginator, paged)

    return render(request, 'codechef/details.html',
                  {'detail': paged, 'page_range': page_range,
                   'requested_for': requested_for})
