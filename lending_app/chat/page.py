import reflex as rx

from lending_app import ui


from lending_app.auth.state import AuthState
from .state import ChatMessage, ChatState
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


def chat_page():

    return ui.base_layout(
        rx.cond(
            AuthState.is_authenticated,
            rx.vstack(
                rx.hstack(
                    rx.heading("Chat Here", size="5"),
                    rx.cond(ChatState.not_found, "Not found", "Found"),
                    rx.button("+ New Chat", on_click=ChatState.create_new_and_redirect),
                ),
                rx.box(rx.foreach(ChatState.messages, message_box), width="100%"),
                chat_form(),
                margin="3rem auto",
                spacing="5",
                justify="center",
                min_height="85vh",
            ),
            rx.hstack(
                rx.box(
                    rx.box(height="20vh"),
                    rx.heading(
                        "Please log in to start a chat", size="9", text_align="center"
                    ),
                    rx.box(height="10vh"),
                    rx.button("Login/Register", on_click=AuthState.initiate_login, style={"font-size": "1.5em", "padding": "1em 2em"}),
                    width="100%",
                    text_align="center",
                    minimum_height="85vh",
                ),
                width="100%",
            ),
        ),
    )
