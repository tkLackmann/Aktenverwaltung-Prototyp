import os
import csv
from datetime import datetime, timedelta
import subprocess  # für Git Push

DATEI = "Prototype 0.6.csv"
akten = []

# Laden der CSV-Datei falls vorhanden
if os.path.exists(DATEI):
    with open(DATEI, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        akten = list(reader)

# -------------------------------
# Git-Push-Funktion
def git_push():
    try:
        subprocess.run(["git", "add", DATEI], check=True)
        subprocess.run(["git", "commit", "-m", "Automatisches Update der Akten"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("CSV-Datei erfolgreich in das Repository übertragen!")
    except subprocess.CalledProcessError:
        print("Fehler beim Pushen in Git! Prüfe Git-Konfiguration.")
# -------------------------------

def speichern():
    with open(DATEI, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["Name","Art","Länge","Grund","Erstellt","Ende"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for akte in akten:
            writer.writerow(akte)
    git_push()

def reset():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Chat wurde zurückgesetzt (Daten bleiben erhalten)\n")

def sammeln():
    print("Format: Name,Art,Länge(in Tagen),Grund")
    eingabe = input(">> ")
    teile = eingabe.split(",")
    if len(teile) != 4:
        print("Fehler: Bitte genau 4 Werte eingeben!\n")
        return
    try:
        laenge = int(teile[2].strip())
    except ValueError:
        print("Länge muss eine Zahl sein!\n")
        return

    erstellt_am = datetime.now()
    enddatum = erstellt_am + timedelta(days=laenge)
    neue_akte = {
        "Name": teile[0].strip(),
        "Art": teile[1].strip(),
        "Länge": str(laenge),
        "Grund": teile[3].strip(),
        "Erstellt": erstellt_am.strftime("%d.%m.%Y"),
        "Ende": enddatum.strftime("%d.%m.%Y")
    }
    akten.append(neue_akte)
    speichern()
    print("Akte wurde hinzugefügt!\n")

def sehen(sort_by=None):
    if not akten:
        print("Keine Akten vorhanden.\n")
        return

    # Optional sortieren
    if sort_by in ["Name", "Art", "Länge", "Erstellt", "Ende"]:
        akten.sort(key=lambda x: x[sort_by])

    print("\n--- Aktensammlung ---")
    print(f"{'Nr':<5}  {'Name':<25}  {'Art':<20}  {'Länge':<10}  {'Erstellt':<15}  {'Ende':<15}  {'Grund':<30}")
    print("-" * 150)
    for i, akte in enumerate(akten):
        print(
            f"{i:<5}  "
            f"{akte['Name']:<25}  "
            f"{akte['Art']:<20}  "
            f"{akte['Länge']:<10}  "
            f"{akte['Erstellt']:<15}  "
            f"{akte['Ende']:<15}  "
            f"{akte['Grund']:<30}"
        )
    print()

def loeschen():
    sehen()
    if not akten:
        return
    try:
        nummer = int(input("Welche Nummer löschen? "))
        if 0 <= nummer < len(akten):
            geloescht = akten.pop(nummer)
            speichern()
            print(f"Akte von {geloescht['Name']} gelöscht!\n")
        else:
            print("Ungültige Nummer.\n")
    except ValueError:
        print("Bitte eine gültige Zahl eingeben!\n")

def abgelaufene_loeschen():
    global akten
    heute = datetime.now()
    neue_akten = []
    for akte in akten:
        ende = datetime.strptime(akte['Ende'], "%d.%m.%Y")
        if ende >= heute:
            neue_akten.append(akte)
    akten = neue_akten
    speichern()
    print("Abgelaufene Akten wurden gelöscht!\n")

def top5_kuerzeste():
    if not akten:
        print("Keine Akten vorhanden.\n")
        return
    sorted_list = sorted(akten, key=lambda x: int(x['Länge']))
    print("\n--- Top 5 kürzeste Banns ---")
    for akte in sorted_list[:5]:
        print(f"{akte['Name']} ({akte['Länge']} Tage) - Ende: {akte['Ende']}")
    print()

def suche():
    begriff = input("Suchbegriff: ").lower()
    results = [a for a in akten if begriff in a['Name'].lower() or begriff in a['Art'].lower()]
    if not results:
        print("Keine Ergebnisse gefunden.\n")
        return
    print("\n--- Suchergebnisse ---")
    for akte in results:
        print(f"{akte['Name']} - {akte['Art']} - Ende: {akte['Ende']}")
    print()

# Hauptmenü
while True:
    print("1 = Sammeln (schnell)")
    print("2 = Sehen")
    print("3 = Löschen")
    print("4 = Reset (Chat leeren)")
    print("5 = Abgelaufene Akten löschen")
    print("6 = Top 5 kürzeste Banns")
    print("7 = Suche")
    print("8 = Beenden")

    auswahl = input("Wähle: ")

    if auswahl == "1":
        sammeln()
    elif auswahl == "2":
        sehen()
    elif auswahl == "3":
        loeschen()
    elif auswahl == "4":
        reset()
    elif auswahl == "5":
        abgelaufene_loeschen()
    elif auswahl == "6":
        top5_kuerzeste()
    elif auswahl == "7":
        suche()
    elif auswahl == "8":
        print("Programm beendet.")
        break
    else:
        print("Ungültige Eingabe.\n")
