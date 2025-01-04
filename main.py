
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QDockWidget
)
from views.RoomModule.room_management import RoomManagement
from views.TenantModule.tenant_management import TenantManagement
from views.PaymentModule.payment_management import PaymentManagement
from views.LeaseModule.lease_management import LeaseManagement
from views.Reports.room_report import RoomReport
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Rental Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize Views
        self.room_management = RoomManagement()
        self.tenant_management = TenantManagement()
        self.lease_management = LeaseManagement()
        self.payment_management = PaymentManagement()
        self.room_report = RoomReport()

        # Add Views to Stack
        self.central_widget.addWidget(self.room_management)
        self.central_widget.addWidget(self.tenant_management)
        self.central_widget.addWidget(self.lease_management)
        self.central_widget.addWidget(self.payment_management)
        self.central_widget.addWidget(self.room_report)

        # Sidebar Navigation
        self.init_sidebar()

    def init_sidebar(self):
        sidebar = QDockWidget("Navigation", self)
        container = QWidget()
        layout = QVBoxLayout()

        # Helper function to create styled buttons
        def create_button(label, on_click):
            btn = QPushButton(label)
            btn.clicked.connect(on_click)
            btn.setMinimumHeight(50)  # Set a larger height
            btn.setMinimumWidth(200)  # Optional: Set a larger width
            btn.setStyleSheet("font-size: 16px;")
            return btn

        # Create buttons for each module and report
        property_room_btn = create_button("Rooms Module", lambda: self.central_widget.setCurrentWidget(self.room_management))
        tenant_btn = create_button("Tenants Module", lambda: self.central_widget.setCurrentWidget(self.tenant_management))
        lease_btn = create_button("Lease Module", lambda: self.central_widget.setCurrentWidget(self.lease_management))
        payment_btn = create_button("Payments Module", lambda: self.central_widget.setCurrentWidget(self.payment_management))
        room_report_btn = create_button("Room Report", lambda: self.central_widget.setCurrentWidget(self.room_report))

        # Add buttons to the layout
        #for btn in [dashboard_btn, property_room_btn, tenant_btn, lease_btn, payment_btn, room_report_btn, tenant_report_btn, lease_report_btn, payment_report_btn]:
        for btn in [ property_room_btn, tenant_btn, lease_btn, payment_btn, room_report_btn]:
        
            layout.addWidget(btn)
 
        container.setLayout(layout)
        sidebar.setWidget(container)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



