from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'priority', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'style': 'width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 4px;'})
