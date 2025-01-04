import reflex as rx
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
import os
import logging
from lending_app.models import UserDetailsModel

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(funcName)s - %(lineno)d",
)


# TODO: Remove Kinde credentials from the file here
# TODO: only log user details to the database when they first sign up

# KINDE_HOST = os.environ.get("KINDE_HOST")
# KINDE_CLIENT_ID = os.environ.get("KINDE_CLIENT_ID")
# KINDE_CLIENT_SECRET = os.environ.get("KINDE_CLIENT_SECRET")
KINDE_REDIRECT_URL = os.environ.get(
    "KINDE_REDIRECT_URL",
    "https://crispy-telegram-pj4wp47g7rqcrw6q-3000.app.github.dev/",
)
KINDE_POST_LOGOUT_REDIRECT_URL = os.environ.get(
    "KINDE_POST_LOGOUT_REDIRECT_URL",
    "https://crispy-telegram-pj4wp47g7rqcrw6q-3000.app.github.dev/",
)


configuration = Configuration(host="https://whitelabel.kinde.com")
kinde_api_client_params = {
    "configuration": configuration,
    "domain": "https://whitelabel.kinde.com",
    "client_id": "07ef9e51d8e74694b4dbd57e9dfb8622",
    "client_secret": "DWwnaRwijJVrSgtM52G94OUxuRQKL4DUB23iXsl33oer3hn1ZAC",
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": "https://crispy-telegram-pj4wp47g7rqcrw6q-3000.app.github.dev/",
}
kinde_client = KindeApiClient(**kinde_api_client_params)


class AuthState(rx.State):
    """The app state."""

    is_authenticated: bool = False
    user_details: dict = {}

    def initiate_login(self):
        logging.info("Initiating login process")
        return rx.redirect(kinde_client.get_login_url())

    def perform_logout(self):
        logging.info("Performing logout")
        self.is_authenticated = False
        self.user_details = {}
        logging.info("User state reset")
        return rx.redirect(
            kinde_client.logout(redirect_to=KINDE_POST_LOGOUT_REDIRECT_URL)
        )

    def process_authentication(self):
        logging.info("Processing authentication")
        auth_params = self.router.page.params
        logging.info(f"Query params: {auth_params}")

        error = auth_params.get("error")
        if error:
            logging.info(f"Authentication error from Kinde: {error}")
            return self.clean_url_and_redirect()

        if auth_params.get("code") and auth_params.get("state"):
            logging.info("Authorization code and state found in query params")
            self.exchange_code_for_token(auth_params)
            return self.clean_url_and_redirect()
        else:
            logging.info(
                "No authorization code and state in query params, attempting silent authentication"
            )
            return self.attempt_silent_auth()

    def exchange_code_for_token(self, auth_params):
        logging.info("Exchanging authorization code for token")
        full_url = f"{KINDE_REDIRECT_URL}?code={auth_params['code']}&state={auth_params['state']}"
        try:
            kinde_client.fetch_token(authorization_response=full_url)
            logging.info("Token fetched successfully")
            self.update_auth_status()
        except Exception as e:
            logging.error(f"Token exchange error: {str(e)}")

    def update_auth_status(self):
        logging.info("Updating authentication status")
        self.is_authenticated = kinde_client.is_authenticated()
        logging.info(f"is_authenticated: {self.is_authenticated}")

        if self.is_authenticated:
            self.user_details = kinde_client.get_user_details()
            logging.info(f"User details fetched: {self.user_details}")
            self.save_user_to_database(self.user_details)
        else:
            logging.info("User is not authenticated")

    def attempt_silent_auth(self):
        logging.info("Attempting silent authentication")
        login_url = kinde_client.get_login_url(additional_params={"prompt": "none"})

        logging.info(f"Login URL: {login_url}")
        # return rx.redirect(login_url)

    def initialize_auth(self):
        logging.info("Initializing authentication")
        self.update_auth_status()

    def clean_url_and_redirect(self):
        logging.info("Cleaning URL and redirecting")
        return rx.redirect("/")

    def save_user_to_database(self, user_details):
        try:
            with rx.session() as db_session:
                data = {
                    "user_id": user_details["id"],
                    "given_name": user_details["given_name"],
                    "family_name": user_details["family_name"],
                    "email": user_details["email"],
                    "picture": user_details["picture"],
                }
                obj = UserDetailsModel(**data)
                db_session.add(obj)  # prepare to save
                db_session.commit()  # actually save

            logging.info("User data saved to the database successfully.")
        except Exception as e:
            logging.error(f"Error saving user data to the database: {str(e)}")
