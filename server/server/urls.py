from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    # Django Admin URL
    path('admin/', admin.site.urls),
    
    # API routes for the app
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('api/upload_csv/', views.UploadCSVDataView.as_view(), name='upload_csv'),
    path('api/approve_transaction/<int:transaction_id>/', views.ApproveTransactionView.as_view(), name='approve_transaction'),
    path('api/reject_transaction/<int:transaction_id>/', views.RejectTransactionView.as_view(), name='reject_transaction'),
    path('api/transactions/', views.TransactionStatusView.as_view(), name='transaction_list'),
]
