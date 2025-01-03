import pandas as pd
from matplotlib import pyplot as plt
#from database import fetch_payment_data, fetch_tenant_data, fetch_room_data  # Assume these fetch data from the database
from controllers.payment_management_controller import fetch_payment_data;
from controllers.tenant_controller import fetch_tenant_data;
from controllers.room_controller import fetch_room_data;
class PaymentReportController:
    def __init__(self):
        self.payment_data = pd.DataFrame(fetch_payment_data())
        self.tenant_data = pd.DataFrame(fetch_tenant_data())
        self.room_data = pd.DataFrame(fetch_room_data())

    def get_payment_summary(self):
        total_payments = len(self.payment_data)
        total_income = self.payment_data['amount_paid'].sum()
        outstanding_balances = self.payment_data['outstanding_balance'].sum()
        overdue_payments = self.payment_data[self.payment_data['status'] == 'Overdue']

        return {
            "total_payments": total_payments,
            "total_income": total_income,
            "outstanding_balances": outstanding_balances,
            "overdue_count": len(overdue_payments),
            "overdue_total": overdue_payments['amount_paid'].sum()
        }

    def generate_status_pie_chart(self):
        status_counts = self.payment_data['status'].value_counts()
        plt.pie(
            status_counts,
            labels=status_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=['green', 'orange', 'red']
        )
        plt.title("Payment Status Breakdown")
        plt.savefig("payment_status_pie_chart.png")
        plt.close()

    def generate_revenue_by_room_chart(self):
        revenue_by_room = self.payment_data.groupby('room_id')['amount_paid'].sum().reset_index()
        revenue_by_room.columns = ['Room ID', 'Total Revenue']

        plt.bar(revenue_by_room['Room ID'], revenue_by_room['Total Revenue'], color='blue')
        plt.title("Revenue Contribution by Room")
        plt.xlabel("Room ID")
        plt.ylabel("Total Revenue")
        plt.savefig("revenue_by_room_bar_chart.png")
        plt.close()

    def generate_monthly_trends_line_chart(self):
        self.payment_data['payment_date'] = pd.to_datetime(self.payment_data['payment_date'])
        monthly_trends = self.payment_data.groupby(self.payment_data['payment_date'].dt.to_period('M'))['amount_paid'].sum()

        monthly_trends.plot(kind='line', marker='o', color='purple')
        plt.title("Monthly Payment Trends")
        plt.xlabel("Month")
        plt.ylabel("Total Payments")
        plt.xticks(rotation=45)
        plt.savefig("monthly_trends_line_chart.png")
        plt.close()
