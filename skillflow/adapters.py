from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def get_client_ip(self, request):
        ip = request.META.get('HTTP_X_REAL_IP')
        if not ip:
            forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            ip = forwarded_for.split(',')[0].strip() or None
        return ip or request.META.get('REMOTE_ADDR')
