from django.shortcuts import render_to_response, get_object_or_404
from budget.categories.models import Category

def category_list(request):
    return render_to_response('.html', {})

def category_add(request):
    return render_to_response('.html', {})

def category_edit(request):
    return render_to_response('.html', {})

def category_delete(request):
    return render_to_response('.html', {})
