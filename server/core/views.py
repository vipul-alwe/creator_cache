from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.utils import timezone
from .models import AppUsers, TempCSVData, MainData, TransactionLog, Vault
import json
from django.core.exceptions import ValidationError
from django.db.models import Q
from .serializers import VaultSerializer


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
            csv_data = data.get('csv_data')
            campaign_name = data.get('campaign_name')  # New Field

            if not campaign_name:
                return JsonResponse({"error": "Campaign Name is required."}, status=400)

            # Validate uploader
            uploaded_by = AppUsers.objects.get(id=uploaded_by_id)

            with transaction.atomic():
                transaction_id = timezone.now().strftime('%Y%m%d%H%M%S')
                TempCSVData.objects.create(
                    transaction_id=transaction_id,
                    data=csv_data,
                    uploaded_by=uploaded_by,
                    status='Pending',
                    campaign_name=campaign_name  # Store campaign name
                )

            return JsonResponse({"message": "CSV uploaded successfully.", "transaction_id": transaction_id}, status=201)

        except AppUsers.DoesNotExist:
            return JsonResponse({"error": "Uploader does not exist."}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to upload CSV.", "details": str(e)}, status=500)


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
                return JsonResponse(
                    {"error": "Only users from the Management team can approve transactions."}, 
                    status=403
                )

            with transaction.atomic():
                # Fetch temp transaction
                temp_data = get_object_or_404(TempCSVData, transaction_id=transaction_id)

                if temp_data.status == 'Approved':
                    return JsonResponse(
                        {"error": "This transaction has already been approved."}, 
                        status=400
                    )

                # Check if the campaign name already exists
                existing_campaign = TempCSVData.objects.filter(campaign_name=temp_data.campaign_name).first()
                
                if existing_campaign:
                    if existing_campaign.status == 'Approved':
                        return JsonResponse(
                            {
                                "error": "This campaign has already been approved. Please revert the previous transaction before approving again."
                            }, 
                            status=400
                        )
                    elif existing_campaign.status == 'Reverted':
                        # Allow approval if the previous transaction was reverted
                        pass

                # Proceed with approval
                csv_data = temp_data.data

                # Handle both single object and list of objects
                if isinstance(csv_data, list):
                    for entry in csv_data:
                        MainData.objects.create(
                            creator_name=entry['creator_name'],
                            ucid=entry.get('ucid'),
                            ig_handle=entry.get('ig_handle'),
                            gender=entry.get('gender'),
                            language=entry.get('language'),
                            genre=entry.get('genre'),
                            contacts=entry['contacts'],
                            contact_number=entry.get('contact_number'),
                            email_id=entry.get('email_id'),
                            median_views=entry.get('median_views'),
                            campaign_name=entry['campaign_name'],
                            date=entry['date'],
                            brand_name=entry.get('brand_name'),
                            trend_type=entry.get('trend_type'),
                            current_cost=entry['current_cost'],
                            current_deliverables=entry['current_deliverables']
                        )
                else:
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

                # Update TempCSVData status
                temp_data.status = 'Approved'
                temp_data.save()

                # Log the transaction approval
                TransactionLog.objects.create(
                    transaction=temp_data,
                    approved_by=approved_by,
                    status='Approved',
                    approval_date=timezone.now(),
                    comments=comments
                )

            return JsonResponse(
                {"message": "Transaction approved and data migrated successfully."}, 
                status=200
            )

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to approve transaction.", "details": str(e)}, 
                status=500
            )


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

            # Validate rejecter exists
            rejected_by = get_object_or_404(AppUsers, id=rejected_by_id)

            # Ensure only Management users can reject
            if rejected_by.team_name != 'Management':
                return JsonResponse(
                    {"error": "Only users from the Management team can reject transactions."},
                    status=403
                )

            with transaction.atomic():
                # Fetch temp transaction
                temp_data = get_object_or_404(TempCSVData, transaction_id=transaction_id)

                # Update TempCSVData status
                temp_data.status = 'Rejected'
                temp_data.save()

                # Log the transaction rejection
                TransactionLog.objects.create(
                    transaction=temp_data,
                    approved_by=rejected_by,
                    status='Rejected',
                    approval_date=timezone.now(),
                    comments=comments,
                    campaign_name=temp_data.campaign_name  # Copy campaign name from TempCSVData
                )

            return JsonResponse(
                {"message": "Transaction rejected successfully."},
                status=200
            )

        except AppUsers.DoesNotExist:
            return JsonResponse({"error": "Rejecter does not exist."}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to reject transaction.", "details": str(e)},
                status=500
            )

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
    

