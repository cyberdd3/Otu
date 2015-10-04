from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import UserProfile, Comment, Post


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='email', max_length=75)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise (forms.ValidationError("This email is already taken"))
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
