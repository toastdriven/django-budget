from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from budget.categories.models import Category
from budget.categories.forms import CategoryForm

def category_list(request):
    categories = Category.objects.filter(is_deleted=False)
    return render_to_response('budget/categories/list.html', {
        'categories': categories,
    }, context_instance=RequestContext(request))

def category_add(request):
    if request.POST:
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_category_list'))
    else:
        form = CategoryForm()
    return render_to_response('budget/categories/add.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug, is_deleted=False)
    if request.POST:
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_category_list'))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('budget/categories/edit.html', {
        'category': category,
        'form': form,
    }, context_instance=RequestContext(request))

def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug, is_deleted=False)
    if request.POST:
        if request.POST.get('confirmed') and request.POST['confirmed'] == 'Yes':
            category.delete()
        return HttpResponseRedirect(reverse('budget_category_list'))
    return render_to_response('budget/categories/delete.html', {
        'category': category,
    }, context_instance=RequestContext(request))
