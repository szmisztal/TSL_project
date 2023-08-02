from django_cron import CronJobBase, Schedule
from django.utils import timezone
from.models import TransportationOrder

class DeleteArchivedOrders(CronJobBase):
    RUN_EVERY_MINS = 1440
    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = "logistician_app.delete_archived_orders"

    def do(self):
        one_month_ago = timezone.now() - timezone.timedelta(days = 30)
        TransportationOrder.archived.filter(date__lte = one_month_ago).delete()
