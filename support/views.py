from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TicketForm, SiteVerificationForm
from .models import Ticket, SiteVerificationFile


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


def is_admin_user(user):
    return user.is_superuser or user.is_staff or getattr(user, 'role', '') == 'ADMIN'


@login_required
@user_passes_test(is_admin_user)
def manage_seo_files(request):
    """Allows admins to manage and upload SEO and site verification files."""
    if request.method == 'POST':
        form = SiteVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "SEO verification file uploaded successfully.")
            return redirect('support:seo_files_manager')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SiteVerificationForm()

    files = SiteVerificationFile.objects.all().order_by('-uploaded_at')
    return render(request, 'support/seo_files_manager.html', {
        'form': form,
        'files': files
    })


@login_required
@user_passes_test(is_admin_user)
def edit_seo_file(request, pk):
    """Allows admins to edit an existing SEO verification file's title or replace the file."""
    file_obj = get_object_or_404(SiteVerificationFile, pk=pk)
    if request.method == 'POST':
        form = SiteVerificationForm(request.POST, request.FILES, instance=file_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Verification file '{file_obj.title}' updated successfully.")
            return redirect('support:seo_files_manager')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SiteVerificationForm(instance=file_obj)

    return render(request, 'support/seo_file_edit.html', {
        'form': form,
        'file_obj': file_obj
    })


@login_required
@user_passes_test(is_admin_user)
def delete_seo_file(request, pk):
    """Allows admins to delete an uploaded SEO verification file."""
    file_obj = get_object_or_404(SiteVerificationFile, pk=pk)
    file_obj.delete()
    messages.success(request, "Verification file removed successfully.")
    return redirect('support:seo_files_manager')


def serve_verification_file(request, filename):
    """Dynamically serves uploaded verification files directly at the site root."""
    for item in SiteVerificationFile.objects.all():
        if item.filename == filename:
            try:
                return FileResponse(item.file.open('rb'))
            except Exception:
                raise Http404("File could not be read.")
    raise Http404("Verification file not found.")