from django import forms
from .models import Note


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "description", "file"]
