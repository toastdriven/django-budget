from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from budget.categories.models import Category
from budget.categories.forms import CategoryForm


def category_list(request, model_class=Category, template_name='budget/categories/list.html'):
    categories_list = model_class.active.all()
    try:
        paginator = Paginator(categories_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        categories = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    return render_to_response(template_name, {
        'categories': categories,
        'paginator': paginator,
        'page': page,
    }, context_instance=RequestContext(request))


def category_add(request, form_class=CategoryForm, template_name='budget/categories/add.html'):
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_category_list'))
    else:
        form = form_class()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


def category_edit(request, slug, model_class=Category, form_class=CategoryForm, template_name='budget/categories/edit.html'):
    category = get_object_or_404(model_class.active.all(), slug=slug)
    if request.POST:
        form = form_class(request.POST, instance=category)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_category_list'))
    else:
        form = form_class(instance=category)
    return render_to_response(template_name, {
        'category': category,
        'form': form,
    }, context_instance=RequestContext(request))


def category_delete(request, slug, model_class=Category, template_name='budget/categories/delete.html'):
    category = get_object_or_404(model_class.active.all(), slug=slug)
    if request.POST:
        if request.POST.get('confirmed') and request.POST['confirmed'] == 'Yes':
            category.delete()
        return HttpResponseRedirect(reverse('budget_category_list'))
    return render_to_response(template_name, {
        'category': category,
    }, context_instance=RequestContext(request))
