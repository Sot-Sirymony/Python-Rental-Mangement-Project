# from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QWidget
# from controllers.tenant_report_controller import TenantReportController
# from PyQt6.QtGui import QPixmap

# class TenantReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.controller = TenantReportController()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Tenant Summary Report
#         summary_label = QLabel("Tenant Summary Report")
#         summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         layout.addWidget(summary_label)

#         total, active, inactive, overdue = self.controller.get_tenant_summary()
#         layout.addWidget(QLabel(f"Total Tenants: {total}"))
#         layout.addWidget(QLabel(f"Active Tenants: {active}"))
#         layout.addWidget(QLabel(f"Inactive Tenants: {inactive}"))
#         layout.addWidget(QLabel(f"Overdue Payments: {overdue}"))

#         # Generate Visualizations
#         bar_chart_btn = QPushButton("Generate Bar Chart")
#         bar_chart_btn.clicked.connect(self.show_bar_chart)
#         layout.addWidget(bar_chart_btn)

#         pie_chart_btn = QPushButton("Generate Pie Chart")
#         pie_chart_btn.clicked.connect(self.show_pie_chart)
#         layout.addWidget(pie_chart_btn)

#         # Payment Report
#         payment_report_btn = QPushButton("Show Tenant Payment Report")
#         payment_report_btn.clicked.connect(self.show_payment_report)
#         layout.addWidget(payment_report_btn)

#         self.setLayout(layout)

#     def show_bar_chart(self):
#         total, active, inactive, _ = self.controller.get_tenant_summary()
#         self.controller.generate_bar_chart(active, inactive)
#         bar_chart = QLabel()
#         bar_chart.setPixmap(QPixmap("tenant_summary_bar_chart.png"))
#         self.layout().addWidget(bar_chart)

#     def show_pie_chart(self):
#         total, active, inactive, _ = self.controller.get_tenant_summary()
#         self.controller.generate_pie_chart(active, inactive)
#         pie_chart = QLabel()
#         pie_chart.setPixmap(QPixmap("tenant_summary_pie_chart.png"))
#         self.layout().addWidget(pie_chart)

#     def show_payment_report(self):
#         payment_data = self.controller.get_tenant_payment_report()
#         self.controller.generate_payment_bar_chart(payment_data)

#         payment_table = QTableWidget()
#         payment_table.setRowCount(len(payment_data))
#         payment_table.setColumnCount(2)
#         payment_table.setHorizontalHeaderLabels(["Tenant ID", "Total Payments"])

#         for row, data in enumerate(payment_data.values):
#             payment_table.setItem(row, 0, QTableWidgetItem(str(data[0])))
#             payment_table.setItem(row, 1, QTableWidgetItem(f"${data[1]:.2f}"))

#         self.layout().addWidget(payment_table)








# from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QWidget
# from controllers.tenant_report_controller import TenantReportController
# from PyQt6.QtGui import QPixmap
# import os

# class TenantReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         print("Initializing TenantReportView")  # Debug print
#         self.controller = TenantReportController()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Tenant Summary Report
#         summary_label = QLabel("Tenant Summary Report")
#         summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         layout.addWidget(summary_label)

#         try:
#             total, active, inactive, overdue = self.controller.get_tenant_summary()
#             print(f"Tenant Summary: Total={total}, Active={active}, Inactive={inactive}, Overdue={overdue}")  # Debug print
#             layout.addWidget(QLabel(f"Total Tenants: {total}"))
#             layout.addWidget(QLabel(f"Active Tenants: {active}"))
#             layout.addWidget(QLabel(f"Inactive Tenants: {inactive}"))
#             layout.addWidget(QLabel(f"Overdue Payments: {overdue}"))
#         except Exception as e:
#             print(f"Error fetching tenant summary: {e}")  # Debug print
#             layout.addWidget(QLabel("Error fetching tenant summary."))

#         # Generate Visualizations
#         bar_chart_btn = QPushButton("Generate Bar Chart")
#         bar_chart_btn.clicked.connect(self.show_bar_chart)
#         layout.addWidget(bar_chart_btn)

