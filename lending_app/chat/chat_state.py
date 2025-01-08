# import time
import reflex as rx
import sqlmodel
import logging

from typing import List, Optional

from lending_app.models import ChatSession, ChatSessionMessageModel
from lending_app.auth.auth_state import AuthState

from . import ai


class ChatMessage(rx.Base):
    message: str
    is_bot: bool = False


class ChatState(AuthState):
    chat_session: ChatSession = None
    not_found: Optional[bool] = None
    did_submit: bool = False
    messages: List[ChatMessage] = []
    hist_chat_sessions: List[ChatSession] = []
    session_msg_counter: int = 0

    @rx.var
    def user_did_submit(self) -> bool:
        return self.did_submit

    def get_session_id(self) -> int:
        try:
            my_session_id = int(self.router.page.params.get("session_id"))
        except:
            my_session_id = None
        return my_session_id

    def get_chat_history(self):
        if self.user_id is not None:
            with rx.session() as db_session:
                self.hist_chat_sessions = db_session.query(ChatSession).filter_by(user_id=self.user_id).all()
                logging.info(f"Found {len(self.hist_chat_sessions)} chat sessions for user_id: {self.user_id}")
        else:
                logging.info(
                    f"Chat Session Data Not Fetched, user not logged in"
                )

    def create_new_chat_session(self):
        user_id = self.user_id
        logging.info(f"self.user_id: {user_id}, type: {type(user_id)}")

        data = {"user_id": user_id, "messages": []}

        logging.info(f"chatsession_data_input: {data}, type: {type(data)}")

        with rx.session() as db_session:
            chat_session = ChatSession(**data)
            logging.info(f"Chat Session Data: {chat_session}")
            
            logging.info(f"message_count: {self.session_msg_counter}")

            # add to the session if user is logged in
            if user_id is not None and self.session_msg_counter > 0:
                db_session.add(chat_session)  # prepare to save
                db_session.commit()  # actually save
                db_session.refresh(chat_session)
                logging.info(f"Chat Session Data Logged: {chat_session}")
            else:
                logging.info(
                    f"Chat Session Data Not Logged, user not logged in: {chat_session}"
                )

            self.chat_session = chat_session
            self.session_msg_counter = 0
        self.get_chat_history()
        return chat_session

    def clear_ui(self):
        self.chat_session = None
        self.not_found = None
        self.did_submit = False
        self.messages = []

    def create_new_and_redirect(self):
        self.clear_ui()
        new_chat_session = self.create_new_chat_session()
        return rx.redirect(f"/chat/{new_chat_session.id}")

    def clear_and_start_new(self):
        self.clear_ui()
        self.create_new_chat_session()
        yield

    def get_session_from_db(self, session_id=None):
        if session_id is None:
            session_id = self.get_session_id()
        # ChatSession.id == session_id
        with rx.session() as db_session:
            sql_statement = sqlmodel.select(ChatSession).where(
                ChatSession.id == session_id
            )
            result = db_session.exec(sql_statement).one_or_none()
            if result is None:
                self.not_found = True
            else:
                self.not_found = False
            self.chat_session = result
            messages = result.messages
            for msg_obj in messages:
                msg_txt = msg_obj.content
                is_bot = False if msg_obj.role == "user" else True
                self.append_message_to_ui(msg_txt, is_bot=is_bot)

    def on_detail_load(self):
        session_id = self.get_session_id()
        reload_detail = False
        if not self.chat_session:
            reload_detail = True
        else:
            """has a session"""
            if self.chat_session.id != session_id:
                reload_detail = True

        if reload_detail:
            self.clear_ui()
            if isinstance(session_id, int):
                self.get_session_from_db(session_id=session_id)

    def on_load(self):
        print("running on load")
        self.clear_ui()
        self.create_new_chat_session()

    def insert_message_to_db(self, content, role="unknown"):
        print("insert message data to db")
        if self.chat_session is None:
            return
        if not isinstance(self.chat_session, ChatSession):
            return
        with rx.session() as db_session:
            data = {
                "session_id": self.chat_session.id,
                "content": content,
                "role": role,
            }
            obj = ChatSessionMessageModel(**data)
            db_session.add(obj)  # prepare to save
            db_session.commit()  # actually save
        self.session_msg_counter += 1

    def append_message_to_ui(self, message, is_bot: bool = False):
        self.messages.append(ChatMessage(message=message, is_bot=is_bot))

    # def get_gpt_messages(self):
    #     gpt_messages = [
    #         {
    #             "role": "system",
    #             "content": "You are an expert at creating recipes like an elite chef. Respond in markdown"
    #         }
    #     ]
    #     for chat_message in self.messages:
    #         role = 'user'
    #         if chat_message.is_bot:
    #             role = 'system'
    #         gpt_messages.append({
    #             "role": role,
    #             "content": chat_message.message
    #         })
    #     return gpt_messages

    async def handle_submit(self, form_data: dict):
        print("here is our form data", form_data)
        user_message = form_data.get("message")
        if user_message:
            self.did_submit = True
            self.append_message_to_ui(user_message, is_bot=False)
            self.insert_message_to_db(user_message, role="user")
            yield
            # gpt_messages = self.get_gpt_messages()
            # bot_response = ai.get_llm_response(gpt_messages)
            bot_response = "bot response"
            self.did_submit = False
            self.append_message_to_ui(bot_response, is_bot=True)
            self.insert_message_to_db(bot_response, role="system")
            yield
