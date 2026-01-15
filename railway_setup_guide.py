#!/usr/bin/env python3
"""
Railway PostgreSQL Setup - Interaktivní Průvodce
"""
import os
import subprocess
import sys

print("\n" + "=" * 70)
print("🚂 RAILWAY POSTGRESQL SETUP - Interaktivní Průvodce")
print("=" * 70 + "\n")

# Check Railway CLI
print("KROK 1: Kontrola Railway CLI...")
print("-" * 70)

try:
    result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Railway CLI nainstalované: {result.stdout.strip()}")
        cli_available = True
    else:
        cli_available = False
except FileNotFoundError:
    cli_available = False

if not cli_available:
    print("❌ Railway CLI NENÍ nainstalované")
    print()
    print("📥 INSTRUKCE K INSTALACI:")
    print()
    print("   Možnost A - NPM:")
    print("   $ npm i -g @railway/cli")
    print()
    print("   Možnost B - Curl:")
    print("   $ curl -fsSL https://railway.app/install.sh | sh")
    print()
    print("   Po instalaci spusť tento script znovu!")
    print("=" * 70)
    sys.exit(0)

# Check if logged in
print()
print("KROK 2: Kontrola přihlášení...")
print("-" * 70)

result = subprocess.run(['railway', 'whoami'], capture_output=True, text=True)
if result.returncode != 0 or 'not logged in' in result.stdout.lower():
    print("❌ NEJSI přihlášen do Railway")
    print()
    print("🔐 INSTRUKCE K PŘIHLÁŠENÍ:")
    print()
    print("   Spusť v terminálu:")
    print("   $ railway login")
    print()
    print("   Otevře se prohlížeč → přihlaš se → vrať se sem")
    print("=" * 70)
    sys.exit(0)
else:
    print(f"✅ Přihlášen jako: {result.stdout.strip()}")

# Check project link
print()
print("KROK 3: Kontrola propojení projektu...")
print("-" * 70)

result = subprocess.run(['railway', 'status'], capture_output=True, text=True, cwd='/home/mariobracho/influencer')
if result.returncode != 0:
    print("❌ Projekt NENÍ propojen s Railway")
    print()
    print("🔗 INSTRUKCE K PROPOJENÍ:")
    print()
    print("   Spusť v terminálu:")
    print("   $ cd /home/mariobracho/influencer")
    print("   $ railway link")
    print()
    print("   Vyber svůj projekt ze seznamu")
    print("=" * 70)
    sys.exit(0)
else:
    print(f"✅ Projekt propojen")
    print(result.stdout)

# List services
print()
print("KROK 4: Seznam služeb v projektu...")
print("-" * 70)

result = subprocess.run(['railway', 'service'], capture_output=True, text=True, cwd='/home/mariobracho/influencer')
print(result.stdout)

if 'postgres' in result.stdout.lower():
    print("✅ PostgreSQL služba EXISTUJE!")
    has_postgres = True
else:
    print("❌ PostgreSQL služba NEEXISTUJE")
    has_postgres = False

# Check DATABASE_URL
print()
print("KROK 5: Kontrola DATABASE_URL...")
print("-" * 70)

result = subprocess.run(
    ['railway', 'variables', '--json'],
    capture_output=True,
    text=True,
    cwd='/home/mariobracho/influencer'
)

if 'DATABASE_URL' in result.stdout:
    print("✅ DATABASE_URL JE nastavena!")
    has_db_url = True
else:
    print("❌ DATABASE_URL NENÍ nastavena")
    has_db_url = False

# Summary and next steps
print()
print("=" * 70)
print("📊 SHRNUTÍ:")
print("=" * 70)

if has_postgres and has_db_url:
    print()
    print("🎉 VŠE JE NASTAVENO SPRÁVNĚ!")
    print()
    print("✅ PostgreSQL služba existuje")
    print("✅ DATABASE_URL je nastavena")
    print()
    print("Můžeš deployovat aplikaci:")
    print("$ git add .")
    print("$ git commit -m 'Add Google Sheets integration'")
    print("$ git push origin main")
    print()
elif has_postgres and not has_db_url:
    print()
    print("⚠️  PROBLÉM: PostgreSQL existuje, ale DATABASE_URL chybí")
    print()
    print("🔧 ŘEŠENÍ:")
    print()
    print("1. Jdi na: https://railway.app")
    print("2. Otevři svůj projekt")
    print("3. Klikni na PostgreSQL service")
    print("4. Variables → zkopíruj DATABASE_URL")
    print("5. Klikni na Streamlit service")
    print("6. Variables → + New Variable")
    print("   Name: DATABASE_URL")
    print("   Value: [vlož zkopírovanou hodnotu]")
    print("7. Save")
    print()
elif not has_postgres:
    print()
    print("⚠️  PROBLÉM: PostgreSQL služba NEEXISTUJE")
    print()
    print("🔧 ŘEŠENÍ - Automatické přidání:")
    print()
    print("Chceš přidat PostgreSQL automaticky? (y/n)")
    choice = input("Odpověď: ").lower()

    if choice == 'y':
        print()
        print("🚀 Přidávám PostgreSQL...")
        result = subprocess.run(
            ['railway', 'add', '--database', 'postgresql'],
            cwd='/home/mariobracho/influencer'
        )

        if result.returncode == 0:
            print()
            print("✅ PostgreSQL úspěšně přidána!")
            print()
            print("Počkej ~2 minuty než se vytvoří, pak:")
            print("$ python3 railway_setup_guide.py")
        else:
            print()
            print("❌ Automatické přidání selhalo")
            print()
            print("🔧 MANUÁLNÍ POSTUP:")
            print()
            print("1. Jdi na: https://railway.app")
            print("2. Otevři svůj projekt")
            print("3. Klikni 'New' nebo '+'")
            print("4. Vyber 'Database'")
            print("5. Vyber 'Add PostgreSQL'")
            print("6. Počkej ~2 minuty")
            print("7. Spusť tento script znovu")
    else:
        print()
        print("🔧 MANUÁLNÍ POSTUP:")
        print()
        print("1. Jdi na: https://railway.app")
        print("2. Otevři svůj projekt")
        print("3. Klikni 'New' nebo '+'")
        print("4. Vyber 'Database'")
        print("5. Vyber 'Add PostgreSQL'")
        print("6. Počkej ~2 minuty")
        print("7. Spusť tento script znovu")

print()
print("=" * 70)
print()
