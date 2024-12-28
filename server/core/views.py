from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.utils import timezone
from .models import AppUsers, TempCSVData, MainData, TransactionLog
import json
from django.core.exceptions import ValidationError


# -----------------------
# 1. Signup View
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            password = data.get('password')
            team_name = data.get('team_name')

            if not (full_name and email and password and team_name):
                return JsonResponse({"error": "All fields are required."}, status=400)

            if AppUsers.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered."}, status=400)

            hashed_password = make_password(password)

            AppUsers.objects.create(
                full_name=full_name,
                email=email,
                password=hashed_password,
                team_name=team_name
            )

            return JsonResponse({"message": "User registered successfully."}, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Signup failed.", "details": str(e)}, status=500)


# -----------------------
# 2. Login View
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not (email and password):
                return JsonResponse({"error": "Email and password are required."}, status=400)

            user = get_object_or_404(AppUsers, email=email)

            if not check_password(password, user.password):
                return JsonResponse({"error": "Invalid password."}, status=401)

            return JsonResponse({
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "team_name": user.team_name,
                    "loggedInStatus":True
                }
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": "Login failed.", "details": str(e)}, status=500)


# -----------------------
# 3. Upload CSV Data (TempCSVData)
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class UploadCSVDataView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            uploaded_by_id = data.get('uploaded_by')
            csv_data = data.get('data')

            # Validate uploaded_by exists
            uploaded_by = get_object_or_404(AppUsers, id=uploaded_by_id)

            # Generate unique transaction ID
            transaction_id = f"txn_{timezone.now().strftime('%Y%m%d%H%M%S')}"

            # Create TempCSVData entry
            temp_data = TempCSVData.objects.create(
                transaction_id=transaction_id,
                uploaded_by=uploaded_by,
                data=csv_data
            )

            return JsonResponse({
                "message": "CSV data uploaded successfully.",
                "transaction_id": transaction_id
            }, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to upload CSV data.", "details": str(e)}, status=500)


# -----------------------
# 4. Approve Transaction
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class ApproveTransactionView(View):
    def post(self, request, transaction_id):
        try:
            data = json.loads(request.body)
            approved_by_id = data.get('approved_by')
            comments = data.get('comments', '')

            # Validate approver exists
            approved_by = get_object_or_404(AppUsers, id=approved_by_id)

            # Ensure only Management users can approve
            if approved_by.team_name != 'Management':
                return JsonResponse({"error": "Only users from the Management team can approve transactions."}, status=403)

            with transaction.atomic():
                # Fetch temp transaction
                temp_data = get_object_or_404(TempCSVData, transaction_id=transaction_id)
                csv_data = temp_data.data

                # Migrate data to MainData
                MainData.objects.create(
                    creator_name=csv_data['creator_name'],
                    ucid=csv_data.get('ucid'),
                    ig_handle=csv_data.get('ig_handle'),
                    gender=csv_data.get('gender'),
                    language=csv_data.get('language'),
                    genre=csv_data.get('genre'),
                    contacts=csv_data['contacts'],
                    contact_number=csv_data.get('contact_number'),
                    email_id=csv_data.get('email_id'),
                    median_views=csv_data.get('median_views'),
                    campaign_name=csv_data['campaign_name'],
                    date=csv_data['date'],
                    brand_name=csv_data.get('brand_name'),
                    trend_type=csv_data.get('trend_type'),
                    current_cost=csv_data['current_cost'],
                    current_deliverables=csv_data['current_deliverables']
                )

                # Log the transaction approval
                TransactionLog.objects.create(
                    transaction=temp_data,
                    approved_by=approved_by,
                    status='Approved',
                    approval_date=timezone.now(),
                    comments=comments
                )

                # Delete TempCSVData after approval
                temp_data.delete()

            return JsonResponse({"message": "Transaction approved and data migrated successfully."}, status=200)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to approve transaction.", "details": str(e)}, status=500)


# -----------------------
# 5. Reject Transaction
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class RejectTransactionView(View):
    def post(self, request, transaction_id):
        try:
            data = json.loads(request.body)
            rejected_by_id = data.get('rejected_by')
            comments = data.get('comments', '')

            # Validate approver exists
            rejected_by = get_object_or_404(AppUsers, id=rejected_by_id)

            # Ensure only Management users can reject
            if rejected_by.team_name != 'Management':
                return JsonResponse({"error": "Only users from the Management team can reject transactions."}, status=403)

            temp_data = get_object_or_404(TempCSVData, transaction_id=transaction_id)

            # Log the rejection
            TransactionLog.objects.create(
                transaction=temp_data,
                approved_by=rejected_by,
                status='Rejected',
                approval_date=timezone.now(),
                comments=comments
            )

            temp_data.delete()

            return JsonResponse({"message": "Transaction rejected successfully."}, status=200)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to reject transaction.", "details": str(e)}, status=500)

# -----------------------
# 6. Transaction Status
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class TransactionStatusView(View):
    def get(self, request, transaction_id):
        transaction = get_object_or_404(TransactionLog, transaction__transaction_id=transaction_id)
        return JsonResponse({
            "transaction_id": transaction.transaction.transaction_id,
            "status": transaction.status,
            "approved_by": transaction.approved_by.full_name if transaction.approved_by else None,
            "approval_date": transaction.approval_date,
            "comments": transaction.comments
        }, status=200)