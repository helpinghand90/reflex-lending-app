import reflex as rx

from lending_app import navigation
from lending_app.auth.auth_state import AuthState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def base_navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Reflex GPT", size="7", weight="bold"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", navigation.routes.HOME_ROUTE),
                    navbar_link("About", navigation.routes.ABOUT_US_ROUTE),
                    navbar_link("Chat", navigation.routes.CHAT_ROUTE),
                    navbar_link("Apply Now", navigation.routes.APPLICATION_ROUTE),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.button("Logout", on_click=AuthState.perform_logout),
                        rx.button("Login/Register", on_click=AuthState.initiate_login),
                    ),
                    justify="end",
                    spacing="5",
                    align_items="center",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Reflex GPT", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item(
                            "Home", on_click=navigation.nav_state.NavState.to_home
                        ),
                        rx.menu.item(
                            "About", on_click=navigation.nav_state.NavState.to_about_us
                        ),
                        rx.menu.item(
                            "Chat", on_click=navigation.nav_state.NavState.to_chat
                        ),
                        rx.menu.item(
                            "Apply Now", on_click=navigation.nav_state.NavState.to_app
                        ),
                    ),
                    justify="end",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.button("Logout", on_click=AuthState.perform_logout),
                    rx.button("Login/Register", on_click=AuthState.initiate_login),
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
        on_mount=AuthState.process_authentication,
    )
