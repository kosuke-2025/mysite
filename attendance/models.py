from django.db import models
from django.conf import settings
from django.utils import timezone

class Attendance(models.Model): # クラス名をより一般的な'Attendance'に変更
    class Status(models.IntegerChoices):
        ATTENDING = 0, '来た'
        PLANNING_TO_GO = 1, '行くつもり'
        NOT_GOING = 2, '行かない'
        UNREGISTERED = 3, '未登録'

    # ユーザー
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name="名前", 
        on_delete=models.CASCADE
    )
    # 日付 (★重要: このフィールドを追加)
    date = models.DateField(verbose_name="日付", default=timezone.now)
    # ステータス
    in_out = models.IntegerField(
        verbose_name='IN/OUT', 
        choices=Status.choices, 
        default=Status.UNREGISTERED # デフォルト値を'未登録'に設定
    )

    comment = models.TextField(
        verbose_name="今日のコメント", 
        blank=True, # 空欄での保存を許可
        null=True   # データベースにNULLでの保存を許可
    )

    class Meta:
        db_table = 'attendance'
        # 同じユーザーが同じ日に複数登録できないようにする制約 (★重要)
        unique_together = ['staff', 'date']

    def __str__(self):
        return f"{self.staff.username} on {self.date}"