#         pie_chart_btn = QPushButton("Generate Pie Chart")
#         pie_chart_btn.clicked.connect(self.show_pie_chart)
#         layout.addWidget(pie_chart_btn)

#         # Payment Report
#         payment_report_btn = QPushButton("Show Tenant Payment Report")
#         payment_report_btn.clicked.connect(self.show_payment_report)
#         layout.addWidget(payment_report_btn)

#         self.setLayout(layout)

#     def show_bar_chart(self):
#         print("Generating bar chart...")  # Debug print
#         self.clear_charts()
#         try:
#             total, active, inactive, _ = self.controller.get_tenant_summary()
#             print(f"Bar Chart Data: Active={active}, Inactive={inactive}")  # Debug print
#             chart_path = self.controller.generate_bar_chart(active, inactive)
#             if not os.path.exists(chart_path):
#                 print(f"Error: Bar chart file not found at {chart_path}")  # Debug print
#                 return

#             bar_chart = QLabel()
#             bar_chart.setPixmap(QPixmap(chart_path))
#             self.layout().addWidget(bar_chart)
#             print(f"Bar chart displayed from: {chart_path}")  # Debug print
#         except Exception as e:
#             print(f"Error generating bar chart: {e}")  # Debug print

#     def show_pie_chart(self):
#         print("Generating pie chart...")  # Debug print
#         self.clear_charts()
#         try:
#             total, active, inactive, _ = self.controller.get_tenant_summary()
#             print(f"Pie Chart Data: Active={active}, Inactive={inactive}")  # Debug print
#             chart_path = self.controller.generate_pie_chart(active, inactive)
#             if not os.path.exists(chart_path):
#                 print(f"Error: Pie chart file not found at {chart_path}")  # Debug print
#                 return

#             pie_chart = QLabel()
#             pie_chart.setPixmap(QPixmap(chart_path))
#             self.layout().addWidget(pie_chart)
#             print(f"Pie chart displayed from: {chart_path}")  # Debug print
#         except Exception as e:
#             print(f"Error generating pie chart: {e}")  # Debug print

#     def show_payment_report(self):
#         print("Generating payment report...")  # Debug print
#         try:
#             payment_data = self.controller.get_tenant_payment_report()
#             print(f"Raw Payment Data:\n{payment_data}")  # Debug print

#             if payment_data.empty:
#                 print("No payment data available.")  # Debug print
#                 no_data_label = QLabel("No payment data available.")
#                 self.layout().addWidget(no_data_label)
#                 return

#             self.controller.generate_payment_bar_chart(payment_data)
#             print("Payment bar chart generated.")  # Debug print

#             payment_table = QTableWidget()
#             payment_table.setRowCount(len(payment_data))
#             payment_table.setColumnCount(2)
#             payment_table.setHorizontalHeaderLabels(["Tenant ID", "Total Payments"])

#             for row, data in enumerate(payment_data.values):
#                 print(f"Row {row}: Tenant ID={data[0]}, Total Payments={data[1]}")  # Debug each row
#                 payment_table.setItem(row, 0, QTableWidgetItem(str(data[0])))
#                 payment_table.setItem(row, 1, QTableWidgetItem(f"${data[1]:.2f}"))

#             self.layout().addWidget(payment_table)
#             print("Payment report table added to layout.")  # Debug print
#         except Exception as e:
#             print(f"Error generating payment report: {e}")  # Debug print

#     def clear_charts(self):
#         """Clear previous charts from the layout."""
#         print("Clearing old charts from layout...")  # Debug print
#         removed_count = 0
#         for i in reversed(range(self.layout().count())):
#             widget = self.layout().itemAt(i).widget()
#             if isinstance(widget, QLabel) and widget.pixmap():
#                 print(f"Removing chart widget at index {i}.")  # Debug specific widget removal
#                 widget.deleteLater()
#                 removed_count += 1
#         print(f"Cleared {removed_count} chart(s) from layout.")  # Debug print









