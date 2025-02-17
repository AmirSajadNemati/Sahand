from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import ContactInfo, Branch, FaqCategory, HelpCategory, StaticForm
from base.serializers import ContactInfoSerializer, BranchSerializer, StaticFormSerializer
from frontend_api.models import Rule, ContactUs, AboutUs, Privacy, Bug, Criticism, Complaint, Suggestion
from frontend_api.serializers import ExtendedResponseSerializer, RuleContentSerializer, \
    ContactUsContentSerializer, AboutUsContentSerializer, AboutUsResponseSerializer, PrivacyContentSerializer, \
    FaqCategoryPageSerializer, HelpCategoryPageSerializer, BugContentSerializer, CriticismContentSerializer, \
    ComplaintContentSerializer, SuggestionContentSerializer
from info.models import CustomerComment, WhyUs, SiteFeature, Honor, Statistic, Team, TimeLine, Colleague
from info.serializers import CustomerCommentSerializer, WhyUsSerializer, SiteFeatureSerializer, HonorSerializer, \
    StatisticSerializer, TeamSerializer, TimeLineSerializer, ColleagueSerializer
from serializers import MessageAndIdSerializer


class ContactInfoView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(

        responses={
            200: OpenApiResponse(response=ExtendedResponseSerializer),
        },
        description="BlogList cmsPage"
    )
    def post(self, request, *args, **kwargs):
        # Get all ContactInfo and Branch data (filtering out deleted ones, for example)
        contact_infos = ContactInfo.objects.filter(is_deleted=False)
        branches = Branch.objects.filter(is_deleted=False)
        contact_us = ContactUs.objects.last()
        # Serialize the data
        contact_info_serializer = ContactInfoSerializer(contact_infos, many=True)
        branch_serializer = BranchSerializer(branches, many=True)
        content_serializer = ContactUsContentSerializer(contact_us)

        response_data = {
            "contactInfos": contact_info_serializer.data,
            "contactBranchs": branch_serializer.data,
            "content": content_serializer.data.get('content', '')
        }

        return Response(response_data)


class RulePageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=RuleContentSerializer)},
        description="Rules Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Rule instance
        rule = Rule.objects.last()

        if rule:
            # Serialize only the content field
            serializer = RuleContentSerializer(rule)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "صفحه مقررات یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)


class AboutUsPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=AboutUsResponseSerializer)},
        description="Rules Page API"
    )
    def post(self, request, *args, **kwargs):
        # Fetch AboutUs content and related ContentManager
        about_us = AboutUs.objects.first()  # Assuming there's only one entry
        content_serializer = AboutUsContentSerializer(about_us)

        # Fetch and serialize CustomerComment data
        customer_comments = CustomerComment.objects.all()
        customer_comments_serializer = CustomerCommentSerializer(customer_comments, many=True)

        # Fetch and serialize WhyUs data
        why_us = WhyUs.objects.all()
        why_us_serializer = WhyUsSerializer(why_us, many=True)

        # Fetch and serialize SiteFeature data
        site_features = SiteFeature.objects.all()
        site_features_serializer = SiteFeatureSerializer(site_features, many=True)

        # Fetch and serialize Honor data
        honors = Honor.objects.all()
        honor_serializer = HonorSerializer(honors, many=True)

        # Fetch and serialize Statistic data
        statistics = Statistic.objects.all()
        statistic_serializer = StatisticSerializer(statistics, many=True)

        # Fetch and serialize Team data
        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)

        # Fetch and serialize TimeLine data
        timelines = TimeLine.objects.all()
        timeline_serializer = TimeLineSerializer(timelines, many=True)

        # Fetch and serialize Colleague data
        colleagues = Colleague.objects.all()
        colleague_serializer = ColleagueSerializer(colleagues, many=True)

        # Prepare the response data
        response_data = {
            "content": content_serializer.data['content'],  # Content from AboutUs model
            "customerCommentPageResponses": customer_comments_serializer.data,
            "whyUSPageResponses": why_us_serializer.data,
            "siteFeaturePageResponses": site_features_serializer.data,
            "honorPageResponses": honor_serializer.data,
            "statisticPageResponses": statistic_serializer.data,
            "teamPageResponses": team_serializer.data,
            "timeLinePageResponses": timeline_serializer.data,
            "colleaguePageResponses": colleague_serializer.data
        }

        return Response(response_data, status=200)


class PrivacyPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=PrivacyContentSerializer)},
        description="Privacy Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Rule instance
        privacy = Privacy.objects.last()

        if privacy:
            # Serialize only the content field
            serializer = PrivacyContentSerializer(privacy)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "حریم خصوصی یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)


class FaqPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=FaqCategoryPageSerializer)},  # Documenting the response
        description="FAQ Page API"
    )
    def post(self, request):
        # Fetch only categories that are not deleted
        faq_categories = FaqCategory.objects.filter(is_deleted=False)

        # Serialize the categories with their related FAQs
        serializer = FaqCategoryPageSerializer(faq_categories, many=True)

        # Return the response in the desired format
        return Response({"faqCategoryItems": serializer.data})


class HelpPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=HelpCategoryPageSerializer)},  # Documenting the response
        description="Help Page API"
    )
    def post(self, request):
        # Fetch only categories that are not deleted
        help_categories = HelpCategory.objects.filter(is_deleted=False)

        # Serialize the categories with their related FAQs
        serializer = FaqCategoryPageSerializer(help_categories, many=True)

        # Return the response in the desired format
        return Response({"helpCategoryItems": serializer.data})

class BugPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=BugContentSerializer)},
        description="Bug Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Rule instance
        bug = Bug.objects.last()

        if bug:
            # Serialize only the content field
            serializer = PrivacyContentSerializer(bug)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "باگ یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

class CriticismPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=CriticismContentSerializer)},
        description="Criticism Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Rule instance
        criticism = Criticism.objects.last()

        if criticism:
            # Serialize only the content field
            serializer = PrivacyContentSerializer(criticism)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "انتقاد یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

class SuggestionPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=SuggestionContentSerializer)},
        description="Suggestion Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Suggestion instance
        suggestion = Suggestion.objects.last()

        if suggestion:
            # Serialize only the content field
            serializer = SuggestionContentSerializer(suggestion)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "پیشنهاد یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

class ComplaintPageView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses={200: OpenApiResponse(response=ComplaintContentSerializer)},
        description="Complaint Page API"
    )
    def post(self, request, *args, **kwargs):
        # Query the latest non-deleted Complaint instance
        complaint = Complaint.objects.last()

        if complaint:
            # Serialize only the content field
            serializer = ComplaintContentSerializer(complaint)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "شکایت یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

class StaticFormRegisterView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=StaticFormSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update StaticForm"
    )
    def post(self, request):
        static_form_id = request.data.get('id', 0)

        # If static_form_id is 0, it's a new page, so create it
        if static_form_id == 0:
            serializer = StaticFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "فرم استاتیک با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If static_form_id is provided, try to update the existing page
        try:
            static_form = StaticForm.objects.get(pk=static_form_id)
        except StaticForm.DoesNotExist:
            return Response({'message': 'فرم استاتیک مورد نظر برای تغییر یافت نشد.', "id": static_form_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = StaticFormSerializer(static_form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "فرم استاتیک با موفقیت به روزرسانی شد!", "id": static_form_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

