from django import forms
from askme.models import Answer, Question, Tag, User
from askme.models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length = 4, widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length = 4, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length = 4, widget=forms.PasswordInput)
    class Meta:
            model = User
            fields = ['username','first_name', 'last_name', 'email']

    def save(self):
        self.cleaned_data.pop('password_check')
        user_ = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(user = user_, nickname = user_.username)
        return user_
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')

class AskQuestionForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()

    def save(self, request):
        question_ = Question.objects.create(title=self.cleaned_data.pop('title'), text=self.cleaned_data.pop('text'), profile=request.user.profile)
        tags = (str(self.cleaned_data.pop('tags'))).split()
        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                question_.tag.add(Tag.objects.get(name=tag))
                print("exists" + tag)
            else:
                tag_ = Tag.objects.create(name=tag)
                print("created" + tag)
                question_.tag.add(tag_) 
        return question_

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, request, question_):
        Answer.objects.create(question=question_, text=self.cleaned_data.pop('text'), profile=request.user.profile)
        return

    

