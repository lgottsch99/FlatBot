

import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


URL = "https://www.immobilienscout24.de/expose/164993515#/"

driver = None


#normal, nicht headless KLAPPT
def get_driver():
    global driver
    if driver is None:
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=/Users/Watanudon/chrome-selenium-profile")
        options.add_argument("--profile-directory=Profile 1")
        driver = uc.Chrome(options=options)
    return driver


def open_listing(url):
    try:
        # Wir gehen erst auf die Hauptseite, um Cookies zu "wärmen" (optional)
        # driver.get("https://www.immobilienscout24.de")
        # time.sleep(random.uniform(2, 4))
        
        driver.get(url)        
        time.sleep(random.uniform(3, 6))
        print("Seite im Hintergrund geladen.")
        
    except Exception as e:
        print(f"Fehler: {e}")


def fill_personal_data(wait):
    # 1. Dictionary mit allen Daten definieren
    # Key = data-testid, Value = Was eingetragen/ausgewählt werden soll
    form_data = {
        # Dropdowns (Select-Felder)
        "salutation": "FEMALE",
        "hasPets": "FALSE",
        "employmentStatus": "INDEFINITE_PERIOD",
        "employmentRelationship": "PUBLIC_EMPLOYEE",
        "forCommercialPurposes": "FALSE",
        "rentArrears": "FALSE",
        "insolvencyProcess": "FALSE",
        "smoker": "FALSE",
        "moveInDateType": "FLEXIBLE",
        "numberOfPersons": "ONE_PERSON",
        "applicationPackageCompleted": "TRUE",
        
        # Textfelder (Input-Felder)
        "firstName": "Lillian",
        "lastName": "Gottschalk",
        "phoneNumber": "+49 176 21920518",
        "street": "Pollnstr",
        "houseNumber": "17",
        "postcode": "85221",
        "city": "Dachau",
        "incomeAmount": "2700",
        "numberOfAdults": "1",
        "numberOfKids": "0"
    }

    # 2. Den "Nachricht"-Button klicken, um das Formular zu öffnen
    try:
        contact_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="contact-button"]')))
        contact_button.click()
        time.sleep(2)
    except:
        print("Konnte Kontakt-Button nicht finden.")
        return

	#nachricht schreiben
    nachricht(wait)

    # 3. DER SMART-LOOP: Wir gehen alle potenziellen Felder durch
    for field_id, value in form_data.items():
        try:
            # Suche das Element (egal ob Input oder Select)
            element = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="{field_id}"]')
            
            if not element:
                continue # Feld existiert in diesem Inserat nicht -> Überspringen
            
            el = element[0]
            tag_name = el.tag_name # 'input' oder 'select'
            
            # Falls es ein SELECT-Feld ist
            if tag_name == "select":
                select = Select(el)
                if select.first_selected_option.get_attribute("value") != value:
                    select.select_by_value(value)
                    print(f"Dropdown {field_id} gesetzt.")
            
            # Falls es ein INPUT-Feld ist
            elif tag_name == "input":
                # Nur ausfüllen, wenn es leer ist oder wir es überschreiben wollen
                if el.get_attribute("value") != value:
                    el.send_keys(Keys.COMMAND + "a")
                    el.send_keys(Keys.BACKSPACE)
                    el.send_keys(value)
                    print(f"Textfeld {field_id} ausgefüllt.")
                    
            time.sleep(random.uniform(0.1, 0.3)) # Kurze Pause für die Stabilität

        except Exception as e:
            print(f"Konnte Feld {field_id} nicht bearbeiten: {e}")

    # 4. Checkboxen (Toggles) - Meistens schon "checked", aber zur Sicherheit:
    for check_id in ["sendUserProfile", "followAnAgent"]:
        try:
            check = driver.find_element(By.ID, check_id)
            if not check.is_selected():
                driver.execute_script("arguments[0].click();", check)
        except:
            pass


