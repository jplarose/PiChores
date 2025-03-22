from PyQt5.QtWidgets import QStackedWidget

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
            print(f"Page '{page_name}' not found!")
