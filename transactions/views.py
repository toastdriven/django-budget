from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from budget.transactions.models import Transaction
from budget.transactions.forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.active.all()
    return render_to_response('budget/transactions/list.html', {
        'transactions': transactions,
    }, context_instance=RequestContext(request))

def transaction_add(request):
    if request.POST:
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            transaction = form.save()
            return HttpResponseRedirect(reverse('budget_transaction_list'))
    else:
        form = TransactionForm()
    return render_to_response('budget/transactions/add.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def transaction_edit(request, transaction_id):
    transaction = get_object_or_404(Transaction.active.all(), pk=transaction_id)
    if request.POST:
        form = TransactionForm(request.POST, instance=transaction)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_transaction_list'))
    else:
        form = TransactionForm(instance=transaction)
    return render_to_response('budget/transactions/edit.html', {
        'transaction': transaction,
        'form': form,
    }, context_instance=RequestContext(request))

def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction.active.all(), pk=transaction_id)
    if request.POST:
        if request.POST.get('confirmed'):
            transaction.delete()
        return HttpResponseRedirect(reverse('budget_transaction_list'))
    return render_to_response('budget/transactions/delete.html', {
        'transaction': transaction,
    }, context_instance=RequestContext(request))
