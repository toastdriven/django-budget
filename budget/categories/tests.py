"""
>>> from django.test import Client
>>> c = Client()

>>> r = c.get('/budget/category/')
>>> r.status_code # /budget/category/
200
>>> r.context[-1]['categories']
[]

>>> r = c.get('/budget/category/add/')
>>> r.status_code # /budget/category/add/
200
>>> type(r.context[-1]['form'])
<class 'budget.categories.forms.CategoryForm'>

>>> r = c.post('/budget/category/add/', {'name': 'Mortgage'})
>>> r.status_code # /budget/category/add/
302
>>> r['Location']
'http://testserver/budget/category/'

>>> r = c.get('/budget/category/')
>>> r.status_code # /budget/category/
200
>>> r.context[-1]['categories']
[<Category: Mortgage>]

>>> r = c.get('/budget/category/edit/mortgage/')
>>> r.status_code # /budget/category/edit/mortgage/
200
>>> type(r.context[-1]['form'])
<class 'budget.categories.forms.CategoryForm'>
>>> r.context[-1]['category']
<Category: Mortgage>

>>> r = c.post('/budget/category/edit/mortgage/', {'name': 'First Mortgage'})
>>> r.status_code # /budget/category/edit/mortgage/
302
>>> r['Location']
'http://testserver/budget/category/'

>>> r = c.get('/budget/category/')
>>> r.status_code # /budget/category/
200
>>> r.context[-1]['categories']
[<Category: First Mortgage>]

>>> r = c.get('/budget/category/delete/mortgage/')
>>> r.status_code # /budget/category/delete/mortgage/
200
>>> r.context[-1]['category']
<Category: First Mortgage>

>>> r = c.post('/budget/category/delete/mortgage/', {'confirmed': 'Yes'})
>>> r.status_code # /budget/category/delete/mortgage/
302
>>> r['Location']
'http://testserver/budget/category/'

>>> r = c.get('/budget/category/')
>>> r.status_code # /budget/category/
200
>>> r.context[-1]['categories']
[]
"""
