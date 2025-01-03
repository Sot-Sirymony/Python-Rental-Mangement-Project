# from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QTableWidget, QTableWidgetItem
# from PyQt6.QtGui import QPixmap
# from controllers.lease_report_controller import LeaseReportController

# class LeaseReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.controller = LeaseReportController()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Lease Summary
#         summary_label = QLabel("Lease Summary Report")
#         summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         layout.addWidget(summary_label)

#         summary = self.controller.get_lease_summary()
#         layout.addWidget(QLabel(f"Total Leases: {summary['total_leases']}"))
#         layout.addWidget(QLabel(f"Active Leases: {summary['active_leases']}"))
#         layout.addWidget(QLabel(f"Completed Leases: {summary['completed_leases']}"))
#         layout.addWidget(QLabel(f"Canceled Leases: {summary['canceled_leases']}"))
#         layout.addWidget(QLabel(f"Occupancy Rate: {summary['occupancy_rate']:.2f}%"))

#         # Generate Visualizations
#         pie_chart_btn = QPushButton("Generate Lease Status Pie Chart")
#         pie_chart_btn.clicked.connect(self.show_pie_chart)
#         layout.addWidget(pie_chart_btn)

#         bar_chart_btn = QPushButton("Generate Room Revenue Bar Chart")
#         bar_chart_btn.clicked.connect(self.show_bar_chart)
#         layout.addWidget(bar_chart_btn)

#         histogram_btn = QPushButton("Generate Lease Duration Histogram")
#         histogram_btn.clicked.connect(self.show_histogram)
#         layout.addWidget(histogram_btn)

#         self.setLayout(layout)

#     def show_pie_chart(self):
#         self.controller.generate_status_pie_chart()
#         pie_chart = QLabel()
#         pie_chart.setPixmap(QPixmap("lease_status_pie_chart.png"))
#         self.layout().addWidget(pie_chart)

#     def show_bar_chart(self):
#         self.controller.generate_revenue_bar_chart()
#         bar_chart = QLabel()
#         bar_chart.setPixmap(QPixmap("room_revenue_bar_chart.png"))
#         self.layout().addWidget(bar_chart)

#     def show_histogram(self):
#         self.controller.generate_lease_duration_histogram()
#         histogram = QLabel()
#         histogram.setPixmap(QPixmap("lease_duration_histogram.png"))
#         self.layout().addWidget(histogram)
