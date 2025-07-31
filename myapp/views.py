from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import SignUpForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from attendance.models import Attendance
from attendance.forms import AttendanceForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "myapp/index.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "myapp/signup.html"

    def get_success_url(self):
        return reverse("myapp:user_home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserHomeView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "myapp/user_home.html"
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        """
        URLのpkやslugではなく、ログインしているユーザーをオブジェクトとして返す
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストに、追加のデータを加える
        """
        # 親クラスのメソッドを呼び出し、基本的なコンテキストを取得
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        # ログインユーザーの今日の出欠データを取得または作成
        attendance, created = Attendance.objects.get_or_create(
            staff=self.request.user,
            date=today
        )

        # コンテキストに出欠フォームと今日の日付を追加
        context['form'] = AttendanceForm(instance=attendance)
        context['today'] = today
        context['current_status'] = attendance.get_in_out_display()
        
        return context

class MyLoginView(LoginView):
    template_name = 'myapp/login.html'

    def get_success_url(self):
        """
        ログイン成功後のリダイレクト先を動的に生成する。
        """
        # ログインしたユーザーのpk（プライマリーキー）を取得
        #user_pk = self.request.user.pk
        
        # user_homeのURLを逆引きして返す
        return reverse('myapp:user_home')
    

# @login_required
# def home_view(request):
#     print("a")
#     """
#     ユーザーのホーム画面を表示し、出欠フォームの準備も行う
#     """
#     today = timezone.localdate()

#     # ログインユーザーの「今日」の出欠データを取得、なければ作成
#     attendance, created = Attendance.objects.get_or_create(
#         user=request.user,  # Django 4.x以降ではstaffよりuserが一般的
#         date=today
#     )

#     # 取得または作成したデータで出欠フォームを初期化
#     form = AttendanceForm(instance=attendance)

#     # フォームをテンプレートのコンテキストに追加
#     context = {
#         'form': form,
#         'today': today,
#         'current_status': attendance.get_in_out_display(),
#     }
#     return render(request, 'myapp:user_home', context)