# from PyQt6.QtWidgets import (
#     QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
#     QTableWidgetItem, QWidget, QMessageBox, QProgressBar, QGroupBox
# )
# from PyQt6.QtGui import QPixmap
# import os
# from controllers.tenant_report_controller import TenantReportController


# class TenantReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         print("Initializing TenantReportView")  # Debug print
#         self.controller = TenantReportController()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Tenant Summary Group
#         summary_group = QGroupBox("Tenant Summary")
#         summary_layout = QVBoxLayout()
#         summary_label = QLabel("Tenant Summary Report")
#         summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         summary_layout.addWidget(summary_label)

#         try:
#             total, active, inactive, overdue = self.controller.get_tenant_summary()
#             print(f"Tenant Summary: Total={total}, Active={active}, Inactive={inactive}, Overdue={overdue}")
#             summary_layout.addWidget(QLabel(f"Total Tenants: {total}"))
#             summary_layout.addWidget(QLabel(f"Active Tenants: {active}"))
#             summary_layout.addWidget(QLabel(f"Inactive Tenants: {inactive}"))
#             summary_layout.addWidget(QLabel(f"Overdue Payments: {overdue}"))
#         except Exception as e:
#             print(f"Error fetching tenant summary: {e}")
#             summary_layout.addWidget(QLabel("Error fetching tenant summary."))
#         summary_group.setLayout(summary_layout)
#         layout.addWidget(summary_group)

#         # Visualization Buttons Group
#         vis_group = QGroupBox("Visualizations")
#         vis_layout = QVBoxLayout()
#         bar_chart_btn = QPushButton("Generate Bar Chart")
#         bar_chart_btn.clicked.connect(self.show_bar_chart)
#         vis_layout.addWidget(bar_chart_btn)

#         pie_chart_btn = QPushButton("Generate Pie Chart")
#         pie_chart_btn.clicked.connect(self.show_pie_chart)
#         vis_layout.addWidget(pie_chart_btn)
#         vis_group.setLayout(vis_layout)
#         layout.addWidget(vis_group)

#         # Payment Report Group
#         report_group = QGroupBox("Payment Report")
#         report_layout = QVBoxLayout()
#         payment_report_btn = QPushButton("Show Tenant Payment Report")
#         payment_report_btn.clicked.connect(self.show_payment_report)
#         report_layout.addWidget(payment_report_btn)

#         export_btn = QPushButton("Export Payment Report")
#         export_btn.clicked.connect(self.export_payment_report)
#         report_layout.addWidget(export_btn)
#         report_group.setLayout(report_layout)
#         layout.addWidget(report_group)

#         # Progress Bar
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setVisible(False)
#         layout.addWidget(self.progress_bar)

#         self.setLayout(layout)

#     def show_bar_chart(self):
#         print("Generating bar chart...")
#         self.start_loading()
#         try:
#             total, active, inactive, _ = self.controller.get_tenant_summary()
#             print(f"Bar Chart Data: Active={active}, Inactive={inactive}")
#             chart_path = self.controller.generate_bar_chart(active, inactive)
#             if not chart_path or not os.path.exists(chart_path):
#                 raise FileNotFoundError(f"Bar chart file not found at {chart_path}")
#             self.display_chart(chart_path, "Bar chart")
#         except Exception as e:
#             print(f"Error generating bar chart: {e}")
#             self.show_error(f"Error generating bar chart: {e}")
#         finally:
#             self.stop_loading()

#     def show_pie_chart(self):
#         print("Generating pie chart...")
#         self.start_loading()
#         try:
#             total, active, inactive, _ = self.controller.get_tenant_summary()
#             print(f"Pie Chart Data: Active={active}, Inactive={inactive}")
#             chart_path = self.controller.generate_pie_chart(active, inactive)
#             if not chart_path or not os.path.exists(chart_path):
#                 raise FileNotFoundError(f"Pie chart file not found at {chart_path}")
#             self.display_chart(chart_path, "Pie chart")
#         except Exception as e:
#             print(f"Error generating pie chart: {e}")
#             self.show_error(f"Error generating pie chart: {e}")
#         finally:
#             self.stop_loading()