def nachricht(wait):
		# textarea für anschreiben finden
	try:
		# 1. Warte, bis das Textfeld erscheint
		# Wir nutzen die ID "message", da sie sehr stabil ist
		message_field = wait.until(EC.presence_of_element_located((By.ID, "message")))
		
		# 2. In das Feld scrollen, falls es ein langes Formular ist
		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", message_field)
		time.sleep(1)

		# 3. Das Feld leeren, falls ein Standardtext drinsteht
		message_field.clear()

		# 4. Deine Nachricht definieren
		my_message = "Sehr geehrte D und H,\n\nbla..."

		# 5. "Menschliches" Tippen (optional, aber sicherer gegen Bot-Erkennung)
		for char in my_message:
			message_field.send_keys(char)
			# Zufällige Pause zwischen 0.02 und 0.1 Sekunden pro Buchstabe
			time.sleep(random.uniform(0.02, 0.1))

		print("Nachricht erfolgreich eingetippt!")

		# 6. Der letzte Schritt: Den Senden-Button finden
		# Meistens hat er data-testid="send-button" oder ähnliches.
		# Du kannst ihn suchen, aber noch nicht klicken, um erst zu testen.

	except Exception as e:
		print(f"Fehler beim Ausfüllen des Textfelds: {e}")


def abschicken(wait):
    try:
        # 1. Warte, bis der Abschicken-Button klickbar ist
        # Wir suchen nach einem Button mit type='submit', der die Klasse für den Primär-Button hat
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].Button_button-primary__6QTnx")))

        # 2. Ein letztes Mal scrollen und eine kurze "menschliche" Pause
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(random.uniform(1.0, 2.0))

        # 3. DER FINALE KLICK
        # submit_button.click() 
        print("KLICK: Die Bewerbung wurde (theoretisch) abgeschickt!")

    except Exception as e:
        print(f"Fehler beim Finden des Abschicken-Buttons: {e}")

    



def get_object_description(wait):
    try:
        # 1. Prüfen, ob der "weiterlesen"-Link existiert und klickbar ist
        # Wir suchen nach dem Link innerhalb der div mit Klasse "show-more"
        try:
            read_more_button = driver.find_element(By.CSS_SELECTOR, ".is24-long-text-attribute .show-more a")
            if read_more_button.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", read_more_button)
                time.sleep(0.5)
                read_more_button.click()
                print("Text expandiert ('weiterlesen' geklickt).")
                time.sleep(0.5) # Kurze Pause zum Ausklappen
        except:
            # Falls kein "weiterlesen" da ist, ist der Text schon voll sichtbar
            pass

        # 2. Den Text aus dem <pre> Tag extrahieren
        # Wir nutzen die spezifische Klasse 'is24qa-objektbeschreibung'
        description_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "is24qa-objektbeschreibung")))
        
        full_text = description_element.text
        
        print(f"Objektbeschreibung erfolgreich extrahiert ({len(full_text)} Zeichen).")
        return full_text

    except Exception as e:
        print(f"Fehler beim Extrahieren der Beschreibung: {e}")
        return ""

# Anwendung in deinem Workflow:
# beschreibung = get_object_description(wait)
# print(beschreibung)
def get_location_description(wait):
    try:
        # 1. Prüfen, ob der "weiterlesen"-Link bei der Lage existiert
        # Wir suchen spezifisch im Container, der die Lage-Klasse enthält
        try:
            # Der Selektor sucht das 'weiterlesen' innerhalb des Lage-Bereichs
            read_more_lage = driver.find_element(By.CSS_SELECTOR, "pre.is24qa-lage + .show-more a")
            if read_more_lage.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", read_more_lage)
                time.sleep(0.5)
                read_more_lage.click()
                print("Lagebeschreibung expandiert.")
        except:
            pass # Kein 'weiterlesen' vorhanden

        # 2. Den Text aus dem Lage-Tag extrahieren
        location_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "is24qa-lage")))
        lage_text = location_element.text
        
        print(f"Lagebeschreibung extrahiert ({len(lage_text)} Zeichen).")
        return lage_text

    except Exception as e:
        print(f"Fehler beim Extrahieren der Lage: {e}")
        return ""

def get_move_in_date(wait):
    try:
        # Wir suchen direkt nach der Klasse für den Wert (dd-Tag)
        date_element = driver.find_elements(By.CLASS_NAME, "is24qa-bezugsfrei-ab")
        
        if date_element:
            # .text extrahiert den Inhalt, .strip() entfernt unsichtbaren Datenmüll
            move_in_date = date_element[0].text.strip()
            print(f"Bezugsfrei ab: {move_in_date}")
            return move_in_date
        else:
            print("Info 'Bezugsfrei ab' nicht im Inserat gefunden.")
            return None
            
    except Exception as e:
        print(f"Fehler beim Extrahieren des Datums: {e}")
        return None


