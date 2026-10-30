from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

@login_required
def user_ticket_list(request):
    """Shows the logged-in user their own support tickets."""
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    """Allows a user to submit a new ticket to the Help Desk."""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('user_ticket_list')
    else:
        form = TicketForm()
        
    return render(request, 'support/ticket_form.html', {'form': form, 'title': 'Open Support Ticket'})
