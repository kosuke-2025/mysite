# attendance/views.py

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm

@login_required
def record_attendance(request):
    """
    フォームからのPOSTリクエストを処理し、データを保存する
    """
    if request.method == 'POST':
        today = timezone.localdate()
        
        # ログインユーザーの今日のデータを取得
        attendance = Attendance.objects.get(staff=request.user, date=today)
        
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'ステータスを更新しました。')

    # 処理が終わったら、myappのホーム画面にリダイレクト
    return redirect('myapp:user_home') # myappのurls.pyで設定したname