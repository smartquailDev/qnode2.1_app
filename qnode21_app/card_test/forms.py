from django import forms


TEST_VALUES_CHOICES = [(i, str(i)) for i in range(1, 2)]


class CartAddTestForm(forms.Form):
    correct = forms.TypedChoiceField(
                                choices=TEST_VALUES_CHOICES,
                                coerce=int,
                                widget=forms.HiddenInput,
                                initial = '1'
                                )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
