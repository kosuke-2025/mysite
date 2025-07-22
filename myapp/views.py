from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import SignUpForm


class IndexView(TemplateView):
    template_name = "myapp/index.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "myapp/signup.html"

    def get_success_url(self):
        return reverse("myapp:user_home", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserHomeView(DetailView):
    model = get_user_model()
    template_name = "myapp/user_home.html"
    context_object_name = 'user_obj'

class MyLoginView(LoginView):
    template_name = 'myapp/login.html'

    def get_success_url(self):
        """
        ログイン成功後のリダイレクト先を動的に生成する。
        """
        # ログインしたユーザーのpk（プライマリーキー）を取得
        user_pk = self.request.user.pk
        
        # user_homeのURLを逆引きして返す
        return reverse('myapp:user_home', kwargs={'pk': user_pk})