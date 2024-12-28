from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget
import matplotlib
matplotlib.use('QtAgg')  # Explicitly set the backend

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Analytics and Reports"))

        # Report Type Selector
        self.report_selector = QComboBox()
        self.report_selector.addItems(["Rent Collection Report", "Occupancy Rates"])
        self.report_selector.currentIndexChanged.connect(self.update_view)
        layout.addWidget(self.report_selector)

        # Report Table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(5)  # Adjust columns based on the report
        layout.addWidget(self.report_table)

        # Chart View (Matplotlib)
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)

        # Export Button
        export_btn = QPushButton("Export Report")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)

        self.setLayout(layout)

    def update_view(self):
        selected_report = self.report_selector.currentText()
        if selected_report == "Rent Collection Report":
            self.load_rent_collection_report()
        elif selected_report == "Occupancy Rates":
            self.load_occupancy_rates()

    def load_rent_collection_report(self):
        # Mock Data
        data = [("Tenant 1", 50), ("Tenant 2", 30), ("Tenant 3", 20)]
        self.update_chart(data, "Rent Collection Breakdown")

    def load_occupancy_rates(self):
        # Mock Data
        data = [("Property A", 70), ("Property B", 50)]
        self.update_chart(data, "Occupancy Rates Breakdown")

    def update_chart(self, data, title):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        labels, sizes = zip(*data)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title(title)
        self.canvas.draw()

    def export_report(self):
        # Placeholder export functionality
        print("Export Report Triggered")
