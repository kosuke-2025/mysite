# attendance/views.py

from django.shortcuts import redirect, render
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

@login_required
def attendance_list_view(request):
    """
    「本日」の全ユーザーの出席データを一覧で表示する
    """
    # 1. 今日の日付を取得
    today = timezone.localdate()

    user_attendance, created = Attendance.objects.get_or_create(
        staff=request.user,
        date=today
    )

    # もしユーザーのステータスが「未登録」だったら...
    if user_attendance.in_out == Attendance.Status.UNREGISTERED:
        # エラーメッセージをセットして、ホーム画面にリダイレクト
        messages.error(request, "出席状況を登録しないと一覧は閲覧できません。")
        return redirect('myapp:user_home')

    # 2. 今日の日付でデータを絞り込む (filter)
    todays_attendances = Attendance.objects.filter(date=today).order_by('staff__username')

    context = {
        'attendance_list': todays_attendances,
        'display_date': today, # テンプレートで日付を表示するために追加
    }
    
    return render(request, 'attendance/attendance_list.html', context)