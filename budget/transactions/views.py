from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from budget.transactions.models import Transaction
from budget.transactions.forms import TransactionForm


def transaction_list(request, model_class=Transaction, template_name='budget/transactions/list.html'):
    """
    A list of transaction objects.

    Templates: ``budget/transactions/list.html``
    Context:
        transactions
            paginated list of transaction objects
        paginator
            A Django Paginator instance
        page
            current page of transaction objects
    """
    transaction_list = model_class.active.order_by('-date', '-created')
    try:
        paginator = Paginator(transaction_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        transactions = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    return render_to_response(template_name, {
        'transactions': transactions,
        'paginator': paginator,
        'page': page,
    }, context_instance=RequestContext(request))


def transaction_add(request, form_class=TransactionForm, template_name='budget/transactions/add.html'):
    """
    Create a new transaction object.

    Templates: ``budget/transactions/add.html``
    Context:
        form
            a transaction form
    """
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            transaction = form.save()
            return HttpResponseRedirect(reverse('budget_transaction_list'))
    else:
        form = form_class()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


def transaction_edit(request, transaction_id, model_class=Transaction, form_class=TransactionForm, template_name='budget/transactions/edit.html'):
    """
    Edit a transaction object.

    Templates: ``budget/transactions/edit.html``
    Context:
        transaction
            the existing transaction object
        form
            a transaction form
    """
    transaction = get_object_or_404(model_class.active.all(), pk=transaction_id)
    if request.POST:
        form = form_class(request.POST, instance=transaction)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_transaction_list'))
    else:
        form = form_class(instance=transaction)
    return render_to_response(template_name, {
        'transaction': transaction,
        'form': form,
    }, context_instance=RequestContext(request))


def transaction_delete(request, transaction_id, model_class=Transaction, template_name='budget/transactions/delete.html'):
    """
    Delete a transaction object.

    Templates: ``budget/transactions/delete.html``
    Context:
        transaction
            the existing transaction object
    """
    transaction = get_object_or_404(Transaction.active.all(), pk=transaction_id)
    if request.POST:
        if request.POST.get('confirmed'):
            transaction.delete()
        return HttpResponseRedirect(reverse('budget_transaction_list'))
    return render_to_response(template_name, {
        'transaction': transaction,
    }, context_instance=RequestContext(request))
