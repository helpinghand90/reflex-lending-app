import reflex as rx
import logging

from lending_app import ui

from .app_state import AppState


def not_loggedin_app_placeholder() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.box(height="20vh"),
            rx.heading(
                "Please log in to start your application", size="9", text_align="center"
            ),
            rx.box(height="10vh"),
            rx.button(
                "Login/Register",
                on_click=AppState.initiate_login,
                style={"font-size": "1.5em", "padding": "1em 2em"},
            ),
            width="100%",
            text_align="center",
            minimum_height="85vh",
        ),
        width="100%",
    )


# employment details
# contact details


def form_page_1():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                ),
                rx.hstack(
                    rx.checkbox("Checked", name="check"),
                    rx.switch("Switched", name="switch"),
                ),
                rx.button("Submit", type="submit"),
            ),
            reset_on_submit=False,
            on_submit=AppState.save_next_page,
        ),
    )


def application_form() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.heading("Application Form", size="9", text_align="center"),
            rx.cond(
                AppState.app_form_page == 0,
                rx.box(
                    rx.text("Page 1"),
                    form_page_1(),
                ),
            ),
        ),
        width="100%",
    )


def app_page():

    return ui.base_layout(
        rx.cond(
            AppState.is_authenticated,
            rx.hstack(
                rx.box(width="10%"),
                rx.vstack(
                    application_form(),
                    width="100%",
                ),
                rx.box(width="10%"),
                width="100%",
            ),
            not_loggedin_app_placeholder(),
        ),
    )