#     def display_chart(self, chart_path, chart_type):
#         chart = QLabel()
#         chart.setPixmap(QPixmap(chart_path))
#         self.layout().addWidget(chart)
#         print(f"{chart_type} displayed from: {chart_path}")

#     def show_payment_report(self):
#         print("Generating payment report...")
#         self.start_loading()
#         try:
#             payment_data = self.controller.get_tenant_payment_report()
#             print(f"Raw Payment Data:\n{payment_data}")

#             if payment_data.empty:
#                 raise ValueError("No payment data available.")

#             self.controller.generate_payment_bar_chart(payment_data)
#             print("Payment bar chart generated.")

#             payment_table = QTableWidget()
#             payment_table.setRowCount(len(payment_data))
#             payment_table.setColumnCount(2)
#             payment_table.setHorizontalHeaderLabels(["Tenant ID", "Total Payments"])

#             for row, data in enumerate(payment_data.values):
#                 print(f"Row {row}: Tenant ID={data[0]}, Total Payments={data[1]}")
#                 payment_table.setItem(row, 0, QTableWidgetItem(str(data[0])))
#                 payment_table.setItem(row, 1, QTableWidgetItem(f"${data[1]:.2f}"))

#             self.layout().addWidget(payment_table)
#             print("Payment report table added to layout.")
#         except Exception as e:
#             print(f"Error generating payment report: {e}")
#             self.show_error(f"Error generating payment report: {e}")
#         finally:
#             self.stop_loading()

#     def export_payment_report(self):
#         print("Exporting payment report...")
#         try:
#             payment_data = self.controller.get_tenant_payment_report()
#             if payment_data.empty:
#                 raise ValueError("No payment data to export.")
#             file_path = "reports/tenant_payment_report.csv"
#             payment_data.to_csv(file_path, index=False)
#             print(f"Payment report exported to {file_path}")
#             self.show_error(f"Payment report saved at {file_path}")
#         except Exception as e:
#             print(f"Error exporting payment report: {e}")
#             self.show_error(f"Error exporting payment report: {e}")

#     def show_error(self, message):
#         """Display an error message box."""
#         error_dialog = QMessageBox()
#         error_dialog.setIcon(QMessageBox.Icon.Critical)
#         error_dialog.setWindowTitle("Error")
#         error_dialog.setText(message)
#         error_dialog.exec()

#     def clear_charts(self):
#         """Clear previous charts from the layout."""
#         print("Clearing old charts from layout...")
#         for i in reversed(range(self.layout().count())):
#             widget = self.layout().itemAt(i).widget()
#             if isinstance(widget, QLabel) and widget.pixmap():
#                 widget.deleteLater()
#         print("Charts cleared.")

#     def start_loading(self):
#         self.progress_bar.setVisible(True)
#         self.progress_bar.setValue(0)

#     def stop_loading(self):
#         self.progress_bar.setVisible(False)








from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QWidget, QMessageBox, QProgressBar, QGroupBox,
    QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QAbstractScrollArea
)
from PyQt6.QtGui import QPixmap
import os
from controllers.tenant_report_controller import TenantReportController


