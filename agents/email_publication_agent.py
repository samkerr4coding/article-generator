import json
import logging
import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

class EmailPublicationAgent:
    def __init__(self):
        load_dotenv()
        self.gmail_email = os.getenv("GMAIL_EMAIL")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not self.gmail_email or not self.gmail_password:
            raise ValueError("You must set GMAIL_EMAIL and GMAIL_APP_PASSWORD in your .env file")

    def send_article_via_email(self, article):
        try:
            msg = EmailMessage()
            msg["Subject"] = f"Generated Article: {article['title']}"
            msg["From"] = self.gmail_email
            msg["To"] = self.gmail_email
            msg.set_content(article.get("content", ""))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_email, self.gmail_password)
                server.send_message(msg)
            logging.info(f"Article '{article['title']}' sent via email.")
            return True
        except Exception as e:
            logging.error(f"Failed to send article '{article.get('title')}' via email: {e}")
            return False

    def publish_articles_from_state(self, state):
        data = state.get('article_producer_agent_result')
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                logging.error(f"Invalid JSON structure in state: {e}")
                return []
        if not data or not isinstance(data, dict) or "articles" not in data:
            logging.error("No articles found in state for email publication.")
            return []

        results = []
        # for article in data.get("articles", []):
        #     if not article.get("title") or not article.get("content"):
        #         continue
        #     email_sent = self.send_article_via_email(article)
        #     results.append({
        #         "title": article["title"],
        #         "email_sent": email_sent
        #     })
        return results

    @classmethod
    def test_email_sending(cls, test_subject="Test Email from EmailPublicationAgent", test_body="This is a test email sent to verify SMTP configuration."):
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
                # server.send_message(msg)
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

if __name__ == "__main__":
    # To test email config directly, uncomment the next line:
    EmailPublicationAgent.test_email_sending()
