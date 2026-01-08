"""
Excel reporting systém pro měsíční reporty
"""
import xlsxwriter
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.db_manager import DatabaseManager
from src.utils.config import Config
from src.utils.logger import main_logger

class ExcelReporter:
    """Generování Excel reportů"""

    def __init__(self):
        self.db = DatabaseManager()

    def generate_monthly_report(self, year: int = None, month: int = None) -> Path:
        """
        Generuje měsíční report

        Args:
            year: Rok (default: aktuální)
            month: Měsíc (default: aktuální)

        Returns:
            Cesta k vygenerovanému Excel souboru
        """
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        # Název souboru
        filename = f"Amity_Report_{year}_{month:02d}.xlsx"
        filepath = Config.REPORTS_DIR / 'monthly' / filename

        main_logger.info(f"Generuji měsíční report pro {month}/{year}...")

        # Vytvoření Excel workbook
        workbook = xlsxwriter.Workbook(str(filepath))

        # Formáty
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left'
        })

        green_format = workbook.add_format({
            'bg_color': '#C6EFCE',
            'font_color': '#006100'
        })

        yellow_format = workbook.add_format({
            'bg_color': '#FFEB9C',
            'font_color': '#9C6500'
        })

        red_format = workbook.add_format({
            'bg_color': '#FFC7CE',
            'font_color': '#9C0006'
        })

        # List 1: Přehled
        self._create_overview_sheet(workbook, year, month, header_format, title_format,
                                    green_format, yellow_format, red_format)

        # List 2: Detail influencerů
        self._create_influencers_detail_sheet(workbook, year, month, header_format)

        # List 3: Všechny příspěvky
        self._create_posts_sheet(workbook, year, month, header_format)

        # List 4: Problémové případy
        self._create_issues_sheet(workbook, year, month, header_format, red_format)

        workbook.close()
        main_logger.info(f"✅ Report vygenerován: {filepath}")

        return filepath

    def _create_overview_sheet(self, workbook, year, month, header_fmt, title_fmt,
                               green_fmt, yellow_fmt, red_fmt):
        """Vytvoří list s přehledem"""
        worksheet = workbook.add_worksheet('Přehled')
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:H', 15)

        row = 0

        # Nadpis
        worksheet.write(row, 0, 'AMITY DRINKS - Měsíční Report Influencerů', title_fmt)
        row += 1
        worksheet.write(row, 0, f'Období: {month}/{year}')
        row += 1
        worksheet.write(row, 0, f'Generováno: {datetime.now().strftime("%d.%m.%Y %H:%M")}')
        row += 3

        # Celková statistika
        self.db.connect()
        stats = self.db.get_monthly_stats(year, month)
        influencers = self.db.get_all_influencers()

        total_influencers = len(influencers)
        met_target = sum(1 for s in stats if s.get('target_met'))
        not_met = total_influencers - met_target
        total_posts = sum(s['stories_count'] + s['posts_count'] + s['reels_count'] for s in stats)
        total_reach = sum(s.get('total_reach', 0) for s in stats)

        worksheet.write(row, 0, 'CELKOVÁ STATISTIKA', title_fmt)
        row += 1

        summary_data = [
            ['Počet aktivních influencerů:', total_influencers],
            ['Splnili cíle:', met_target],
            ['Nesplnili cíle:', not_met],
            ['Celkový počet příspěvků:', total_posts],
            ['Celkový reach:', f'{total_reach:,}']
        ]

        for label, value in summary_data:
            worksheet.write(row, 0, label)
            worksheet.write(row, 1, value)
            row += 1

        row += 2

        # Tabulka influencerů
        worksheet.write(row, 0, 'PŘEHLED INFLUENCERŮ', title_fmt)
        row += 1

        headers = ['Jméno', 'Stories (cíl/skut.)', 'Posty (cíl/skut.)', 'Reels (cíl/skut.)',
                  'Celkem', '% Plnění', 'Status', 'Reach']

        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_fmt)
        row += 1

        # Data influencerů
        for stat in stats:
            stories_actual = stat['stories_count']
            stories_target = stat['stories_mesic']
            posts_actual = stat['posts_count']
            posts_target = stat['prispevky_mesic']
            reels_actual = stat['reels_count']
            reels_target = stat['reels_mesic']

            total_actual = stories_actual + posts_actual + reels_actual
            total_target = stories_target + posts_target + reels_target

            completion = (total_actual / total_target * 100) if total_target > 0 else 0

            # Určení formátu podle plnění
            if stat['target_met']:
                fmt = green_fmt
                status = '✅ Splněno'
            elif completion >= 50:
                fmt = yellow_fmt
                status = '⚠️ Riziko'
            else:
                fmt = red_fmt
                status = '❌ Nesplní'

            worksheet.write(row, 0, stat['jmeno'])
            worksheet.write(row, 1, f"{stories_actual}/{stories_target}", fmt)
            worksheet.write(row, 2, f"{posts_actual}/{posts_target}", fmt)
            worksheet.write(row, 3, f"{reels_actual}/{reels_target}", fmt)
            worksheet.write(row, 4, total_actual, fmt)
            worksheet.write(row, 5, f"{completion:.0f}%", fmt)
            worksheet.write(row, 6, status, fmt)
            worksheet.write(row, 7, f"{stat.get('total_reach', 0):,}", fmt)
            row += 1

        self.db.close()

    def _create_influencers_detail_sheet(self, workbook, year, month, header_fmt):
        """Vytvoří detail influencerů"""
        worksheet = workbook.add_worksheet('Detail Influencerů')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:G', 12)

        self.db.connect()
        influencers = self.db.get_all_influencers()

        row = 0
        headers = ['Jméno', 'Instagram', 'Facebook', 'TikTok', 'Email', 'Datum začátku', 'Poznámky']

        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_fmt)
        row += 1

        for inf in influencers:
            worksheet.write(row, 0, inf['jmeno'])
            worksheet.write(row, 1, f"@{inf.get('instagram_handle', '')}")
            worksheet.write(row, 2, inf.get('facebook_handle', ''))
            worksheet.write(row, 3, f"@{inf.get('tiktok_handle', '')}" if inf.get('tiktok_handle') else '')
            worksheet.write(row, 4, inf.get('email', ''))
            worksheet.write(row, 5, str(inf.get('datum_zacatku', '')))
            worksheet.write(row, 6, inf.get('poznamky', ''))
            row += 1

        self.db.close()

    def _create_posts_sheet(self, workbook, year, month, header_fmt):
        """Vytvoří list se všemi příspěvky"""
        worksheet = workbook.add_worksheet('Všechny Příspěvky')
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 50)
        worksheet.set_column('E:H', 12)

        self.db.connect()
        posts = self.db.get_posts_by_month(year, month)

        row = 0
        headers = ['Influencer', 'Platforma', 'Typ', 'Caption', 'Datum', 'Likes', 'Comments', 'Reach']

        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_fmt)
        row += 1

        for post in posts:
            worksheet.write(row, 0, post.get('influencer_name', ''))
            worksheet.write(row, 1, post['platform'].title())
            worksheet.write(row, 2, post['post_type'].title())
            worksheet.write(row, 3, post.get('caption', '')[:100])
            worksheet.write(row, 4, post['timestamp'][:10] if post.get('timestamp') else '')
            worksheet.write(row, 5, post.get('likes', 0))
            worksheet.write(row, 6, post.get('comments', 0))
            worksheet.write(row, 7, post.get('reach', 0))
            row += 1

        self.db.close()

    def _create_issues_sheet(self, workbook, year, month, header_fmt, red_fmt):
        """Vytvoří list s problémovými případy"""
        worksheet = workbook.add_worksheet('Problémové Případy')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:E', 15)

        self.db.connect()
        stats = self.db.get_monthly_stats(year, month)

        row = 0
        worksheet.write(row, 0, 'INFLUENCEŘI, KTEŘÍ NESPLNILI CÍLE', header_fmt)
        row += 2

        headers = ['Jméno', 'Stories', 'Posty', 'Reels', 'Doporučení']

        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_fmt)
        row += 1

        # Filtr nesplněných
        issues = [s for s in stats if not s.get('target_met')]

        if not issues:
            worksheet.write(row, 0, '✅ Všichni influenceři splnili cíle!')
        else:
            for stat in issues:
                worksheet.write(row, 0, stat['jmeno'], red_fmt)
                worksheet.write(row, 1, f"{stat['stories_count']}/{stat['stories_mesic']}", red_fmt)
                worksheet.write(row, 2, f"{stat['posts_count']}/{stat['prispevky_mesic']}", red_fmt)
                worksheet.write(row, 3, f"{stat['reels_count']}/{stat['reels_mesic']}", red_fmt)
                worksheet.write(row, 4, 'Kontaktovat a připomenout', red_fmt)
                row += 1

        self.db.close()
