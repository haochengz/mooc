
import re

from django import forms

from operations.models import UserConsult


class UserConsultForm(forms.ModelForm):

    class Meta:
        model = UserConsult
        fields = [
            "name", "mobile", "course_name",
        ]

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        MOBILE_PATTERN = "^1[358]\d{9}$|^147\d{8}$|^17\d{9}$"
        p = re.compile(pattern=MOBILE_PATTERN)
        if p.match(mobile):
            return mobile
        raise forms.ValidationError("Invalid mobile phone number", code="invalid_mobile")
