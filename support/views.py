from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TicketForm
from .models import Ticket


@login_required
def support_hub(request):
    """Renders the master unified support hub containing all help desk modules and handles ticket submissions."""
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST' and 'subject' in request.POST:
        form = TicketForm(request.POST)
        if form.is_valid():
            try:
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
            except Exception:
                messages.error(request, "An error occurred while submitting your ticket. Please try again.")
            else:
                messages.success(request, f"Support ticket #{ticket.id} ('{ticket.subject}') has been opened successfully.")
                return redirect('support:support_hub')
        else:
            messages.error(request, "Please correct the errors in your ticket submission.")
    else:
        form = TicketForm()

    context = {
        "tickets": tickets,
        "ticket_count": tickets.count(),
        "form": form,
        "title": "Client Support Hub",
    }
    return render(request, 'support/support_hub.html', context)


@login_required
def user_ticket_list(request):
    """Shows the logged-in user their own support tickets."""
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        "tickets": tickets,
        "ticket_count": tickets.count(),
    }
    return render(request, 'support/ticket_list.html', context)


@login_required
def create_ticket(request):
    """Allows a user to submit a new ticket to the Help Desk via the dedicated form view."""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            try:
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
            except Exception:
                messages.error(request, "An error occurred while submitting your ticket. Please try again.")
            else:
                messages.success(request, f"Support ticket #{ticket.id} ('{ticket.subject}') has been opened successfully.")
                return redirect('support:support_hub')
        else:
            messages.error(request, "Please correct the errors in your submission.")
    else:
        form = TicketForm()
        
    context = {
        "form": form,
        "title": "Open Support Ticket"
    }
    return render(request, 'support/ticket_form.html', context)