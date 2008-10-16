"""
>>> from django.test import Client
>>> c = Client()


# Budgets

>>> r = c.get('/budget/budget/')
>>> r.status_code # /budget/budget/
200
>>> r.context[-1]['budgets']
[]

>>> r = c.get('/budget/budget/add/')
>>> r.status_code # /budget/budget/add/
200
>>> type(r.context[-1]['form'])
<class 'budget.forms.BudgetForm'>

>>> r = c.post('/budget/budget/add/', {'name': 'Our Budget', 'start_date': '2008-10-14'})
>>> r.status_code # /budget/budget/add/
302
>>> r['Location']
'http://testserver/budget/budget/'

>>> r = c.get('/budget/budget/')
>>> r.status_code # /budget/budget/
200
>>> r.context[-1]['budgets']
[<Budget: Our Budget>]

>>> r = c.get('/budget/budget/edit/our-budget/')
>>> r.status_code # /budget/budget/edit/our-budget/
200
>>> type(r.context[-1]['form'])
<class 'budget.forms.BudgetForm'>
>>> r.context[-1]['budget']
<Budget: Our Budget>

>>> r = c.post('/budget/budget/edit/our-budget/', {'name': 'Our Family Budget', 'start_date': '2008-10-14'})
>>> r.status_code # /budget/budget/edit/our-budget/
302
>>> r['Location']
'http://testserver/budget/budget/'

>>> r = c.get('/budget/budget/')
>>> r.status_code # /budget/budget/
200
>>> r.context[-1]['budgets']
[<Budget: Our Family Budget>]

>>> r = c.get('/budget/budget/delete/our-budget/')
>>> r.status_code # /budget/budget/delete/our-budget/
200
>>> r.context[-1]['budget']
<Budget: Our Family Budget>

>>> r = c.post('/budget/budget/delete/our-budget/', {'confirmed': 'Yes'})
>>> r.status_code # /budget/budget/delete/our-budget/
302
>>> r['Location']
'http://testserver/budget/budget/'

>>> r = c.get('/budget/budget/')
>>> r.status_code # /budget/budget/
200
>>> r.context[-1]['budgets']
[]


# Budget Estimates

# Setup
>>> from budget.models import Budget
>>> budget = Budget.objects.create(name='Test Budget', slug='test-budget', start_date='2008-10-14')

>>> from django.core.management import call_command
>>> call_command('loaddata', 'categories_testdata.yaml') #doctest: +ELLIPSIS
Installing yaml fixture 'categories_testdata' from ...
Installed 1 object(s) from 1 fixture(s)

>>> from budget.categories.models import Category
>>> cat = Category.objects.get(slug='misc')

>>> r = c.get('/budget/budget/test-budget/estimate/')
>>> r.status_code # /budget/budget/test-budget/estimate/
200
>>> r.context[-1]['estimates']
[]

>>> r = c.get('/budget/budget/test-budget/estimate/add/')
>>> r.status_code # /budget/budget/test-budget/estimate/add/
200
>>> type(r.context[-1]['form'])
<class 'budget.forms.BudgetEstimateForm'>

>>> r = c.post('/budget/budget/test-budget/estimate/add/', {'budget': budget.id, 'category': cat.id, 'amount': '200.00'})
>>> r.status_code # /budget/budget/test-budget/estimate/add/
302
>>> r['Location']
'http://testserver/budget/budget/test-budget/estimate/'

>>> r = c.get('/budget/budget/test-budget/estimate/')
>>> r.status_code # /budget/budget/test-budget/estimate/
200
>>> r.context[-1]['estimates']
[<BudgetEstimate: Misc - 200>]

>>> r = c.get('/budget/budget/test-budget/estimate/edit/1/')
>>> r.status_code # /budget/budget/test-budget/estimate/edit/1/
200
>>> type(r.context[-1]['form'])
<class 'budget.forms.BudgetEstimateForm'>
>>> r.context[-1]['estimate']
<BudgetEstimate: Misc - 200>

>>> r = c.post('/budget/budget/test-budget/estimate/edit/1/', {'budget': budget.id, 'category': cat.id, 'amount': '250.00'})
>>> r.status_code # /budget/budget/test-budget/estimate/edit/1/
302
>>> r['Location']
'http://testserver/budget/budget/test-budget/estimate/'

>>> r = c.get('/budget/budget/test-budget/estimate/')
>>> r.status_code # /budget/budget/test-budget/estimate/
200
>>> r.context[-1]['estimates']
[<BudgetEstimate: Misc - 250>]

>>> r = c.get('/budget/budget/test-budget/estimate/delete/1/')
>>> r.status_code # /budget/budget/test-budget/estimate/delete/1/
200
>>> r.context[-1]['estimate']
<BudgetEstimate: Misc - 250>

>>> r = c.post('/budget/budget/test-budget/estimate/delete/1/', {'confirmed': 'Yes'})
>>> r.status_code # /budget/budget/test-budget/estimate/delete/1/
302
>>> r['Location']
'http://testserver/budget/budget/test-budget/estimate/'

>>> r = c.get('/budget/budget/test-budget/estimate/')
>>> r.status_code # /budget/budget/test-budget/estimate/
200
>>> r.context[-1]['estimates']
[]


# Summaries

>>> r = c.get('/budget/summary/2008/')
>>> r.status_code # /budget/summary/2008/
200
>>> r.context[-1]['budget']
<Budget: Test Budget>

>>> r = c.get('/budget/summary/2008/10/')
>>> r.status_code # /budget/summary/2008/10/
200
>>> r.context[-1]['budget']
<Budget: Test Budget>


# Dashboard

>>> r = c.get('/budget/')
>>> r.status_code # /budget/
200
>>> r.context[-1]['budget']
<Budget: Test Budget>
>>> r.context[-1]['latest_debits']
[]
>>> r.context[-1]['latest_credits']
[]
>>> r.context[-1]['estimated_amount']
Decimal("250.0")
>>> r.context[-1]['amount_used']
Decimal("0.0")
>>> r.context[-1]['progress_bar_percent']
0
>>> r.context[-1]['progress_bar_level']
'green'
"""
