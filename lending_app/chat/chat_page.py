import reflex as rx
import logging

from lending_app import ui

from .chat_state import ChatMessage, ChatState, ChatSession
from .form import chat_form




message_style = dict(
    display="inline-block",
    padding="1em",
    border_radius="8px",
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
)


def message_box(chat_message: ChatMessage) -> rx.Component:
    return rx.box(
        rx.box(
            rx.markdown(
                chat_message.message,
                background_color=rx.cond(
                    chat_message.is_bot, rx.color("mauve", 4), rx.color("blue", 4)
                ),
                color=rx.cond(
                    chat_message.is_bot, rx.color("mauve", 12), rx.color("blue", 12)
                ),
                **message_style,
            ),
            text_align=rx.cond(chat_message.is_bot, "left", "right"),
            margin_top="1em",
        ),
        width="100%",
    )


def not_loggedin_chat_placeholder() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.box(height="20vh"),
            rx.heading("Please log in to start a chat", size="9", text_align="center"),
            rx.box(height="10vh"),
            rx.button(
                "Login/Register",
                on_click=ChatState.initiate_login,
                style={"font-size": "1.5em", "padding": "1em 2em"},
            ),
            width="100%",
            text_align="center",
            minimum_height="85vh",
        ),
        width="100%",
    )


def chat_window() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Chat Here", size="5"),
            rx.cond(ChatState.not_found, "Not found", "Found"),
            rx.button("+ New Chat", on_click=ChatState.create_new_and_redirect),
            gap="auto",
            id="chat-page-open-hstack",
        ),
        rx.box(
            rx.foreach(ChatState.messages, message_box),
            width="100%",
            overflow="auto",
            max_height="65vh",
            id="chat-page-open-messages",
        ),
        chat_form(),
        spacing="5",
        justify="center",
        min_height="25vh",
        width="100%",
        id="chat-page-open-vstack",
    )


def hist_chat_session_card(chat_session: ChatSession) -> rx.Component:
    return rx.link(
        rx.card(
            f"User {chat_session.user_id}: Chat {chat_session.id} @ {chat_session.created_at}",
            height="7vh",
            width="100%",
        ),
        on_click=lambda: rx.redirect(f"/chat/{chat_session.id}"),
    )


def chat_history():
    return rx.box(
        rx.vstack(
            rx.heading("Chat History", size="5"),
            rx.box(
                rx.grid(
                    rx.foreach(
                        ChatState.hist_chat_sessions,
                        hist_chat_session_card,
                    ),
                    gap="1rem",
                    grid_template_columns="1fr",
                    width="100%",
                ),
                width="100%",
                overflow="auto",
                max_height="35vh",
                padding="8px",
            ),
            width="100%",
        ),
        width="100%",
        height="100%",
        min_height="7vh",
        id="chat-history",
    )


def chat_page():

    return ui.base_layout(
        rx.cond(
            ChatState.is_authenticated,
            rx.hstack(
                rx.box(width="10%"),
                rx.vstack(
                    chat_window(),
                    chat_history(),
                    width="100%",
                ),
                rx.box(width="10%"),
                width="100%",
            ),
            not_loggedin_chat_placeholder(),
        ),
    )
