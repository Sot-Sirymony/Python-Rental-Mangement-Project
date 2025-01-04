
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.room_report_controller import fetch_room_summary, fetch_occupancy_analysis, fetch_financial_performance
import pandas as pd

class RoomReport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Report")
        self.layout = QVBoxLayout()
        
        # Filter and Actions
        filter_layout = QHBoxLayout()
        self.report_type_selector = QComboBox()
        self.report_type_selector.addItems(["Room Summary", "Occupancy Analysis", "Financial Performance"])
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        filter_layout.addWidget(QLabel("Select Report:"))
        filter_layout.addWidget(self.report_type_selector)
        filter_layout.addWidget(self.generate_btn)
        self.layout.addLayout(filter_layout)

        # Table for displaying data
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Canvas for Matplotlib graphs
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        print("RoomReport initialized")  # Debug print

    def generate_report(self):
        """Generate the selected report."""
        report_type = self.report_type_selector.currentText()
        print(f"Report type selected: {report_type}")  # Debug print

        if report_type == "Room Summary":
            self.show_room_summary()
        elif report_type == "Occupancy Analysis":
            self.show_occupancy_analysis()
        elif report_type == "Financial Performance":
            self.show_financial_performance()

    def show_room_summary(self):
        """Display room summary in the table."""
        df = fetch_room_summary()
        print(f"Room Summary Data: \n{df}")  # Debug print
        self.populate_table(df)

    def show_occupancy_analysis(self):
        """Display occupancy analysis with a pie chart."""
        df = fetch_occupancy_analysis()
        print(f"Occupancy Analysis Data: \n{df}")  # Debug print
        self.populate_table(df)

        # Plot pie chart
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.pie(df['count'], labels=df['occupancy_status'], autopct='%1.1f%%', startangle=140)
        ax.set_title("Occupancy Analysis")
        self.canvas.draw()
        print("Pie chart drawn")  # Debug print

    def show_financial_performance(self):
        """Display financial performance in the table and bar chart."""
        df = fetch_financial_performance()
        print(f"Financial Performance Data: \n{df}")  # Debug print
        self.populate_table(df)

        # Ensure no None values for plotting
        df['total_income'] = df['total_income'].fillna(0)
        df['outstanding'] = df['outstanding'].fillna(0)

        # Plot bar chart
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.bar(df['name'], df['total_income'], label='Total Income')
        ax.bar(df['name'], df['outstanding'], bottom=df['total_income'], label='Outstanding', color='red')
        ax.set_xlabel("Rooms")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Financial Performance by Room")
        ax.legend()
        self.canvas.draw()
        print("Bar chart drawn")  # Debug print

    def populate_table(self, df: pd.DataFrame):
        """Populate the table with DataFrame data, ensuring that None values are handled."""
        df = df.fillna('N/A')  # Replace None with 'N/A' for display purposes
        self.table.setRowCount(0)
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for row_idx, row_data in df.iterrows():
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        print("Table populated with data")  # Debug print
