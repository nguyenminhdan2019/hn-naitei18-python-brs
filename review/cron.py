from django.core.mail import send_mail
import environ
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext as _
from django.utils import translation
from dateutil.relativedelta import relativedelta
from .models import (
    Request,
    Rating,
  )
env = environ.Env()
# reading .env file
environ.Env.read_env()

def send_mail_cron_job():
  now = datetime.now()
  now = now + relativedelta(months=-1)
  num_review = Rating.objects.filter(date_added__year=now.year, date_added__month=now.month).count()
  num_request = Request.objects.filter(date_added__year=now.year, date_added__month=now.month).count()
  num_user = User.objects.filter(date_joined__year=now.year, date_joined__month=now.month).count()
  mail_subject = _('Monthly statistics')
  active_user = _('Total active users in month')
  request = _('Total requests in month')
  reviewings = _('Total reviewings in month')
  send_mail(
    subject= mail_subject,
    message='%s: %s\n%s: %s\n%s: %s' % (active_user, num_user, request, num_request,reviewings, num_review),
    from_email = env('EMAIL_HOST_USER'),
    recipient_list = [env('EMAIL_ADMIN'), ],
  )
