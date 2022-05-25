from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 4)]


class CartAddTestForm(forms.Form):
    correct = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                widget = forms.NumberInput(attrs={'style': 'width:40px','readonly':'readonly'})
                                )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
