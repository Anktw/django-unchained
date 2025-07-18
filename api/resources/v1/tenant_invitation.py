import logging
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from django.conf import settings
from api.resources.decorators import tenant_admin_api
import os
from core import models
from api import serializers
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mass_mail
from rest_framework.permissions import AllowAny


logger = logging.getLogger(__name__)

class TenantInvitationCodeListView(APIView, api_settings.DEFAULT_PAGINATION_CLASS):
    BASE_URL = os.path.join(settings.APP_DOMAIN, 'auth/invite/')

    @tenant_admin_api
    def get(self, request, tenant_user, domain):
        query = models.TenantInvitationCode.objects.filter(tenant_id=tenant_user.tenant.id)

        search = request.query_params.get('search')
        if (search is not None) and (len(search.strip(' ')) > 0):
            query = self.filter_by_search_text(search, query)

        page = self.paginate_queryset(query, request)
        serializer = serializers.TenantInvitationCodeSerializer(page, many=True)

        ret = dict(results=serializer.data, count=self.page.paginator.count)
        return Response(ret, status=status.HTTP_200_OK)
    
    
    @tenant_admin_api
    def post(self, request, tenant_user, domain):
        serializer = serializers.TenantInvitationCodeSerializer(
        data=request.data, tenant_user=tenant_user,
        many=isinstance(request.data, list),
        extra_request=dict(tenant_id=tenant_user.tenant.id))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.send_invitation_code(
        tenant=tenant_user.tenant, sender=tenant_user,
        data=serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_invitation_code(self, tenant, sender, data):
        emails = [d['email'] for d in data]
        codes = [d['invitation_code'] for d in data]
        emails, codes = self.drop_existing_tenant_users(tenant_id=tenant.id, emails=emails, codes=codes)
        mass_messages = tuple()
        for email, code in zip(emails, codes):
            mass_messages = mass_messages + (self.get_email_message(tenant=tenant, sender=sender, email=email, code=code),)

        send_mass_mail(mass_messages, fail_silently=False)

    def get_email_message(self, tenant, sender, email, code):
        url = self.BASE_URL.rstrip('/') + f'/{code}'
        subject = (f'{sender.user.first_name} {sender.user.last_name} '
                   f'has invited you to join the workspace in '
                   f'{settings.APP_NAME}')
        body = (f'{sender.user.first_name} {sender.user.last_name}'
                f'({sender.user.email}) has invited you({email}) to join '
                f'{tenant.name} in {settings.APP_NAME}.\n'
                f'If you accept the request, click the following URL.\n\n'
                f'{url}\n\n'
                f'Note that the above invitation link expires in '
                f'{settings.TENANT_INVITATION_CODE_LIFETIME_MINS} minutes.\n')
        from_email = settings.EMAIL_HOST_USER
        return (subject, body, from_email, [email],)
    
    def drop_existing_tenant_users(self, tenant_id, emails, codes):
        filtered_emails = []
        filtered_codes = []
        for email, code in zip(emails, codes):
            query = models.TenantUser.objects.filter(tenant_id=tenant_id, user__email=email)
            if not query.exists():
                filtered_emails.append(email)
                filtered_codes.append(code)

        return filtered_emails, filtered_codes

class TenantInvitationCodeView(APIView):
    @tenant_admin_api
    def delete(self, request, tenant_user, domain, invitation_code_id):
        obj = models.TenantInvitationCode.objects.get(
        pk=invitation_code_id, tenant_id=tenant_user.tenant.id)
        query = models.TenantInvitationCode.objects.filter(tenant_id=tenant_user.tenant.id, email=obj.email)

        serializer = serializers.TenantInvitationCodeSerializer(query.all(), many=True)
        data = serializer.data
        query.all().delete()
        return Response(data, status.HTTP_200_OK)
    
class InvitedTenantView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.InvitedTenantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the invitation code from validated data
        invitation_code = serializer.validated_data['invitation_code']
        
        # Find the existing invitation code record
        invitation = models.TenantInvitationCode.objects.get(invitation_code=invitation_code)
        
        # Return the tenant information
        tenant_serializer = serializers.TenantSerializer(invitation.tenant_user.tenant)
        return Response(tenant_serializer.data, status=status.HTTP_200_OK)