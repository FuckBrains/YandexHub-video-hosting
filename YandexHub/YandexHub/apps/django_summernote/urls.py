from django.urls import path

from .views import SummernoteEditor, SummernoteUploadAttachment

urlpatterns = [
    path('editor/<str:id>/', SummernoteEditor.as_view(), name='django_summernote-editor'),
    path('upload_attachment/', SummernoteUploadAttachment.as_view(), name='django_summernote-upload_attachment'),
]
