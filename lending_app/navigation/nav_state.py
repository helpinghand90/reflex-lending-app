import reflex as rx

from . import routes
from lending_app.auth.auth_state import AuthState


class NavState(AuthState):
    def to_home(self):
        """
        on_click event
        """
        return rx.redirect(routes.HOME_ROUTE)
    
    def to_about_us(self):
        """
        on_click event
        """
        return rx.redirect(routes.ABOUT_US_ROUTE)

    def to_chat(self):
        return rx.redirect(routes.CHAT_ROUTE)
    
    
    def to_app(self):
        return rx.redirect(routes.APPLICATION_ROUTE)