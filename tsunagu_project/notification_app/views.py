import imp
from django.shortcuts import render, redirect
# モデルをインポート
from notification_app.models import Notification

def ShowNotification(request):
    # ユーザ取得
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    context = {
        'notifications': notifications,

    }
    # 'notifications/notification.html'　のフォルダを持ってきて出力
    # データベースのデータ(context)をテンプレート(HTML)に変換
    # 作成されたHTMLをHTTPレスポンスで出力
    return render(request, 'notifications/notification.html', context)


# 通知削除右上の✖
def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notification')
