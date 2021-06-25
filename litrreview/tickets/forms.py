from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

RATINGS = (
    ('', 'Choisir...'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class TicketReviewForm(forms.Form):
    title = forms.CharField(max_length=200, label='Titre', widget=forms.TextInput(
        attrs={'placeholder': 'Titre du ticket'}))

    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'placeholder': "Merci d'entrer la description du livre"}))
    image = forms.ImageField()

    headline = forms.CharField(max_length=200, label='Titre', widget=forms.TextInput(
        attrs={'placeholder': 'Titre  de la critique'}))
    body = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'placeholder': "Merci d'ecrire votre critique ici"}))
    rating = forms.ChoiceField(choices=RATINGS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            'image',
            'headline',
            'body',
            'rating',
            Submit('submit', 'Envoyer')
        )
