from django.contrib import admin
from .models import UserWallet, UserPlan

class UserWalletAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin
    list_display = ('user', 'balance', 'currency', 'created_at', 'updated_at')
    # Filters available in the admin
    list_filter = ('currency', 'user')
    # Fields to search in the admin
    search_fields = ('user__username', 'currency')
    # Add actions to the admin (optional)
    actions = ['reset_balance']

    # Optional: Define actions to reset the balance
    def reset_balance(self, request, queryset):
        for wallet in queryset:
            wallet.balance = 0
            wallet.save()
        self.message_user(request, "Selected wallets have been reset to zero balance.")
    reset_balance.short_description = "Reset selected wallet balances to zero"


class UserPlanAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin
    list_display = ('user', 'plan', 'status', 'date_completed', 'current_balance', 'created_at', 'updated_at')
    # Filters available in the admin
    list_filter = ('status', 'plan', 'user')
    # Fields to search in the admin
    search_fields = ('user__username', 'plan__name', 'status')

    # Optional: Add a method to format the date_completed as a string in the list view
    def date_completed_formatted(self, obj):
        return obj.date_completed.strftime('%Y-%m-%d %H:%M') if obj.date_completed else 'N/A'
    date_completed_formatted.short_description = 'Date Completed'


# Register your models with the custom admin classes
admin.site.register(UserWallet, UserWalletAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
