# from PyQt6.QtWidgets import (
#     QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem,
#     QPushButton, QWidget, QMessageBox
# )
# from PyQt6.QtCore import Qt
# from controllers.payment_management_controller import (
#     payment_summary_by_tenant, payment_summary_by_room, monthly_yearly_payment_report
# )
# import pandas as pd


# class ReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Payment Reports")
#         self.layout = QVBoxLayout()

#         # Report Type Selector
#         self.report_selector = QComboBox()
#         self.report_selector.addItems([
#             "Payment Summary by Tenant", 
#             "Payment Summary by Room", 
#             "Monthly Payment Report", 
#             "Yearly Payment Report"
#         ])
#         self.report_selector.currentTextChanged.connect(self.load_report)
#         self.layout.addWidget(self.report_selector)

#         # Report Table
#         self.report_table = QTableWidget()
#         self.layout.addWidget(self.report_table)

#         # Export Buttons
#         export_layout = QHBoxLayout()
#         self.export_pdf_btn = QPushButton("Export as PDF")
#         self.export_pdf_btn.clicked.connect(lambda: self.export_report("pdf"))
#         self.export_csv_btn = QPushButton("Export as CSV")
#         self.export_csv_btn.clicked.connect(lambda: self.export_report("csv"))
#         self.export_excel_btn = QPushButton("Export as Excel")
#         self.export_excel_btn.clicked.connect(lambda: self.export_report("excel"))

#         export_layout.addWidget(self.export_pdf_btn)
#         export_layout.addWidget(self.export_csv_btn)
#         export_layout.addWidget(self.export_excel_btn)

#         self.layout.addLayout(export_layout)
#         self.setLayout(self.layout)

#         self.load_report()

#     def load_report(self):
#         """Load the selected report."""
#         report_type = self.report_selector.currentText()
#         if report_type == "Payment Summary by Tenant":
#             data = payment_summary_by_tenant()
#             headers = ["Tenant Name", "Total Paid", "Outstanding Balance", "Overdue"]
#         elif report_type == "Payment Summary by Room":
#             data = payment_summary_by_room()
#             headers = ["Room Name", "Total Collected", "Outstanding Amount"]
#         elif report_type == "Monthly Payment Report":
#             data = monthly_yearly_payment_report("monthly")
#             headers = ["Month", "Total Income", "Overdue"]
#         else:  # Yearly Payment Report
#             data = monthly_yearly_payment_report("yearly")
#             headers = ["Year", "Total Income", "Overdue"]

#         self.populate_table(data, headers)

#     def populate_table(self, data, headers):
#         """Populate the table with report data."""
#         self.report_table.clear()
#         self.report_table.setRowCount(len(data))
#         self.report_table.setColumnCount(len(headers))
#         self.report_table.setHorizontalHeaderLabels(headers)

#         for row_idx, row_data in enumerate(data):
#             for col_idx, value in enumerate(row_data):
#                 item = QTableWidgetItem(str(value))
#                 item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#                 self.report_table.setItem(row_idx, col_idx, item)

#     def export_report(self, file_type):
#         """Export the report to the specified file type."""
#         report_type = self.report_selector.currentText()
#         headers = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
#         data = [
#             [self.report_table.item(row, col).text() for col in range(self.report_table.columnCount())]
#             for row in range(self.report_table.rowCount())
#         ]
#         df = pd.DataFrame(data, columns=headers)

#         try:
#             if file_type == "pdf":
#                 df.to_csv("report.pdf", index=False)
#             elif file_type == "csv":
#                 df.to_csv("report.csv", index=False)
#             elif file_type == "excel":
#                 df.to_excel("report.xlsx", index=False)
#             QMessageBox.information(self, "Success", f"Report exported as {file_type.upper()}.")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to export report: {e}")
