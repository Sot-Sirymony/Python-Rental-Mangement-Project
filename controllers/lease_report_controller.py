# import pandas as pd
# from matplotlib import pyplot as plt
# ##import from other
# from controllers.tenant_controller import  fetch_tenant_data  # Assume these fetch data from the database
# from controllers.room_controller import fetch_room_data
# from controllers.lease_management_controller import fetch_lease_data
# class LeaseReportController:
#     def __init__(self):
#         self.lease_data = pd.DataFrame(fetch_lease_data())
#         self.room_data = pd.DataFrame(fetch_room_data())
#         self.tenant_data = pd.DataFrame(fetch_tenant_data())

#     def get_lease_summary(self):
#         total_leases = len(self.lease_data)
#         active_leases = len(self.lease_data[self.lease_data['status'] == 'Active'])
#         completed_leases = len(self.lease_data[self.lease_data['status'] == 'Completed'])
#         canceled_leases = len(self.lease_data[self.lease_data['status'] == 'Canceled'])

#         total_rooms = len(self.room_data)
#         rented_rooms = len(self.lease_data[self.lease_data['status'] == 'Active']['room_id'].unique())
#         occupancy_rate = (rented_rooms / total_rooms) * 100 if total_rooms > 0 else 0

#         return {
#             "total_leases": total_leases,
#             "active_leases": active_leases,
#             "completed_leases": completed_leases,
#             "canceled_leases": canceled_leases,
#             "occupancy_rate": occupancy_rate
#         }

#     def generate_status_pie_chart(self):
#         statuses = self.lease_data['status'].value_counts()
#         labels = statuses.index
#         sizes = statuses.values
#         colors = ['green', 'blue', 'red']

#         plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
#         plt.title("Lease Status Breakdown")
#         plt.savefig("lease_status_pie_chart.png")
#         plt.close()

#     def generate_revenue_bar_chart(self):
#         revenue_by_room = self.lease_data.groupby('room_id')['revenue'].sum().reset_index()
#         revenue_by_room.columns = ['Room ID', 'Total Revenue']

#         plt.bar(revenue_by_room['Room ID'], revenue_by_room['Total Revenue'], color='orange')
#         plt.title("Revenue Contribution by Room")
#         plt.xlabel("Room ID")
#         plt.ylabel("Total Revenue")
#         plt.savefig("room_revenue_bar_chart.png")
#         plt.close()

#     def generate_lease_duration_histogram(self):
#         lease_durations = self.lease_data['duration']
#         plt.hist(lease_durations, bins=10, color='purple')
#         plt.title("Lease Duration Distribution")
#         plt.xlabel("Duration (days)")
#         plt.ylabel("Number of Leases")
#         plt.savefig("lease_duration_histogram.png")
#         plt.close()