# -----------------------
# 7. Revert Transaction
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class RevertTransactionView(View):
    def post(self, request, transaction_id):
        try:
            data = json.loads(request.body)
            reverted_by_id = data.get('reverted_by')
            comments = data.get('comments', '')

            # Validate user exists
            reverted_by = get_object_or_404(AppUsers, id=reverted_by_id)

            # Ensure only Management users can revert
            if reverted_by.team_name != 'Management':
                return JsonResponse({"error": "Only users from the Management team can revert transactions."}, status=403)

            with transaction.atomic():
                # Fetch the TempCSVData and ensure it was approved
                temp_data = get_object_or_404(TempCSVData, transaction_id=transaction_id, status='Approved')
                csv_data = temp_data.data

                deleted_count = 0

                # Handle both single object and list of objects in CSV data
                if isinstance(csv_data, list):
                    for entry in csv_data:
                        deleted, _ = MainData.objects.filter(
                            creator_name=entry['creator_name'],
                            campaign_name=entry['campaign_name'],
                            date=entry['date'],
                            brand_name=entry.get('brand_name')
                        ).delete()
                        deleted_count += deleted
                else:
                    deleted, _ = MainData.objects.filter(
                        creator_name=csv_data['creator_name'],
                        campaign_name=csv_data['campaign_name'],
                        date=csv_data['date'],
                        brand_name=csv_data.get('brand_name')
                    ).delete()
                    deleted_count += deleted

                if deleted_count == 0:
                    return JsonResponse({"error": "No matching data found in MainData for the given transaction to revert."}, status=404)

                # Update the TempCSVData status back to 'Pending'
                temp_data.status = 'Pending'
                temp_data.save()

                # Log the revert action in TransactionLog
                TransactionLog.objects.create(
                    transaction=temp_data,
                    approved_by=reverted_by,
                    status='Reverted',
                    approval_date=timezone.now(),
                    comments=comments
                )

            return JsonResponse({
                "message": "Transaction successfully reverted.",
                "details": f"{deleted_count} entries removed from MainData."
            }, status=200)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except TempCSVData.DoesNotExist:
            return JsonResponse({"error": "Approved transaction not found or already reverted."}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Failed to revert transaction.", "details": str(e)}, status=500)
        

# -----------------------
# 8. Filter Vault
# -----------------------
@method_decorator(csrf_exempt, name='dispatch')
class VaultFilterView(View):
    """
    View to filter Vault data based on query parameters with support for ranges.
    """

    def get(self, request):
        filters = Q()

        # Extract filter parameters from the query string
        creator_name = request.GET.get('creator_name')
        channel_link = request.GET.get('channel_link')
        gender = request.GET.get('gender')
        language = request.GET.get('language')
        genre = request.GET.get('genre')
        ig_link = request.GET.get('ig_link')
        campaign_name = request.GET.get('campaign_name')  # Added campaign_name filter

        # Range-based filters for numeric fields
        ig_subs_min = request.GET.get('ig_subs_min')
        ig_subs_max = request.GET.get('ig_subs_max')

        pct_13_17_min = request.GET.get('pct_13_17_min')
        pct_13_17_max = request.GET.get('pct_13_17_max')

        yt_genz_13_24_min = request.GET.get('yt_genz_13_24_min')
        yt_genz_13_24_max = request.GET.get('yt_genz_13_24_max')

        rpr_min = request.GET.get('rpr_min')
        rpr_max = request.GET.get('rpr_max')

        # Apply basic filters
        if creator_name:
            filters &= Q(creator_name__icontains=creator_name)
        if channel_link:
            filters &= Q(channel_link__icontains=channel_link)
        if gender:
            filters &= Q(gender__icontains=gender)
        if language:
            filters &= Q(language__icontains=language)
        if genre:
            filters &= Q(genre__icontains=genre)
        if ig_link:
            filters &= Q(ig_link__icontains=ig_link)
        if campaign_name:
            filters &= Q(campaign_name__icontains=campaign_name)  # Campaign name filter

        # Apply range filters for numeric fields
        if ig_subs_min is not None:
            filters &= Q(ig_subs__gte=int(ig_subs_min))  # Greater than or equal to
        if ig_subs_max is not None:
            filters &= Q(ig_subs__lte=int(ig_subs_max))  # Less than or equal to

        if pct_13_17_min is not None:
            filters &= Q(pct_13_17__gte=float(pct_13_17_min))  # Greater than or equal to
        if pct_13_17_max is not None:
            filters &= Q(pct_13_17__lte=float(pct_13_17_max))  # Less than or equal to

        if yt_genz_13_24_min is not None:
            filters &= Q(yt_genz_13_24__gte=float(yt_genz_13_24_min))  # Greater than or equal to
        if yt_genz_13_24_max is not None:
            filters &= Q(yt_genz_13_24__lte=float(yt_genz_13_24_max))  # Less than or equal to

        if rpr_min is not None:
            filters &= Q(rpr__gte=float(rpr_min))  # Greater than or equal to
        if rpr_max is not None:
            filters &= Q(rpr__lte=float(rpr_max))  # Less than or equal to

        # Query the database with the filters
        filtered_data = Vault.objects.filter(filters)

        # Serialize the data
        serializer = VaultSerializer(filtered_data, many=True)

        # Return the filtered data as JSON
        return JsonResponse(serializer.data, safe=False)
