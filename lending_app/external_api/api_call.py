import reflex as rx
import requests
import json
from lending_app.auth.auth_state import AuthState
from lending_app import ui
from typing import List
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)

logger = logging.getLogger(__name__)  # Create a logger instance

def key_value_pair_display(item) -> rx.Component:
    return rx.hstack(
                        rx.text(f"{item}",  # Capitalize the key
                            color="black",  # Example styling: blue color
                            font_size="1.2em",  # Example styling: larger font size
                            margin_bottom="0.5em",  # Add margin between elements
                        )
    )


class APIState(AuthState):
    api_response: list[str] = [] # Initialize as an empty list
    is_loading: bool = False

    def call_api(self):
        self.is_loading = True  # Set loading state
        yield  # Allow UI to update with loading indicator
        try:
            api_url = f"https://jsonplaceholder.typicode.com/todos/{random.randint(1, 100)}"
            headers = {"Content-Type": "application/json"}

            logger.info(f"Calling API: {api_url} with headers: {headers}")  # Log API call

            response = requests.get(api_url, headers=headers)

            logger.info(f"API Response Status Code: {response.status_code}")  # Log status code

            response.raise_for_status()
            response_json = response.json()

            logger.debug(f"API Response JSON: {response_json}")  # Log the JSON response (use DEBUG level)
                

            temp_list = []  # Create a temporary list
            for key, value in response_json.items():
                temp_list.append(f"{key.capitalize()}: {value}")  # Append to the temporary list
            self.api_response = temp_list #Assign the temp list.
            logger.debug(f"API Response: {self.api_response}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request Error: {e}")  # Log request exceptions
            self.api_response = rx.text(f"Error: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")  # Log JSON decoding errors
            self.api_response = rx.text(f"Invalid JSON response: {e}")
        finally:
            self.is_loading = False
            logger.info("API call finished.")  # Log the completion of the API call
            yield



def api_page():

    return ui.base_layout(
        rx.cond(
            APIState.is_authenticated,
            rx.vstack(
                rx.button(
                    "Call API",
                    on_click=APIState.call_api,
                    is_disabled=APIState.is_loading,
                ),
                rx.cond(
                    APIState.is_loading,
                    rx.spinner(),  # Display loading indicator
                    # rx.text(APIState.api_response), # Display API response
                    rx.foreach(APIState.api_response, key_value_pair_display),  # Display API response
                ),
            ),
            rx.hstack(
                rx.box(width="10%"),
                rx.vstack(
                    rx.text("Please log in to use the API"),
                    width="100%",
                ),
                rx.box(width="10%"),
                width="100%",
            ),
        ),
    )
