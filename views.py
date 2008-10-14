from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from budget.models import Budget, BudgetEstimate
from budget.categories.models import Category
from budget.transactions.models import Transaction
from budget.forms import BudgetEstimateForm, BudgetForm

def dashboard(request):
    return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))

def year_summary(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def month_summary(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def budget_list(request):
    budgets = Budget.objects.filter(is_deleted=False)
    return render_to_response('budget/budgets/list.html', {
        'budgets': budgets,
    }, context_instance=RequestContext(request))

def budget_add(request):
    if request.POST:
        form = BudgetForm(request.POST)
        
        if form.is_valid():
            budget = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = BudgetForm()
    return render_to_response('budget/budgets/add.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def budget_edit(request, slug):
    budget = get_object_or_404(Budget, slug=slug, is_deleted=False)
    if request.POST:
        form = BudgetForm(request.POST, instance=budget)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = BudgetForm(instance=budget)
    return render_to_response('budget/budgets/edit.html', {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))

def budget_delete(request, slug):
    budget = get_object_or_404(Budget, slug=slug, is_deleted=False)
    if request.POST:
        if request.POST.get('confirmed'):
            budget.delete()
        return HttpResponseRedirect(reverse('budget_budget_list'))
    return render_to_response('budget/budgets/delete.html', {
        'budget': budget,
    }, context_instance=RequestContext(request))

def estimate_list(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug, is_deleted=False)
    estimates = BudgetEstimate.objects.filter(is_deleted=False)
    return render_to_response('budget/estimates/list.html', {
        'budget': budget,
        'estimates': estimates,
    }, context_instance=RequestContext(request))

def estimate_add(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug, is_deleted=False)
    if request.POST:
        form = BudgetEstimateForm(request.POST)
        
        if form.is_valid():
            estimate = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = BudgetEstimateForm()
    return render_to_response('budget/estimates/add.html', {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))

def estimate_edit(request, budget_slug, estimate_id):
    budget = get_object_or_404(Budget, slug=budget_slug, is_deleted=False)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        form = BudgetEstimateForm(request.POST, instance=estimate)
        
        if form.is_valid():
            category = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = BudgetEstimateForm(instance=estimate)
    return render_to_response('budget/estimates/edit.html', {
        'budget': budget,
        'estimate': estimate,
        'form': form,
    }, context_instance=RequestContext(request))

def estimate_delete(request, budget_slug, estimate_id):
    budget = get_object_or_404(Budget, slug=budget_slug, is_deleted=False)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        if request.POST.get('confirmed'):
            estimate.delete()
        return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    return render_to_response('budget/estimates/delete.html', {
        'budget': budget,
        'estimate': estimate,
    }, context_instance=RequestContext(request))
