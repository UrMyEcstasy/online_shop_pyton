from django import forms


class CouponForm(forms.Form):
    """
    Form for applying a discount coupon.

    Contains a single input field for entering the coupon code.
    """
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Coupon Code"
    )
