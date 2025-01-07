# import time
import reflex as rx
import sqlmodel
import logging

from typing import List, Optional

from lending_app.auth.auth_state import AuthState


# class ChatMessage(rx.Base):
#     message: str
#     is_bot: bool = False


class AppState(AuthState):
    app_form_page: int = 0
    form_data: dict = {}

    @rx.event
    def submit_application(self):
        self.app_form_page = 0
        rx.alert("Application submitted!")
        
    ...