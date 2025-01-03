# from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget
# from PyQt6.QtGui import QPixmap
# from controllers.payment_report_controller import PaymentReportController

# class PaymentReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.controller = PaymentReportController()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Payment Summary
#         summary_label = QLabel("Payment Summary Report")
#         summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         layout.addWidget(summary_label)

#         summary = self.controller.get_payment_summary()
#         layout.addWidget(QLabel(f"Total Payments: {summary['total_payments']}"))
#         layout.addWidget(QLabel(f"Total Income: ${summary['total_income']:.2f}"))
#         layout.addWidget(QLabel(f"Outstanding Balances: ${summary['outstanding_balances']:.2f}"))
#         layout.addWidget(QLabel(f"Overdue Payments: {summary['overdue_count']} (${summary['overdue_total']:.2f})"))

#         # Generate Visualizations
#         pie_chart_btn = QPushButton("Generate Payment Status Pie Chart")
#         pie_chart_btn.clicked.connect(self.show_pie_chart)
#         layout.addWidget(pie_chart_btn)

#         bar_chart_btn = QPushButton("Generate Revenue by Room Chart")
#         bar_chart_btn.clicked.connect(self.show_bar_chart)
#         layout.addWidget(bar_chart_btn)

#         trends_chart_btn = QPushButton("Generate Monthly Payment Trends Chart")
#         trends_chart_btn.clicked.connect(self.show_line_chart)
#         layout.addWidget(trends_chart_btn)

#         self.setLayout(layout)

#     def show_pie_chart(self):
#         self.controller.generate_status_pie_chart()
#         pie_chart = QLabel()
#         pie_chart.setPixmap(QPixmap("payment_status_pie_chart.png"))
#         self.layout().addWidget(pie_chart)

#     def show_bar_chart(self):
#         self.controller.generate_revenue_by_room_chart()
#         bar_chart = QLabel()
#         bar_chart.setPixmap(QPixmap("revenue_by_room_bar_chart.png"))
#         self.layout().addWidget(bar_chart)

#     def show_line_chart(self):
#         self.controller.generate_monthly_trends_line_chart()
#         line_chart = QLabel()
#         line_chart.setPixmap(QPixmap("monthly_trends_line_chart.png"))
#         self.layout().addWidget(line_chart)