def get_sonstiges_description(wait):
    try:
        # 1. Prüfen, ob der "weiterlesen"-Link bei 'Sonstiges' existiert
        try:
            # Wir suchen das 'weiterlesen' spezifisch im Bereich 'sonstiges'
            read_more_misc = driver.find_element(By.CSS_SELECTOR, "pre.is24qa-sonstiges + .show-more a")
            if read_more_misc.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", read_more_misc)
                time.sleep(0.5)
                read_more_misc.click()
                print("Bereich 'Sonstiges' expandiert.")
        except:
            pass # Entweder kein Link da oder Text ist kurz genug

        # 2. Den Text aus der Klasse 'is24qa-sonstiges' extrahieren
        # Wir nutzen find_elements (Plural), um einen Crash zu vermeiden, falls das Feld fehlt
        misc_elements = driver.find_elements(By.CLASS_NAME, "is24qa-sonstiges")
        
        if misc_elements:
            misc_text = misc_elements[0].text.strip()
            print(f"Infos unter 'Sonstiges' extrahiert: {misc_text}")
            return misc_text
        else:
            return ""

    except Exception as e:
        print(f"Fehler beim Scrapen von 'Sonstiges': {e}")
        return ""

def get_contact_name(wait):
    try:
        # Wir suchen nach dem Element mit dem data-qa Attribut 'contactName'
        # Dieses befindet sich im unteren Kontaktbereich (contact-bottom)
        contact_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="contactName"]')))
        
        full_name = contact_element.text.strip()
        
        if full_name:
            print(f"Ansprechpartner gefunden: {full_name}")
            return full_name
        return "Anbieter:in" # Fallback, falls das Feld leer ist

    except Exception as e:
        print(f"Kontaktname konnte nicht gelesen werden: {e}")
        return "Anbieter:in"


def scrape_listing(wait):
    frei_ab = get_move_in_date(wait)
    objektbeschr = get_object_description(wait)
    lagetext = get_location_description(wait)
    sonstiges = get_sonstiges_description(wait)
    name = get_contact_name(wait)
    print(name)


def apply_to_listing(URL):
    driver = get_driver()
    wait = WebDriverWait(driver, 6)
    open_listing(URL)

    #scrape listing info
    scrape_listing(wait)

	#drop downs und info
    fill_personal_data(wait)

	#abschicken
    abschicken(wait)
        
    while True:
        time.sleep(1)
    time.sleep(2)




# def apply_to_listing(URL):

# 	# Prüfen, ob es überhaupt ein ImmoScout-Link ist
# 	if "immobilienscout24.de" not in URL:
# 		print(f"Überspringe: {URL} ist kein ImmoScout-Link.")
# 		return

# 	driver = get_driver()


# 	open_listing(URL)

# 	#'Nachricht button klicken
# 	try:
# 		# 1. Warte maximal 15 Sekunden, bis der Button im DOM ist und klickbar wird
# 		wait = WebDriverWait(driver, 7)
		
# 		# Wir nutzen data-testid, da es am eindeutigsten ist
# 		contact_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="contact-button"]')))
		
# 		# 2. Den Button in den Sichtbereich scrollen (manchmal wichtig für Selenium)
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contact_button)
# 		time.sleep(1) # Kurze Pause für die Optik
		
# 		# 3. Klicken
# 		contact_button.click()
# 		print("Button 'Nachricht' wurde geklickt.")

# 	except Exception as e:
# 		# Erstellt ein Beweisfoto im gleichen Ordner
# 		driver.save_screenshot("fehler_ansicht.png")
# 		print(f"Fehler beim Klicken des Buttons: {e}")
		

# 	# textarea für anschreiben finden
# 	try:
# 		# 1. Warte, bis das Textfeld erscheint
# 		# Wir nutzen die ID "message", da sie sehr stabil ist
# 		message_field = wait.until(EC.presence_of_element_located((By.ID, "message")))
		
# 		# 2. In das Feld scrollen, falls es ein langes Formular ist
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", message_field)
# 		time.sleep(1)

# 		# 3. Das Feld leeren, falls ein Standardtext drinsteht
# 		message_field.clear()

# 		# 4. Deine Nachricht definieren
# 		my_message = "Sehr geehrte D und H,\n\nbla..."

