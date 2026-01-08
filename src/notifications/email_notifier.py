"""
Email notifikační systém
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import notification_logger
from src.database.db_manager import DatabaseManager

class EmailNotifier:
    """Email notifikace"""

    def __init__(self):
        self.enabled = Config.EMAIL_ENABLED
        self.from_email = Config.EMAIL_FROM
        self.to_email = Config.EMAIL_TO
        self.password = Config.EMAIL_PASSWORD
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.db = DatabaseManager()

    def send_email(self, subject: str, body: str, attachments: List[Path] = None) -> bool:
        """
        Odešle email

        Args:
            subject: Předmět emailu
            body: Tělo emailu (HTML podporováno)
            attachments: Seznam příloh

        Returns:
            True pokud úspěšně odesláno
        """
        if not self.enabled:
            notification_logger.info("Email notifikace jsou vypnuté")
            return False

        if not self.password or self.password == 'your_gmail_app_password_here':
            notification_logger.warning("Email heslo není nastaveno, přeskakuji odeslání")
            return False

        try:
            # Vytvoření zprávy
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject

            # HTML tělo
            msg.attach(MIMEText(body, 'html'))

            # Přílohy
            if attachments:
                for attachment_path in attachments:
                    if attachment_path.exists():
                        with open(attachment_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition',
                                          f'attachment; filename={attachment_path.name}')
                            msg.attach(part)

            # Odeslání
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)

            notification_logger.info(f"✅ Email odeslán: {subject}")

            # Uložení do databáze
            self.db.connect()
            self.db.log_notification('email', self.to_email, subject, body[:200], 'sent')
            self.db.close()

            return True

        except Exception as e:
            notification_logger.error(f"Chyba při odesílání emailu: {str(e)}")

            # Uložení chyby
            self.db.connect()
            self.db.log_notification('email', self.to_email, subject, str(e), 'failed')
            self.db.close()

            return False

    def send_new_post_notification(self, posts: List[Dict]) -> bool:
        """
        Odešle notifikaci o nových příspěvcích

        Args:
            posts: Seznam nových příspěvků

        Returns:
            True pokud úspěšně odesláno
        """
        if not posts:
            return False

        subject = f"✅ {len(posts)} {'nový příspěvek' if len(posts) == 1 else 'nové příspěvky'} - Amity Drinks"

        # HTML tělo
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #4472C4; color: white; padding: 15px; }}
                .content {{ padding: 20px; }}
                .post {{ background-color: #f5f5f5; margin: 10px 0; padding: 15px; border-left: 4px solid #4472C4; }}
                .platform {{ font-weight: bold; color: #4472C4; }}
                .footer {{ margin-top: 30px; padding: 15px; background-color: #f0f0f0; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🍹 Amity Drinks - Influencer Monitor</h2>
            </div>

            <div class="content">
                <p>Dobrý den,</p>

                <p>byl{'y' if len(posts) > 1 else ''} detekován{'y' if len(posts) > 1 else ''}
                <strong>{len(posts)}</strong> {'nové příspěvky' if len(posts) > 1 else 'nový příspěvek'}
                s označením Amity Drinks:</p>
        """

        # Přidání jednotlivých příspěvků
        for post in posts[:10]:  # Max 10 v emailu
            influencer_name = self._get_influencer_name(post.get('influencer_id'))
            platform_emoji = '📱' if post['platform'] == 'instagram' else '👍'

            body += f"""
                <div class="post">
                    <p>👤 <strong>Influencer:</strong> {influencer_name}</p>
                    <p>{platform_emoji} <span class="platform">{post['platform'].title()}</span> - {post['post_type'].title()}</p>
                    <p>🕐 <strong>Čas:</strong> {post.get('timestamp', 'N/A')}</p>
                    <p>💬 <strong>Text:</strong> {post.get('caption', 'Bez popisku')[:100]}</p>
                    {'<p>🔗 <a href="' + post['post_url'] + '">Zobrazit příspěvek</a></p>' if post.get('post_url') else ''}
                </div>
            """

        if len(posts) > 10:
            body += f"<p><em>... a dalších {len(posts) - 10} příspěvků</em></p>"

        body += """
            </div>

            <div class="footer">
                <p>Tento email byl odeslán automaticky systémem Amity Influencer Monitor</p>
                <p>📊 Pro detailní přehled otevřete dashboard nebo zkontrolujte databázi</p>
            </div>
        </body>
        </html>
        """

        return self.send_email(subject, body)

    def send_daily_summary(self, date: datetime = None) -> bool:
        """
        Odešle denní souhrn

        Args:
            date: Datum (default: dnes)

        Returns:
            True pokud úspěšně odesláno
        """
        date = date or datetime.now()
        date_str = date.strftime('%d.%m.%Y')

        subject = f"📊 Denní souhrn - {date_str}"

        # Získání dat z databáze
        self.db.connect()
        # TODO: Implementovat get_posts_by_date metodu
        # Pro teď použijeme měsíční data
        posts = self.db.get_posts_by_month(date.year, date.month)
        self.db.close()

        # Filtr pro dnešní den
        today_posts = [p for p in posts if p.get('timestamp', '').startswith(date.strftime('%Y-%m-%d'))]

        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #4472C4; color: white; padding: 15px; }}
                .content {{ padding: 20px; }}
                .stat {{ display: inline-block; margin: 10px 20px; }}
                .number {{ font-size: 32px; font-weight: bold; color: #4472C4; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📊 Denní Souhrn - {date_str}</h2>
            </div>

            <div class="content">
                <h3>AKTIVITA DNES:</h3>

                <div class="stat">
                    <div class="number">{len(today_posts)}</div>
                    <div>Nových příspěvků</div>
                </div>

                <div class="stat">
                    <div class="number">{len(set(p.get('influencer_id') for p in today_posts))}</div>
                    <div>Aktivních influencerů</div>
                </div>

                <p><a href="http://localhost:8501">Zobrazit kompletní přehled v dashboardu</a></p>
            </div>
        </body>
        </html>
        """

        return self.send_email(subject, body)

    def send_monthly_report_email(self, report_path: Path) -> bool:
        """
        Odešle měsíční report jako přílohu

        Args:
            report_path: Cesta k Excel reportu

        Returns:
            True pokud úspěšně odesláno
        """
        subject = f"📈 Měsíční report - {report_path.stem}"

        body = """
        <html>
        <body>
            <h2>📈 Měsíční Report Influencerů</h2>

            <p>Dobrý den,</p>

            <p>v příloze naleznete měsíční report aktivity influencerů.</p>

            <p><strong>Report obsahuje:</strong></p>
            <ul>
                <li>✅ Přehled plnění cílů</li>
                <li>📊 Detailní statistiky</li>
                <li>📝 Seznam všech příspěvků</li>
                <li>⚠️ Problémové případy</li>
            </ul>

            <p>S pozdravem,<br>Amity Influencer Monitor</p>
        </body>
        </html>
        """

        return self.send_email(subject, body, attachments=[report_path])

    def _get_influencer_name(self, influencer_id: int) -> str:
        """Získá jméno influencera podle ID"""
        self.db.connect()
        inf = self.db.get_influencer_by_id(influencer_id)
        self.db.close()
        return inf['jmeno'] if inf else 'Neznámý'
