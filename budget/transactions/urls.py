from django.conf.urls.defaults import *

urlpatterns = patterns('budget.transactions.views',
    url(r'^$', 'transaction_list', name='budget_transaction_list'),
    url(r'^add/$', 'transaction_add', name='budget_transaction_add'),
    url(r'^edit/(?P<transaction_id>\d+)/$', 'transaction_edit', name='budget_transaction_edit'),
    url(r'^delete/(?P<transaction_id>\d+)/$', 'transaction_delete', name='budget_transaction_delete'),
)
