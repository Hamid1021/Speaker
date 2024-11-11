import itertools

from django.http import JsonResponse
from django.shortcuts import render
from news.models import News
from application_manager.models import WebSiteSettings, FooterLink
from news.models import Category


def grouper(n, iterable, fill_value=None):
    args = [iter(iterable)] * n
    return list(itertools.zip_longest(*args, fillvalue=fill_value))


def header_ref(request):
    context = {

    }
    return render(request, "rtl/shared/base/header_ref.html", context)


def header(request):
    all_fast_news = News.objects.get_fast_news()
    context = {
        "all_fast_news": all_fast_news
    }
    return render(request, "rtl/shared/base/header.html", context)


def nav(request):
    settings: WebSiteSettings = WebSiteSettings.objects.get_first_active_or_create()
    all_cat_none_parent = Category.objects.get_active_category_no_parent()
    group_cat_4 = grouper(settings.col_count_of_categories, all_cat_none_parent)
    context = {
        'group_cat_4': group_cat_4,
        "header_logo": settings.header_logo,
        "footer_logo": settings.footer_logo,
    }
    return render(request, "rtl/shared/base/nav.html", context)


def footer(request):
    settings: WebSiteSettings = WebSiteSettings.objects.get_first_active_or_create()
    footer_link = FooterLink.objects.get_active_links()
    context = {
        "copy_write": settings.copy_write if settings.copy_write is not None else '',
        "logo": settings.footer_logo,
        "title": settings.title,
        "footer_text": settings.footer_text,
        "allows_subscribe": settings.is_subscribe_active,
        "footer_link": footer_link
    }
    return render(request, "rtl/shared/base/footer.html", context)


def footer_ref(request):
    context = {

    }
    return render(request, "rtl/shared/base/footer_ref.html", context)


def most_visit_news(request):
    most_visit: News = News.objects.get_most_visit_news(5)
    context = {
        "most_visit": most_visit,
    }
    return render(request, "rtl/shared/component/most_visit_news.html", context)


def last_created_news(request):
    last_news: News = News.objects.get_last_active_news(5)
    context = {
        "last_news": last_news,
    }
    return render(request, "rtl/shared/component/last_created_news.html", context)


def tags(request):
    last_tags: News = News.objects.get_last_tags(10)
    context = {
        "last_tags": last_tags,
    }
    return render(request, "rtl/shared/component/tags.html", context)


def about_sidebar(request):
    context = {

    }
    return render(request, "rtl/shared/component/about_sidebar.html", context)


def index_static_news(request):
    context = {}
    # تنظیمات ظاهری سایت
    settings: WebSiteSettings = WebSiteSettings.objects.get_first_active_or_create()
    # اخبار ثابت یا اخبار بر گزیده که باید 4 عدد باشد
    static_news = News.objects.get_static_news(settings.static_news_in_search_page)
    # context["len_static_news"] = len(static_news)
    # context["static_news"] = static_news
    try:context['static_1'] = static_news[0]
    except:pass
    try:context['static_2'] = static_news[1]
    except:pass
    try:context['static_3'] = static_news[2]
    except:pass
    try:context['static_4'] = static_news[3]
    except:pass

    return render(request, "rtl/shared/component/index_static_news.html", context)
