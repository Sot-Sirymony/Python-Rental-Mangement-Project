# import pandas as pd
# from matplotlib import pyplot as plt 
# from controllers.tenant_controller import fetch_tenant_data
# from controllers.payment_management_controller import fetch_payment_data
# from controllers.lease_management_controller import fetch_lease_data
# # Assume database functions
# class TenantReportController:
#     def __init__(self):
#         self.tenant_data = pd.DataFrame(fetch_tenant_data())  # Fetch tenant data from DB
#         self.payment_data = pd.DataFrame(fetch_payment_data())  # Fetch payment data
#         self.lease_data = pd.DataFrame(fetch_lease_data())  # Fetch lease data
    
#     def get_tenant_summary(self):
#         total_tenants = len(self.tenant_data)
        
#         # Ensure 'tenant_id' exists in lease_data before proceeding
#         if 'tenant_id' in self.lease_data.columns:
#             active_tenants = len(self.lease_data[self.lease_data['status'] == 'Active']['tenant_id'].unique())
#         else:
#             active_tenants = 0  # Handle case where 'tenant_id' does not exist

#         inactive_tenants = total_tenants - active_tenants
        
#         # Ensure 'tenant_id' exists in payment_data before proceeding
#         if 'tenant_id' in self.payment_data.columns:
#             overdue_tenants = len(self.payment_data[self.payment_data['status'] == 'Overdue']['tenant_id'].unique())
#         else:
#             overdue_tenants = 0  # Handle case where 'tenant_id' does not exist
        
#         return total_tenants, active_tenants, inactive_tenants, overdue_tenants


#     def generate_bar_chart(self, active, inactive):
#         labels = ['Active Tenants', 'Inactive Tenants']
#         values = [active, inactive]
#         plt.bar(labels, values, color=['green', 'red'])
#         plt.title("Active vs. Inactive Tenants")
#         plt.ylabel("Number of Tenants")
#         plt.savefig("tenant_summary_bar_chart.png")  # Save chart as an image
#         plt.close()

#     def generate_pie_chart(self, active, inactive):
#         labels = ['Active Tenants', 'Inactive Tenants']
#         values = [active, inactive]
#         plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
#         plt.title("Tenant Status Distribution")
#         plt.savefig("tenant_summary_pie_chart.png")
#         plt.close()

#     def get_tenant_payment_report(self):
#         payments = self.payment_data.groupby('tenant_id')['amount'].sum().reset_index()
#         payments.columns = ['Tenant ID', 'Total Payments']
#         return payments.sort_values(by='Total Payments', ascending=False)

#     def generate_payment_bar_chart(self, payment_data):
#         top_tenants = payment_data.head(10)  # Top 10 tenants by total payments
#         plt.barh(top_tenants['Tenant ID'], top_tenants['Total Payments'], color='blue')
#         plt.title("Top 10 Tenants by Payments")
#         plt.xlabel("Total Payments")
#         plt.ylabel("Tenant ID")
#         plt.savefig("tenant_payment_bar_chart.png")
#         plt.close()



import pandas as pd
from matplotlib import pyplot as plt
from controllers.tenant_controller import fetch_tenant_data
from controllers.payment_management_controller import fetch_payment_data
from controllers.lease_management_controller import fetch_lease_data
import os

class TenantReportController:
    def __init__(self):
        try:
            self.tenant_data = pd.DataFrame(fetch_tenant_data())  # Fetch tenant data from DB
            self.payment_data = pd.DataFrame(fetch_payment_data())  # Fetch payment data
            self.lease_data = pd.DataFrame(fetch_lease_data())  # Fetch lease data
            print("TenantReportController initialized.")  # Debug print
        except Exception as e:
            print(f"Error initializing TenantReportController: {e}")  # Debug print
            self.tenant_data = pd.DataFrame()
            self.payment_data = pd.DataFrame()
            self.lease_data = pd.DataFrame()

    def get_tenant_summary(self):
        """Generate tenant summary: total, active, inactive, overdue."""
        try:
            total_tenants = len(self.tenant_data)
            active_tenants = (
                len(self.lease_data[self.lease_data['status'] == 'Active']['tenant_id'].unique())
                if 'tenant_id' in self.lease_data.columns else 0
            )
            inactive_tenants = total_tenants - active_tenants
            overdue_tenants = (
                len(self.payment_data[self.payment_data['status'] == 'Overdue']['tenant_id'].unique())
                if 'tenant_id' in self.payment_data.columns else 0
            )
            print(f"Tenant Summary: Total={total_tenants}, Active={active_tenants}, Inactive={inactive_tenants}, Overdue={overdue_tenants}")  # Debug print
            return total_tenants, active_tenants, inactive_tenants, overdue_tenants
        except Exception as e:
            print(f"Error in get_tenant_summary: {e}")  # Debug print
            return 0, 0, 0, 0

    def generate_bar_chart(self, active, inactive):
        """Generate a bar chart for active and inactive tenants."""
        try:
            labels = ['Active Tenants', 'Inactive Tenants']
            values = [active, inactive]
            os.makedirs("reports", exist_ok=True)
            chart_path = "reports/tenant_summary_bar_chart.png"
            plt.bar(labels, values, color=['green', 'red'])
            plt.title("Active vs. Inactive Tenants")
            plt.ylabel("Number of Tenants")
            plt.savefig(chart_path)
            plt.close()
            print(f"Bar chart saved at {chart_path}")  # Debug print
            return chart_path
        except Exception as e:
            print(f"Error in generate_bar_chart: {e}")  # Debug print
            return None

    def generate_pie_chart(self, active, inactive):
        """Generate a pie chart for active and inactive tenants."""
        try:
            labels = ['Active Tenants', 'Inactive Tenants']
            values = [active, inactive]
            os.makedirs("reports", exist_ok=True)
            chart_path = "reports/tenant_summary_pie_chart.png"
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
            plt.title("Tenant Status Distribution")
            plt.savefig(chart_path)
            plt.close()
            print(f"Pie chart saved at {chart_path}")  # Debug print
            return chart_path
        except Exception as e:
            print(f"Error in generate_pie_chart: {e}")  # Debug print
            return None

    def get_tenant_payment_report(self):
        """Generate a payment report for tenants."""
        try:
            if 'amount' not in self.payment_data.columns:
                raise KeyError("Column 'amount' not found in payment data.")
            payments = self.payment_data.groupby('tenant_id')['amount'].sum().reset_index()
            payments.columns = ['Tenant ID', 'Total Payments']
            print(f"Generated tenant payment report:\n{payments}")  # Debug print
            return payments.sort_values(by='Total Payments', ascending=False)
        except Exception as e:
            print(f"Error in get_tenant_payment_report: {e}")  # Debug print
            return pd.DataFrame()

    def generate_payment_bar_chart(self, payment_data):
        """Generate a bar chart for tenant payments."""
        try:
            top_tenants = payment_data.head(10)  # Top 10 tenants by total payments
            os.makedirs("reports", exist_ok=True)
            chart_path = "reports/tenant_payment_bar_chart.png"
            plt.barh(top_tenants['Tenant ID'], top_tenants['Total Payments'], color='blue')
            plt.title("Top 10 Tenants by Payments")
            plt.xlabel("Total Payments")
            plt.ylabel("Tenant ID")
            plt.savefig(chart_path)
            plt.close()
            print(f"Payment bar chart saved at {chart_path}")  # Debug print
            return chart_path
        except Exception as e:
            print(f"Error in generate_payment_bar_chart: {e}")  # Debug print
            return None