# 		# 5. "Menschliches" Tippen (optional, aber sicherer gegen Bot-Erkennung)
# 		for char in my_message:
# 			message_field.send_keys(char)
# 			# Zufällige Pause zwischen 0.02 und 0.1 Sekunden pro Buchstabe
# 			time.sleep(random.uniform(0.02, 0.1))

# 		print("Nachricht erfolgreich eingetippt!")

# 		# 6. Der letzte Schritt: Den Senden-Button finden
# 		# Meistens hat er data-testid="send-button" oder ähnliches.
# 		# Du kannst ihn suchen, aber noch nicht klicken, um erst zu testen.

# 	except Exception as e:
# 		print(f"Fehler beim Ausfüllen des Textfelds: {e}")

# 	#optionale drop downs auswählen ----
# 	##einzugsdatum
# 	try:
# 		# 1. Warte, bis das Dropdown sichtbar ist
# 		# Wir nutzen data-testid, da es am stabilsten ist
# 		dropdown_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="moveInDateType"]')))
		
# 		# 2. Scrolle zum Dropdown
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_element)
# 		time.sleep(random.uniform(0.5, 1.2))

# 		# 3. Nutze die Select-Klasse von Selenium (der "saubere" Weg)
# 		select = Select(dropdown_element)
		
# 		# 4. Wähle "FLEXIBLE" (das ist der 'value' aus deinem HTML)
# 		# Wir klicken nicht direkt, sondern lassen Selenium die Logik übernehmen
# 		select.select_by_value("FLEXIBLE")
		
# 		print("Einzugsdatum 'flexibel' ausgewählt.")

# 	except Exception as e:
# 		# Falls das Dropdown gar nicht da ist (passiert oft bei IS24 je nach Anbieter)
# 		print(f"Dropdown nicht gefunden oder Fehler: {e}")


# 	##haushaltsgröße
# 	try:
# 		# 1. Warte, bis das Dropdown für Personen sichtbar ist
# 		persons_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="numberOfPersons"]')))
		
# 		# 2. Kurze Pause vor der nächsten Interaktion (menschliches Zögern)
# 		time.sleep(random.uniform(0.6, 1.4))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", persons_dropdown)
		
# 		# 4. Auswahl treffen
# 		select_persons = Select(persons_dropdown)
# 		select_persons.select_by_value("ONE_PERSON")
		
# 		print("Haushaltsgröße 'Einpersonenhaushalt' ausgewählt.")

# 	except Exception as e:
# 		# Dieses Feld fehlt oft, wenn man bereits ein Profil hinterlegt hat,
# 		# in dem die Personenanzahl gespeichert ist. Daher fangen wir den Fehler ab.
# 		print(f"Personen-Dropdown nicht gefunden (evtl. bereits vorausgefüllt): {e}")
		

# 	##haustoere?
# 	try:
# 		# 1. Warte auf das Haustier-Dropdown
# 		pets_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="hasPets"]')))
		
# 		# 2. Kurze Pause für die "menschliche" Optik
# 		time.sleep(random.uniform(0.5, 1.1))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pets_dropdown)
		
# 		# 4. "Nein" auswählen (Value ist "FALSE" laut deinem HTML)
# 		select_pets = Select(pets_dropdown)
# 		select_pets.select_by_value("FALSE")
		
# 		print("Haustiere: 'Nein' ausgewählt.")

# 	except Exception as e:
# 		# Oft wird diese Frage übersprungen, wenn im Inserat Haustiere explizit erlaubt/verboten sind
# 		print(f"Haustier-Dropdown nicht gefunden: {e}")


# 	## Beschäftigungsstatus (Befristet/Unbefristet)
# 	try:
# 		# 1. Warte, bis das Dropdown für den Status klickbar ist
# 		# Wir nutzen data-testid="employmentStatus", da das am sichersten ist
# 		employment_status_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="employmentStatus"]')))
		
# 		# 2. Kurze "menschliche" Pause
# 		time.sleep(random.uniform(0.5, 1.2))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", employment_status_dropdown)
		
# 		# 4. Auswahl treffen
# 		select_status = Select(employment_status_dropdown)
		
# 		# Wir wählen den Wert "INDEFINITE_PERIOD" (Unbefristet)
# 		select_status.select_by_value("INDEFINITE_PERIOD")
		
