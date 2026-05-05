from django import forms
from fetch_scripts.domains import DOMAINS

DOMAIN_CHOICES = [("", "— inchangé —")] + [(k, v["label"]) for k, v in DOMAINS.items()]


class FeedbackForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5,
                                widget=forms.NumberInput(attrs={"class": "form-control"}))
    comment = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    suggested_domain = forms.ChoiceField(choices=DOMAIN_CHOICES, required=False,
                                         widget=forms.Select(attrs={"class": "form-select"}))
