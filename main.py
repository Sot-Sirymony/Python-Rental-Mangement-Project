

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QHeaderView, QWidget, QPushButton, QDockWidget
)
from views.dashboard import Dashboard  # Main dashboard
from views.property_room import PropertyRoomManagement
from views.rental_management import RentalManagement
from views.tenant_management import TenantManagement
from views.payment import PaymentManagement
from views.booking_management import BookingManagement  # Import Booking Management


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Rental Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize Views
        self.dashboard = Dashboard()
        self.property_room_management = PropertyRoomManagement()
        self.tenant_management = TenantManagement()
        self.rental_management = RentalManagement()
        self.payment_management = PaymentManagement()
        self.booking_management = BookingManagement()  # Initialize Booking Management
        self.reports = Dashboard()

        # Add Views to Stack
        self.central_widget.addWidget(self.dashboard)
        self.central_widget.addWidget(self.property_room_management)
        self.central_widget.addWidget(self.tenant_management)
        self.central_widget.addWidget(self.rental_management)
        self.central_widget.addWidget(self.payment_management)
        self.central_widget.addWidget(self.booking_management)  # Add Booking Management to stack
        self.central_widget.addWidget(self.reports)

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
            btn.setStyleSheet("font-size: 16px;")  # Adjust font size
            return btn

        # Create buttons with larger sizes
        dashboard_btn = create_button("Dashboard", lambda: self.central_widget.setCurrentWidget(self.dashboard))
        property_room_btn = create_button("Properties & Rooms", lambda: self.central_widget.setCurrentWidget(self.property_room_management))
        tenant_btn = create_button("Tenants", lambda: self.central_widget.setCurrentWidget(self.tenant_management))
        rental_btn = create_button("Rental Management", lambda: self.central_widget.setCurrentWidget(self.rental_management))
        payment_btn = create_button("Payments", lambda: self.central_widget.setCurrentWidget(self.payment_management))
        booking_btn = create_button("Bookings", lambda: self.central_widget.setCurrentWidget(self.booking_management))  # Booking Button
        reports_btn = create_button("Reports", lambda: self.central_widget.setCurrentWidget(self.reports))

        # Add buttons to the layout
        for btn in [dashboard_btn, property_room_btn, tenant_btn, rental_btn, payment_btn, booking_btn, reports_btn]:
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

