from django.contrib import admin
from budget.transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('transaction_type', 'notes', 'category', 'amount', 'date'),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated', 'is_deleted')
        })
    )
    list_display = ('notes', 'transaction_type', 'amount', 'date', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('notes',)


admin.site.register(Transaction, TransactionAdmin)
