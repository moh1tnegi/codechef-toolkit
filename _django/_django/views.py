# from django.views import generic
# from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.core.paginator import PageNotAnInteger, InvalidPage
import logging
from .models import User


# LOG_FORMAT = "%()s"
logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()
logger.debug("# logging starts")

top_rated = User.objects.all().order_by('-ratings')
cities = []
states = []
ins = []
counter = 1
for info in top_rated:
    cities.append(str(counter)+'. '+info.city)
    states.append(str(counter)+'. '+info.state)
    ins.append(str(counter)+'. '+info.inst)
    counter += 1


def index(request):
    context = {'cities': cities[:10], 'states': states[:10],
               'instit': ins[:10]}
    return render(request, 'codechef/index.html', context)


def search(request):
    if request.method == 'GET':
        srh = request.GET['srch']
        if srh:
            try:
                match = User.objects.get(Q(username__exact=srh))
                return render(request, 'codechef/search.html', {'sr': match})
            except ObjectDoesNotExist:
                messages.error(request, 'No results!')
        else:
            return HttpResponseRedirect('codechef/index.html')
    return render(request, 'codechef/search.html', {'sr': 0})


def get_details(request, toppers):
    paginator = Paginator(toppers, 10)
    page = request.GET.get('page')
    try:
        top_paged = paginator.get_page(page)
    except PageNotAnInteger:
        top_paged = paginator.get_page(1)
    except (EmptyPage, InvalidPage):
        top_paged = paginator.get_page(paginator.num_pages)
    yield paginator
    yield top_paged


def pagination_problem(paged, paginated):
    indx = paginated.number-1
    mx_indx = len(paged.page_range)
    logger.debug(indx)
    start = indx - 3 if indx >= 3 else 0
    end = indx + 3 if indx <= mx_indx-3 else mx_indx
    page_range = list(paged.page_range)[start:end]
    return page_range


def city_details(request):
    city_paginator, city_paged = get_details(request, cities)
    page_range = pagination_problem(city_paginator, city_paged)
    return render(request, 'codechef/details.html', {'cit': city_paged, 'page_range': page_range})


def state_details(request):
    stat_paginator, state_paged = get_details(request, states)
    page_range = pagination_problem(stat_paginator, state_paged)
    return render(request, 'codechef/details.html', {'stat': state_paged, 'page_range': page_range})


def inst_details(request):
    inst_paginator, inst_paged = get_details(request, ins)
    page_range = pagination_problem(inst_paginator, inst_paged)
    return render(request, 'codechef/details.html', {'inst': inst_paged, 'page_range': page_range})
