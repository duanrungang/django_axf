
from rest_framework.routers import SimpleRouter

from users.views import AuthView

router = SimpleRouter()
router.register('auth', AuthView)

urlpatterns = router.urls
