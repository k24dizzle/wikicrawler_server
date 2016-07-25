from django import forms

class StartForm(forms.Form):
    difficulty_choices = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    name = forms.CharField(label="Name ", max_length=100)
    starting_page = forms.CharField(label="Starting Page ", max_length=400)
    difficulty = forms.ChoiceField(choices=difficulty_choices)

    def __init__(self, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)

