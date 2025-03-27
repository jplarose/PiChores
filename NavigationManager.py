from PyQt5.QtWidgets import QStackedWidget
from database import log_action

class NavigationManager(QStackedWidget):
    """Manages navigation between multiple pages dynamically."""
    
    def __init__(self):
        super().__init__()
        self.pages = {}

    def add_page(self, page_name, page_instance):
        """Adds a new page to the navigation system."""
        self.pages[page_name] = page_instance
        self.addWidget(page_instance)

    def navigate_to(self, page_name, user=None):
        """Passes user data dynamically and switches pages."""
        if page_name in self.pages:
            page = self.pages[page_name]

            # If the page supports dynamic updates, refresh its content
            if hasattr(page, "update_page"):
                page.update_page(user)

            self.setCurrentWidget(page)
        else:
            log_action(user.id if user is not None else 1, f"Page '{page_name}' not found!")

    def navigate_to_chore(self, page_name, user=None, chore=None):
        """Passes user data dynamically and switches pages."""
        if page_name in self.pages:
            page = self.pages[page_name]

            # If the page supports dynamic updates, refresh its content
            if hasattr(page, "update_page"):
                page.update_page(user, chore)

            self.setCurrentWidget(page)
        else:
            log_action(user.id if user is not None else 1, f"Page '{page_name}' not found!")

    def navigate_to_admin(self, page_name, user=None, is_admin=1):
        """Navigation specifically to get to the admin pages"""
        if page_name in self.pages:
            page = self.pages[page_name]

            if hasattr(page, "update_page"):
                page.update_page(user, is_admin)

            self.setCurrentWidget(page)
        else:
            log_action(user.id if user is not None else 1, f"Admin Page '{page_name}' not found!")

    def navigate_to_selected_chore(self, page_name, user=None, selected_date=None):
        """Passes user data dynamically and switches pages."""
        if page_name in self.pages:
            page = self.pages[page_name]

            # If the page supports dynamic updates, refresh its content
            if hasattr(page, "update_page"):
                page.update_page(user, selected_date)

            self.setCurrentWidget(page)
        else:
            log_action(user.id if user is not None else 1, f"Page '{page_name}' not found!")
