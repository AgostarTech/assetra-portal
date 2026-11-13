from django import forms
from .models import Ticket, SiteVerificationFile

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


class SiteVerificationForm(forms.ModelForm):
    class Meta:
        model = SiteVerificationFile
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-[#086070] focus:ring-2 focus:ring-[#086070]/20 text-sm outline-none transition',
                'placeholder': 'e.g., Google Search Console Verification'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-[#086070]/10 file:text-[#086070] hover:file:bg-[#086070]/20 cursor-pointer'
            })
        }