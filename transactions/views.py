from django.shortcuts import render_to_response, get_object_or_404
from budget.transactions.models import Transaction

def transaction_list(request):
    return render_to_response('.html', {})

def transaction_add(request):
    return render_to_response('.html', {})

def transaction_edit(request):
    return render_to_response('.html', {})

def transaction_delete(request):
    return render_to_response('.html', {})
