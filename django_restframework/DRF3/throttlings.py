from rest_framework.throttling import SimpleRateThrottle


class TenPerMinuteThrottle(SimpleRateThrottle):
    rate = '10/m'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
