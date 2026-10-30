from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm

@login_required
def document_list(request):
    # Enforce object-level authorization for documents
    documents = Document.objects.filter(uploader=request.user).order_by('-uploaded_at')
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploader = request.user
            # Automatically set status to SUBMITTED upon user upload
            document.status = Document.StatusChoices.SUBMITTED
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm(request.user)
        
    return render(request, 'documents/document_form.html', {'form': form, 'title': 'Upload Document'})
from django.utils import timezone
from django.http import HttpResponseForbidden

@login_required
def review_document(request, doc_id):
    if not request.user.is_manager():
        return HttpResponseForbidden("Unauthorized")
        
    document = Document.objects.get(id=doc_id)
    
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
        
        return redirect("manager_dashboard")
        
    return render(request, "documents/review_document.html", {"document": document})
