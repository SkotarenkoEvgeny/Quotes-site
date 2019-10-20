from django.forms.models import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import MessagesToAdmin

class AdminContactForm(ModelForm):

    class Meta:
        model = MessagesToAdmin
        fields = ['from_email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        # add buttons
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit('reset', 'Reset'))
        self.helper.add_input(Submit('cancel', 'Cancel'))
