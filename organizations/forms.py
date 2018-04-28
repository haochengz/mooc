
from django import forms

from operations.models import UserConsult


class UserConsultForm(forms.ModelForm):

    class Meta:
        model = UserConsult
        fields = [
            "name", "mobile", "course_name",
        ]
