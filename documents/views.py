from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden

from .models import Document
from .forms import DocumentForm


def _is_admin(user):
    """Check if user has admin privileges (superuser, staff, or ADMIN role)."""
    return user.is_authenticated and (
        user.is_superuser or user.is_staff or getattr(user, "role", "USER").upper() == "ADMIN"
    )


@login_required
def document_list(request):
    """Enforce object-level authorization for user verification documents."""
    documents = Document.objects.filter(uploader=request.user).order_by('-uploaded_at')
    
    context = {
        'documents': documents,
    }
    return render(request, 'documents/document_list.html', context)


@login_required
def upload_document(request):
    """Handle user document uploads for compliance verification."""
    if request.method == 'POST':
        form = DocumentForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploader = request.user
            document.status = Document.StatusChoices.SUBMITTED
            document.save()
            messages.success(request, "Document uploaded successfully and submitted for review.")
            return redirect('documents:document_list')
    else:
        form = DocumentForm(request.user)
        
    context = {
        'form': form,
        'title': 'Upload Document',
    }
    return render(request, 'documents/document_form.html', context)


@login_required
def document_verification_queue(request):
    """Display pending compliance documents for administrative review and SLA monitoring."""
    if not _is_admin(request.user):
        messages.error(request, "Unauthorized access. Admin privileges required.")
        return redirect('documents:document_list')

    documents = (
        Document.objects.all()
        .select_related("uploader", "reviewed_by")
        .order_by("-uploaded_at")
    )

    context = {
        "documents": documents,
    }
    return render(request, "documents/document_verification_queue.html", context)


@login_required
def review_document(request, doc_id):
    """Allow administrators to review, approve, or reject submitted compliance documents."""
    if not _is_admin(request.user):
        return HttpResponseForbidden("Unauthorized access. Admin privileges required.")
        
    document = get_object_or_404(Document, id=doc_id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        notes = request.POST.get("review_notes", "")
        
        if action == "approve":
            document.status = Document.StatusChoices.APPROVED
        elif action == "reject":
            document.status = Document.StatusChoices.REJECTED
            
        document.reviewed_by = request.user
        document.reviewed_at = timezone.now()
        document.review_notes = notes
        document.save()
        
        messages.success(request, f"Document '{document.title}' has been {document.get_status_display().lower()}.")
        return redirect("documents:document_verification_queue")
        
    context = {
        "document": document,
    }
    return render(request, "documents/review_document.html", context)