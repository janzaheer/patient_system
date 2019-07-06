import json
import datetime

from calendar import monthrange
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Sum

from ps_com.models import Billing


class DailySalesAPI(View):

    @staticmethod
    def sales_data(obj, date=None, week_date=None, month_date=None):
        bill_amount = obj.aggregate(
            total_bill=Sum('amount')
        )
        total_bill = (
            int(bill_amount.get('total_bill')) if
            bill_amount.get('total_bill') else 0
        )
        bill_discount = obj.aggregate(
            total_discount=Sum('discount')
        )

        total_discount = (
            int(bill_discount.get('total_discount')) if
            bill_discount.get('total_discount') else 0
        )

        total = total_bill - total_discount

        data = {
            'amount': total_bill,
            'discount': total_discount,
            'total': total,
        }

        if week_date:
            data.update({
                'date': week_date.strftime('%a %d, %b')
            })
        elif month_date:
            data.update({
                'day': month_date.strftime('%b')
            })
        else:
            data.update({
                'date': date.strftime('%d-%b-%Y')
            })
        return data

    def get(self, request, *args, **kwargs):
        sales = []
        for day in range(12):
            sales_day = timezone.now() - relativedelta(days=day)
            billing = Billing.objects.filter(
                billing_date__icontains=sales_day.date()
            )

            data = self.sales_data(
                obj=billing, date=sales_day
            )
            sales.append(data)

        return JsonResponse(
            {'bill_data': sales}
        )


class MonthlySalesAPI(DailySalesAPI):
    def get(self, request, *args, **kwargs):
        sales = []

        for month in range(12):
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            billing = Billing.objects.filter(
                billing_date__gte=start_month,
                billing_date__lt=end_month.replace(
                        hour=23, minute=59, second=59)
            )

            data = self.sales_data(
                obj=billing, month_date=end_month
            )
            sales.append(data)

        return JsonResponse(
            {'bill_data': sales}
        )