class TenantReportView(QWidget):
    def __init__(self):
        super().__init__()
        print("Initializing TenantReportView")  # Debug print
        self.controller = TenantReportController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Scroll Area for the entire content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Tenant Summary Group
        summary_group = QGroupBox("Tenant Summary")
        summary_layout = QVBoxLayout()
        summary_label = QLabel("Tenant Summary Report")
        summary_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        summary_layout.addWidget(summary_label)

        try:
            total, active, inactive, overdue = self.controller.get_tenant_summary()
            print(f"Tenant Summary: Total={total}, Active={active}, Inactive={inactive}, Overdue={overdue}")
            summary_layout.addWidget(QLabel(f"Total Tenants: {total}"))
            summary_layout.addWidget(QLabel(f"Active Tenants: {active}"))
            summary_layout.addWidget(QLabel(f"Inactive Tenants: {inactive}"))
            summary_layout.addWidget(QLabel(f"Overdue Payments: {overdue}"))
        except Exception as e:
            print(f"Error fetching tenant summary: {e}")
            summary_layout.addWidget(QLabel("Error fetching tenant summary."))
        summary_group.setLayout(summary_layout)
        scroll_layout.addWidget(summary_group)

        # Visualization Buttons Group
        vis_group = QGroupBox("Visualizations")
        vis_layout = QVBoxLayout()
        bar_chart_btn = QPushButton("Generate Bar Chart")
        bar_chart_btn.clicked.connect(self.show_bar_chart)
        vis_layout.addWidget(bar_chart_btn)

        pie_chart_btn = QPushButton("Generate Pie Chart")
        pie_chart_btn.clicked.connect(self.show_pie_chart)
        vis_layout.addWidget(pie_chart_btn)
        vis_group.setLayout(vis_layout)
        scroll_layout.addWidget(vis_group)

        # Payment Report Group
        report_group = QGroupBox("Payment Report")
        report_layout = QVBoxLayout()
        payment_report_btn = QPushButton("Show Tenant Payment Report")
        payment_report_btn.clicked.connect(self.show_payment_report)
        report_layout.addWidget(payment_report_btn)

        export_btn = QPushButton("Export Payment Report")
        export_btn.clicked.connect(self.export_payment_report)
        report_layout.addWidget(export_btn)
        report_group.setLayout(report_layout)
        scroll_layout.addWidget(report_group)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        scroll_layout.addWidget(self.progress_bar)

        # Add scrollable widget to the scroll area
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def show_bar_chart(self):
        print("Generating bar chart...")
        self.start_loading()
        try:
            total, active, inactive, _ = self.controller.get_tenant_summary()
            print(f"Bar Chart Data: Active={active}, Inactive={inactive}")
            chart_path = self.controller.generate_bar_chart(active, inactive)
            if not chart_path or not os.path.exists(chart_path):
                raise FileNotFoundError(f"Bar chart file not found at {chart_path}")
            self.display_scrollable_chart(chart_path, "Bar chart")
        except Exception as e:
            print(f"Error generating bar chart: {e}")
            self.show_error(f"Error generating bar chart: {e}")
        finally:
            self.stop_loading()

    def show_pie_chart(self):
        print("Generating pie chart...")
        self.start_loading()
        try:
            total, active, inactive, _ = self.controller.get_tenant_summary()
            print(f"Pie Chart Data: Active={active}, Inactive={inactive}")
            chart_path = self.controller.generate_pie_chart(active, inactive)
            if not chart_path or not os.path.exists(chart_path):
                raise FileNotFoundError(f"Pie chart file not found at {chart_path}")
            self.display_scrollable_chart(chart_path, "Pie chart")
        except Exception as e:
            print(f"Error generating pie chart: {e}")
            self.show_error(f"Error generating pie chart: {e}")
        finally:
            self.stop_loading()

    def display_scrollable_chart(self, chart_path, chart_type):
        """Display a chart with scrollable view."""
        print(f"Displaying scrollable {chart_type} from: {chart_path}")
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(QPixmap(chart_path))
        scene.addItem(pixmap_item)

        graphics_view = QGraphicsView()
        graphics_view.setScene(scene)
        graphics_view.setHorizontalScrollBarPolicy(QAbstractScrollArea.ScrollBarPolicy.ScrollBarAsNeeded)
        graphics_view.setVerticalScrollBarPolicy(QAbstractScrollArea.ScrollBarPolicy.ScrollBarAsNeeded)

        self.layout().addWidget(graphics_view)
        print(f"Scrollable {chart_type} added to layout.")

    def show_payment_report(self):
        # Implementation for showing the payment report...
        pass

    def export_payment_report(self):
        # Implementation for exporting the payment report...
        pass

    def show_error(self, message):
        """Display an error message box."""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec()

    def clear_charts(self):
        """Clear previous charts from the layout."""
        print("Clearing old charts from layout...")
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.pixmap():
                widget.deleteLater()
        print("Charts cleared.")

    def start_loading(self):
        self.progress_bar.setVisible(True)
        self.pro
