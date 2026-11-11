from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("upload/", views.upload_document, name="upload_document"),
    path("queue/", views.document_verification_queue, name="document_verification_queue"),
    path("review/<int:doc_id>/", views.review_document, name="review_document"),
]