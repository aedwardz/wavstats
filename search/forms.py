from django import forms

class text_form(forms.Form):
    artist = forms.CharField(
                            required=True,
                            label='',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control me-2',
                                'type': 'search',
                                'placeholder': 'Drake',
                                'aria-label': 'Search'})
                             )

