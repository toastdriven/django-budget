from django import forms
from budget.transactions.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'name', 'category', 'amount', 'date')
