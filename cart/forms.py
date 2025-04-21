from django import forms


class Add2CartForm(forms.Form):
    """
    Form for adding a product to the shopping cart.

    Allows the user to specify a quantity between 1 and 12.
    """

    quantity = forms.IntegerField(
        min_value=1,
        max_value=12,
        label="Quantity"
    )

