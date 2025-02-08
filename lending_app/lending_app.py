"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from . import chat, pages, navigation, application, external_api

app = rx.App()
app.add_page(pages.home_page, route=navigation.routes.HOME_ROUTE)
app.add_page(pages.about_us_page, route=navigation.routes.ABOUT_US_ROUTE)
app.add_page(
    chat.chat_page, 
    route=f"{navigation.routes.CHAT_ROUTE}/[session_id]",
    on_load=chat.chat_state.ChatState.on_detail_load
)

app.add_page(
    chat.chat_page, 
    route=navigation.routes.CHAT_ROUTE,
    on_load=chat.chat_state.ChatState.on_load
)


app.add_page(
    application.employment_details_page, 
    route=navigation.routes.APPLICATION_ROUTE,
    # on_load=application.app_state.AppState.on_load
)

app.add_page(
    external_api.api_page, 
    route=navigation.routes.API_ROUTE
)