# 		print("Beschäftigungsstatus 'Unbefristet' ausgewählt.")

# 	except Exception as e:
# 		# Das Feld taucht oft nur auf, wenn man vorher "Angestellter" gewählt hat
# 		print(f"Beschäftigungsstatus-Dropdown nicht gefunden oder bereits ausgefüllt")


# 	## Gewerbliche Nutzung?
# 	try:
# 		# 1. Warte auf das Dropdown für gewerbliche Zwecke
# 		commercial_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="forCommercialPurposes"]')))
		
# 		# 2. Kurze Pause für die menschliche Optik
# 		time.sleep(random.uniform(0.4, 0.8))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", commercial_dropdown)
		
# 		# 4. "Nein" auswählen (Value ist "FALSE")
# 		select_commercial = Select(commercial_dropdown)
# 		select_commercial.select_by_value("FALSE")
		
# 		print("Gewerbliche Nutzung: 'Nein' ausgewählt.")

# 	except Exception as e:
# 		# Dieses Feld taucht meist nur bei Wohnungen auf, die auch als Büro nutzbar wären
# 		print(f"Gewerbe-Dropdown nicht gefunden oder übersprungen: {e}")

		

# 	## Mietschulden vorhanden?
# 	try:
# 		# 1. Warte auf das Dropdown für Mietschulden
# 		rent_arrears_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="rentArrears"]')))
		
# 		# 2. Kurze Pause
# 		time.sleep(random.uniform(0.3, 0.7))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rent_arrears_dropdown)
		
# 		# 4. "Nein" auswählen (Value ist "FALSE")
# 		select_arrears = Select(rent_arrears_dropdown)
# 		select_arrears.select_by_value("FALSE")
		
# 		print("Mietschulden: 'Nein' ausgewählt.")

# 	except Exception as e:
# 		# Wird oft übersprungen, wenn man eine Schufa-Auskunft im Profil hinterlegt hat
# 		print(f"Mietschulden-Dropdown nicht gefunden oder übersprungen: {e}")
# #

# 	## Insolvenzverfahren?
# 	try:
# 		# 1. Warte auf das Dropdown für Insolvenzverfahren
# 		insolvency_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="insolvencyProcess"]')))
		
# 		# 2. Kurze Pause
# 		time.sleep(random.uniform(0.3, 0.7))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", insolvency_dropdown)
		
# 		# 4. "Nein" auswählen (Value ist "FALSE")
# 		select_insolvency = Select(insolvency_dropdown)
# 		select_insolvency.select_by_value("FALSE")
		
# 		print("Insolvenzverfahren: 'Nein' ausgewählt.")

# 	except Exception as e:
# 		print(f"Insolvenz-Dropdown nicht gefunden oder übersprungen: {e}")


# 	## Raucher?
# 	try:
# 		# 1. Warte auf das Dropdown für Raucher-Status
# 		smoker_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="smoker"]')))
		
# 		# 2. Kurze Pause
# 		time.sleep(random.uniform(0.3, 0.6))
		
# 		# 3. Zum Element scrollen
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", smoker_dropdown)
		
# 		# 4. "Nein" auswählen (Value ist "FALSE")
# 		select_smoker = Select(smoker_dropdown)
# 		select_smoker.select_by_value("FALSE")
		
# 		print("Raucher: 'Nein' ausgewählt.")

# 	except Exception as e:
# 		print(f"Raucher-Dropdown nicht gefunden oder bereits ausgefüllt: {e}")

# 	##angestellter
# 	try:
# 		# 1. Warte auf das Beschäftigungs-Dropdown
# 		employment_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="employmentRelationship"]')))
		
# 		# 2. Scrolle zum Element
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", employment_dropdown)
# 		time.sleep(random.uniform(0.5, 1.0))

# 		# 3. Prüfe den aktuellen Wert
# 		select_employment = Select(employment_dropdown)
# 		current_selection = select_employment.first_selected_option.get_attribute("value")

# 		# 4. Nur auswählen, wenn noch nicht "PUBLIC_EMPLOYEE" eingestellt ist
# 		if current_selection != "PUBLIC_EMPLOYEE":
# 			select_employment.select_by_value("PUBLIC_EMPLOYEE")
# 			print("Beschäftigungsverhältnis auf 'Angestellte:r' gesetzt.")
# 		else:
# 			print("Beschäftigungsverhältnis war bereits korrekt vorausgefüllt.")

