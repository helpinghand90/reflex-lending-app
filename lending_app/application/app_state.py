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
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        
    ...