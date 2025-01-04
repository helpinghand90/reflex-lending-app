"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from lending_app import ui

def about_us_page() -> rx.Component:
    # About us Page
    return ui.base_layout(
        rx.vstack(
            rx.heading("Welcome to Reflex About!", size="9"),
            spacing="5",
            justify="center",
            min_height="85vh",
            width="100%",  # Ensure full width
            id="about-us-vstack",
        ),
    )