import datetime
from django import forms
from django.template.defaultfilters import slugify
from budget.models import Budget, BudgetEstimate


class BudgetForm(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.datetime.now, required=False, widget=forms.SplitDateTimeWidget)
    
    class Meta:
        model = Budget
        fields = ('name', 'start_date')
    
    def save(self):
        if not self.instance.slug:
            self.instance.slug = slugify(self.cleaned_data['name'])
        super(BudgetForm, self).save()


class BudgetEstimateForm(forms.ModelForm):
    class Meta:
        model = BudgetEstimate
        fields = ('category', 'amount')
    
    def save(self, budget):
        self.instance.budget = budget
        super(BudgetEstimateForm, self).save()
