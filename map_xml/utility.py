from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.urls import reverse
from django.utils.html import strip_tags


class NewsSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return News.objects.get_active_news()


class CategorySitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Category.objects.get_active_category()


class TagsSitemap(sitemaps.Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        all_active_article = News.objects.get_active_news()
        tag_list = []
        for item in all_active_article:
            for j in item.get_tags():
                if j != "":
                    tag_list.append(j)
        return list(set(tag_list))

    def location(self, item):
        return f"/news/lits?search={strip_tags(item)}"


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return [
            'Home:Home', 'ContactUs:send_message', 'AboutUs:about_us', 'account:login', 'account:register',
        ]

    def location(self, item):
        return reverse(item)


# ##############################################################
SiteMaps = {}


def add_to_sitemaps(key, value, flag=0):
    # add
    if flag == 0:
        SiteMaps[key] = value
    # update
    else:
        SiteMaps.update({key: value})

#
# add_to_sitemaps('NewsSitemap', NewsSitemap)
# add_to_sitemaps('CategorySitemap', CategorySitemap)
# add_to_sitemaps('TagsSitemap', TagsSitemap)
# add_to_sitemaps('StaticViewSitemap', StaticViewSitemap)
