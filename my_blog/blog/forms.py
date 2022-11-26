from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models  import Post, Comment








class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'reg-form'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'reg-form'}))
    

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
       
        help_texts ={
            'username': None,
            'password1': None,
            'password2': None,


        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['username'].widget.attrs['class']= "reg-form"
        self.fields['password1'].widget.attrs['class']= "reg-form"
        self.fields['password2'].widget.attrs['class']= "reg-form"









class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'body',)
        labels ={
            'body': ''
        }

        widgets = {
            'body': forms.Textarea(attrs={'class': 'post-form', 'placeholder': 'Add comment...'}),
                       
    }