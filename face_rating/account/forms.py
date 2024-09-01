from django import forms
from .models import AccountModel
import face_recognition
import cv2
import numpy as np
import json

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = AccountModel
        fields = ['email', 'username', 'face_image_encoding', 'face_image']

    def validate_password_match(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if AccountModel.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên người dùng đã tồn tại")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if AccountModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại")
        return email
    def clean_face_image(self):
        face_image = self.cleaned_data.get("face_image")
        if face_image:
            # Mã hóa ảnh khuôn mặt
            img = cv2.imdecode(np.fromstring(face_image.read(), np.uint8), cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_encoding = face_recognition.face_encodings(rgb_img)
            if len(img_encoding) > 0:
                # Chuyển đổi mảng thành danh sách và sau đó sang JSON
                self.cleaned_data['face_image_encoding'] = json.dumps(img_encoding[0].tolist())
                print("Dang ky khuon mat thanh cong")
            else:
                raise forms.ValidationError("Không thể nhận diện khuôn mặt từ ảnh được cung cấp")
        return face_image

            
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.face_image_encoding = self.cleaned_data.get("face_image_encoding")
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        self.validate_password_match()
        return cleaned_data

from django.contrib.auth.forms import AuthenticationForm

class SignInForm(AuthenticationForm):
    # email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
 
