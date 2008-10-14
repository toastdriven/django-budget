from django.conf.urls.defaults import *

urlpatterns = patterns('budget.categories.views',
    url(r'^$', 'category_list', name='budget_category_list'),
    url(r'^add/$', 'category_add', name='budget_category_add'),
    url(r'^edit/(?P<slug>)\w+/$', 'category_edit', name='budget_category_edit'),
    url(r'^delete/(?P<slug>)\w+/$', 'category_delete', name='budget_category_delete'),
)
