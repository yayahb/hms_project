from django_cron import CronJobBase, Schedule
from .models import ServiceReservation
from django.utils import timezone
from .models import Reservation






class DeleteExpiredReservations(CronJobBase):
    RUN_EVERY_MINS = 60  # Run the cron job every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reservation.delete_expired_reservations'  # A unique code for the cron job

    def do(self):
        now = timezone.now()
        expired_room_reservations = Reservation.objects.filter(end_date__lt=now.date(), end_time__lt=now.time())
        expired_service_reservations = ServiceReservation.objects.filter(reservation_date__lt=now.date(), reservation_time__lt=now.time())
        expired_room_reservations.delete()
        expired_service_reservations.delete()