# 	except Exception as e:
# 		print(f"Beschäftigungs-Dropdown nicht gefunden oder Fehler: {e}")

# 	##einkommen textfeld
# 	try:
# 		# 1. Warte, bis das Textfeld für den Betrag sichtbar ist
# 		income_amount_field = wait.until(EC.presence_of_element_located((By.ID, "incomeAmount")))
		
# 		# 2. Scrolle zum Feld
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", income_amount_field)
# 		time.sleep(random.uniform(0.5, 1.0))

# 		# 3. Feld leeren
# 		# .clear() funktioniert bei ImmoScout manchmal nicht perfekt, 
# 		# daher nutzen wir zusätzlich Control+A + Backspace zur Sicherheit
# 		income_amount_field.send_keys(uc.Keys.COMMAND + "a") # Für Mac
# 		income_amount_field.send_keys(uc.Keys.BACKSPACE)
# 		time.sleep(0.5)

# 		# 4. Wunschbetrag eintragen (als String ohne Punkte/Kommas)
# 		mein_gehalt = "2700"
		
# 		for char in mein_gehalt:
# 			income_amount_field.send_keys(char)
# 			time.sleep(random.uniform(0.1, 0.2))

# 		print(f"Netto-Einkommen Betrag '{mein_gehalt}' eingetragen.")

# 	except Exception as e:
# 		print(f"Einkommen-Betrag-Feld nicht gefunden oder Fehler: {e}")

# 	##gehalt dropdown 
# 	try:
# 		# 1. Warte auf das Einkommens-Dropdown
# 		income_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="income"]')))
		
# 		# 2. Scrolle zum Element
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", income_dropdown)
# 		time.sleep(random.uniform(0.4, 0.9))

# 		# 3. Prüfe den aktuellen Wert
# 		select_income = Select(income_dropdown)
# 		current_income = select_income.first_selected_option.get_attribute("value")

# 		# 4. Nur auswählen, wenn noch nicht der gewünschte Bereich eingestellt ist
# 		target_income = "OVER_2000_UPTO_3000"
		
# 		if current_income != target_income:
# 			select_income.select_by_value(target_income)
# 			print(f"Einkommen auf '{target_income}' gesetzt.")
# 		else:
# 			print("Einkommen war bereits korrekt vorausgefüllt.")

# 	except Exception as e:
# 		print(f"Einkommens-Dropdown nicht gefunden oder Fehler: {e}")

# 	##bewerbungsunterlagen
# 	try:
# 		# 1. Warte auf das "Bewerbermappe"-Dropdown
# 		package_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="applicationPackageCompleted"]')))
		
# 		# 2. Scrolle zum Element
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_dropdown)
# 		time.sleep(random.uniform(0.5, 0.9))

# 		# 3. Auswahl treffen (Value ist "TRUE" laut HTML)
# 		select_package = Select(package_dropdown)
# 		select_package.select_by_value("TRUE")
		
# 		print("Bewerbermappe: 'Vorhanden' ausgewählt.")

# 	except Exception as e:
# 		# Dieses Feld wird oft automatisch ausgefüllt, wenn dein Plus-Profil aktiv ist
# 		print(f"Bewerbermappe-Dropdown nicht gefunden oder bereits ausgefüllt: {e}")


# 	#ABSCHICKEN
# 	try:
# 		# 1. Warte, bis der Abschicken-Button klickbar ist
# 		# Wir suchen nach einem Button mit type='submit', der die Klasse für den Primär-Button hat
# 		submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].Button_button-primary__6QTnx")))
		
# 		# 2. Ein letztes Mal scrollen und eine kurze "menschliche" Pause
# 		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
# 		time.sleep(random.uniform(1.0, 2.0))
		
# 		# 3. DER FINALE KLICK
# 		# submit_button.click() 
# 		print("KLICK: Die Bewerbung wurde (theoretisch) abgeschickt!")

# 	except Exception as e:
# 		print(f"Fehler beim Finden des Abschicken-Buttons: {e}")

# 	time.sleep(random.uniform(2.2, 5.6))
# 	driver.quit()


# apply_to_listing(URL)


# # Loop zum Offenhalten
# while True:
#     time.sleep(10)