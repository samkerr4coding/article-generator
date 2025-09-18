import json
import logging
import os
import smtplib
import tempfile
import zipfile
from dotenv import load_dotenv
from email.message import EmailMessage


class EmailPublicationAgent:
    def __init__(self):
        load_dotenv()
        self.gmail_email = os.getenv("GMAIL_EMAIL")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not self.gmail_email or not self.gmail_password:
            raise ValueError("You must set GMAIL_EMAIL and GMAIL_APP_PASSWORD in your .env file")

        # Where rewritten articles are stored
        self.output_root = "articles/output"

    def _create_zip_from_articles(self):
        """
        Walk through articles/output/<title> folders and bundle all .md files into a zip archive.
        Returns the path of the zip file.
        """
        if not os.path.exists(self.output_root):
            logging.warning(f"Output folder '{self.output_root}' does not exist.")
            return None

        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "articles_bundle.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.output_root):
                for file in files:
                    if file.endswith(".md"):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, self.output_root)
                        zipf.write(full_path, rel_path)
                        logging.debug(f"Added {rel_path} to zip archive")

        logging.info(f"Created zip archive: {zip_path}")
        return zip_path

    def send_articles_zip_via_email(self):
        """
        Create a zip archive of all rewritten articles and send it in one email.
        """
        zip_path = self._create_zip_from_articles()
        if not zip_path:
            logging.error("No articles to send. Aborting email send.")
            return False

        try:
            msg = EmailMessage()
            msg["Subject"] = "Generated Articles Bundle"
            msg["From"] = self.gmail_email
            msg["To"] = self.gmail_email
            msg.set_content("Attached is the zip archive containing all rewritten articles.")

            # Attach the zip
            with open(zip_path, "rb") as f:
                zip_data = f.read()
                msg.add_attachment(
                    zip_data,
                    maintype="application",
                    subtype="zip",
                    filename="articles_bundle.zip",
                )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_email, self.gmail_password)
                server.send_message(msg)

            logging.info("Articles bundle sent via email successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to send articles bundle via email: {e}")
            return False

    def publish_articles_from_state(self, state):
        """
        Ignores state content and just sends everything under articles/output as a zip.
        """
        success = self.send_articles_zip_via_email()
        return {"email_sent": success}

    @classmethod
    def test_email_sending(
        cls,
        test_subject="Test Email from EmailPublicationAgent",
        test_body="This is a test email sent to verify SMTP configuration.",
    ):
        """
        Sends a test email with a fixed subject and body to verify setup.
        """
        load_dotenv()
        gmail_email = os.getenv("GMAIL_EMAIL")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_email or not gmail_password:
            print("You must set GMAIL_EMAIL and GMAIL_APP_PASSWORD in your .env file")
            return False

        msg = EmailMessage()
        msg["Subject"] = test_subject
        msg["From"] = gmail_email
        msg["To"] = gmail_email
        msg.set_content(test_body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_email, gmail_password)
                # server.send_message(msg)  # Uncomment to actually send test
            print(f"Test email sent successfully to {gmail_email}")
            return True
        except Exception as e:
            print(f"Failed to send test email: {e}")
            return False


def run(state):
    logging.info("Starting email publication task")
    agent = EmailPublicationAgent()
    email_publication_results = agent.publish_articles_from_state(state)
    logging.info(f"Finished email publication task: {email_publication_results}")
    return {"email_publication_result": email_publication_results}
