"""OpenNLP forms."""

from django import forms

CHOICES = (
        ("location", "Locations"),
        ("date", "Dates"),
        ("money", "Money"),
        ("organization", "Organisations"),
        ("person", "People"),
        ("time", "Times"),
        ("percentage", "Percentages"),
)

class OpenNLPForm(forms.Form):
    text = forms.CharField("Paste text here", widget=forms.Textarea(
        attrs={"class":"bulktext", "style":"width:100%"}
        ))
    entity = forms.MultipleChoiceField(choices=CHOICES)
