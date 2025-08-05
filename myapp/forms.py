from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django import forms

class SignUpForm(UserCreationForm):
    passcode = forms.CharField(
        label="サインアップ用パスコード",
        widget=forms.PasswordInput() # 入力内容が●で隠れるようにする
    )

    field_order = ['passcode', 'username', 'password',]

    class Meta:
        model = User
        fields = ["username"]
    
    def clean(self):
        # まず親クラスのcleanメソッドを呼び出し、基本的な検証を行う
        cleaned_data = super().clean()
        
        # フォームに入力されたパスコードを取得
        entered_passcode = cleaned_data.get('passcode')
        
        # settings.pyで設定した正しいパスコードと比較
        if entered_passcode != settings.SIGNUP_PASSCODE:
            # もし一致しなかったら、検証エラーを発生させる
            raise forms.ValidationError("招待パスコードが正しくありません。")
            
        return cleaned_data
