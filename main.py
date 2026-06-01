import flet as ft
import os
import shutil
import cv2
import imagehash
from PIL import Image, ImageFile
import numpy as np
import uuid
import tkinter as tk
from tkinter import filedialog
import asyncio
import threading
import gc

# Prevents PIL from crashing on truncated or corrupted images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# --- CONFIGURATION ---
UNSCHAERFE_SCHWELLENWERT = 100.0
HAMMING_DISTANZ_LIMIT = 8

# --- COLOR PALETTES (Light & Dark Mode) ---
PURPLE = "#8B5CF6"
DANGER = "#FF5555"

THEME = {
    "dark": {
        "bg": "#0B0C10",
        "card": "#15161E",
        "card_inner": "#1A1B26",
        "text_main": "#F8F8F2",
        "text_muted": "#6272A4"
    },
    "light": {
        "bg": "#F3F4F6",
        "card": "#FFFFFF",
        "card_inner": "#E5E7EB",
        "text_main": "#111827",
        "text_muted": "#6B7280"
    }
}

# --- TRANSLATIONS ---
TEXTS = {
    "DE": {
        "sub": "IMAGE ANALYZER",
        "desc": "Scanne deine Mediathek nach Duplikaten und unscharfen Bildern.",
        "col_blur": "📉 Unscharf",
        "col_dup": "👥 Duplikate",
        "col_prev": "VORSCHAU",
        "prev_empty": "Wähle ein Bild für die Vorschau",
        "btn_scan": "ORDNER SCANNEN",
        "btn_blur": "UNSCHARFE VERSCHIEBEN",
        "btn_dup": "DUPLIKATE VERSCHIEBEN",
        "btn_keep": "BILD BEHALTEN",
        "working": "ARBEITE...",
        "done": "ERLEDIGT",
        "search": "Suche Bilder...",
        "no_imgs": "Keine Bilder gefunden.",
        "err_read": "Fehler beim Lesen:",
        "analyzing": "Analysiere Bild {i} von {total}...",
        "copy": "➔ Kopie",
        "finished": "Analyse fertig! {b} unscharf, {d} Duplikate.",
        "moved": "{n} Bilder erfolgreich verschoben!",
        "dialog": "Wähle deinen Bilder-Ordner",
        "crit_err": "Kritischer Fehler:"
    },
    "EN": {
        "sub": "IMAGE ANALYZER",
        "desc": "Scan your library for duplicates and blurred images.",
        "col_blur": "📉 Blurred",
        "col_dup": "👥 Duplicates",
        "col_prev": "PREVIEW",
        "prev_empty": "Select an image for preview",
        "btn_scan": "SCAN FOLDER",
        "btn_blur": "MOVE BLURRED",
        "btn_dup": "MOVE DUPLICATES",
        "btn_keep": "KEEP IMAGE",
        "working": "WORKING...",
        "done": "DONE",
        "search": "Searching images...",
        "no_imgs": "No images found.",
        "err_read": "Error reading:",
        "analyzing": "Analyzing image {i} of {total}...",
        "copy": "➔ Copy",
        "finished": "Analysis complete! {b} blurred, {d} duplicates.",
        "moved": "{n} images moved successfully!",
        "dialog": "Select your image folder",
        "crit_err": "Critical Error:"
    },
    "FR": {
        "sub": "ANALYSEUR D'IMAGES",
        "desc": "Analysez votre bibliothèque pour trouver des doublons et des images floues.",
        "col_blur": "📉 Floues",
        "col_dup": "👥 Doublons",
        "col_prev": "APERÇU",
        "prev_empty": "Sélectionnez une image pour l'aperçu",
        "btn_scan": "SCANNER DOSSIER",
        "btn_blur": "DÉPLACER FLOUES",
        "btn_dup": "DÉPLACER DOUBLONS",
        "btn_keep": "GARDER L'IMAGE",
        "working": "TRAVAIL...",
        "done": "TERMINÉ",
        "search": "Recherche d'images...",
        "no_imgs": "Aucune image trouvée.",
        "err_read": "Erreur de lecture :",
        "analyzing": "Analyse de l'image {i} sur {total}...",
        "copy": "➔ Copie",
        "finished": "Analyse terminée ! {b} floues, {d} doublons.",
        "moved": "{n} images déplacées avec succès !",
        "dialog": "Sélectionnez votre dossier d'images",
        "crit_err": "Erreur Critique:"
    },
    "ES": {
        "sub": "ANALIZADOR DE IMÁGENES",
        "desc": "Escanea tu biblioteca en busca de duplicados e imágenes borrosas.",
        "col_blur": "📉 Borrosas",
        "col_dup": "👥 Duplicados",
        "col_prev": "VISTA PREVIA",
        "prev_empty": "Selecciona una imagen para la vista previa",
        "btn_scan": "ESCANEAR CARPETA",
        "btn_blur": "MOVER BORROSAS",
        "btn_dup": "MOVER DUPLICADOS",
        "btn_keep": "CONSERVAR IMAGEN",
        "working": "TRABAJANDO...",
        "done": "HECHO",
        "search": "Buscando imágenes...",
        "no_imgs": "No se encontraron imágenes.",
        "err_read": "Error al leer:",
        "analyzing": "Analizando imagen {i} de {total}...",
        "copy": "➔ Copia",
        "finished": "¡Análisis completo! {b} borrosas, {d} duplicados.",
        "moved": "¡{n} imágenes movidas con éxito!",
        "dialog": "Selecciona tu carpeta de imágenes",
        "crit_err": "Error Crítico:"
    },
    "IT": {
        "sub": "ANALIZZATORE DI IMMAGINI",
        "desc": "Scansiona la tua libreria per trovare duplicati e immagini sfocate.",
        "col_blur": "📉 Sfocate",
        "col_dup": "👥 Duplicati",
        "col_prev": "ANTEPRIMA",
        "prev_empty": "Seleziona un'immagine per l'anteprima",
        "btn_scan": "SCANSIONA CARTELLA",
        "btn_blur": "SPOSTA SFOCATE",
        "btn_dup": "SPOSTA DUPLICATI",
        "btn_keep": "MANTIENI IMMAG.",
        "working": "ELABORAZIONE...",
        "done": "FATTO",
        "search": "Ricerca immagini...",
        "no_imgs": "Nessuna immagine trovata.",
        "err_read": "Errore di lettura:",
        "analyzing": "Analisi immagine {i} di {total}...",
        "copy": "➔ Copia",
        "finished": "Analisi completata! {b} sfocate, {d} duplicati.",
        "moved": "{n} immagini spostate con successo!",
        "dialog": "Seleziona la cartella delle immagini",
        "crit_err": "Errore Critico:"
    },
    "RU": {
        "sub": "АНАЛИЗАТОР ИЗОБРАЖЕНИЙ",
        "desc": "Сканируйте библиотеку на дубликаты и размытые фото.",
        "col_blur": "📉 Размытые",
        "col_dup": "👥 Дубликаты",
        "col_prev": "ПРЕДПРОСМОТР",
        "prev_empty": "Выберите фото для предпросмотра",
        "btn_scan": "СКАНИРОВАТЬ ПАПКУ",
        "btn_blur": "ПЕРЕМЕСТИТЬ РАЗМЫТЫЕ",
        "btn_dup": "ПЕРЕМЕСТИТЬ ДУБЛИКАТЫ",
        "btn_keep": "ОСТАВИТЬ ФОТО",
        "working": "РАБОТАЮ...",
        "done": "ГОТОВО",
        "search": "Поиск изображений...",
        "no_imgs": "Изображения не найдены.",
        "err_read": "Ошибка чтения:",
        "analyzing": "Анализ фото {i} из {total}...",
        "copy": "➔ Копия",
        "finished": "Анализ завершен! {b} размытых, {d} дубликатов.",
        "moved": "{n} фото успешно перемещено!",
        "dialog": "Выберите папку с изображениями",
        "crit_err": "Критическая ошибка:"
    }
}

def main(page: ft.Page):
    # --- WINDOW SETUP & ANTI-CRASH LIMITS ---
    page.title = "Jayace PicClean"
    page.padding = 30
    page.vertical_alignment = "center"
    page.theme_mode = "dark"

    # Instructs Flet to load the app window icon
    try:
        page.window.icon = "icon.png"
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 900
        page.window.min_height = 600
    except Exception:
        pass

    state = {
        "ordner": "",
        "unscharf": [],
        "duplikate": [],
        "vorschau_pfad": None,
        "vorschau_kategorie": None,
        "lang": "DE",
        "is_dark": True,
        "is_working": False # LOCK SYSTEM: Prevents race conditions from double-clicks
    }

    # --- DECLARE UI ELEMENTS ---
    txt_badge = ft.Text("", size=10, weight="bold", text_align="center")
    txt_title = ft.Text("P I C C L E A N", size=32, weight="w900", italic=True, text_align="center")
    txt_desc = ft.Text("", size=14, text_align="center")

    txt_col_blur = ft.Text("", size=16, weight="bold", color=DANGER, text_align="center")
    txt_col_dup = ft.Text("", size=16, weight="bold", color=PURPLE, text_align="center")
    txt_col_prev = ft.Text("", size=12, weight="bold", text_align="center")

    status_text = ft.Text("", size=12, visible=False, text_align="center")
    progress_bar = ft.ProgressBar(width=400, color=PURPLE, value=0, visible=False)

    txt_prev_empty = ft.Text("", italic=True, text_align="center")
    badge_container = ft.Container(content=txt_badge, padding=ft.Padding(15, 5, 15, 5), border_radius=20, alignment=ft.Alignment(0,0))

    card_blur = ft.Container(expand=2, padding=20, border_radius=15, alignment=ft.Alignment(0, -1))
    card_dup = ft.Container(expand=2, padding=20, border_radius=15, alignment=ft.Alignment(0, -1))
    card_prev = ft.Container(expand=3, padding=20, border_radius=15, alignment=ft.Alignment(0, -1))

    preview_container = ft.Container(content=txt_prev_empty, alignment=ft.Alignment(0, 0), expand=True)

    list_unscharf = ft.ListView(expand=True, spacing=10)
    list_duplikate = ft.ListView(expand=True, spacing=10)

    # --- THEME & LANGUAGE UPDATERS ---
    def apply_theme():
        t = THEME["dark"] if state["is_dark"] else THEME["light"]

        page.bgcolor = t["bg"]
        page.theme_mode = "dark" if state["is_dark"] else "light"

        badge_container.bgcolor = t["card_inner"]
        txt_badge.color = t["text_muted"]
        txt_title.color = t["text_main"]
        txt_desc.color = t["text_muted"]
        txt_col_prev.color = t["text_muted"]
        status_text.color = t["text_muted"]
        txt_prev_empty.color = t["text_muted"]
        progress_bar.bgcolor = t["card_inner"]

        card_blur.bgcolor = t["card"]
        card_dup.bgcolor = t["card"]
        card_prev.bgcolor = t["card"]

        btn_clean_blur.bgcolor = t["card_inner"]
        btn_clean_dup.bgcolor = t["card_inner"]

        btn_keep.bgcolor = t["card_inner"]
        btn_keep.content.color = t["text_main"]

        for item in list_unscharf.controls:
            item.bgcolor = t["card_inner"]
            item.content.color = t["text_main"]
        for item in list_duplikate.controls:
            item.bgcolor = t["card_inner"]
            item.content.color = t["text_muted"]

        theme_btn.content.value = "☀️" if state["is_dark"] else "🌙"
        page.update()

    def apply_language():
        l = state["lang"]
        t = TEXTS[l]

        txt_badge.value = t["sub"]
        txt_desc.value = t["desc"]
        txt_col_blur.value = t["col_blur"]
        txt_col_dup.value = t["col_dup"]
        txt_col_prev.value = t["col_prev"]

        if state["vorschau_pfad"] is None:
            txt_prev_empty.value = t["prev_empty"]

        btn_scan.content.value = t["btn_scan"]
        btn_clean_blur.content.value = t["btn_blur"]
        btn_clean_dup.content.value = t["btn_dup"]
        btn_keep.content.value = t["btn_keep"]

        # Highlight the currently active language
        for btn in lang_row.controls:
            if btn.content.value == l:
                btn.content.color = PURPLE
            else:
                btn.content.color = THEME["dark" if state["is_dark"] else "light"]["text_muted"]

        # Live translation for dynamic list items
        for item in list_duplikate.controls:
            dateiname = item.data["dateiname"]
            item.content.value = f"{dateiname} {t['copy']}"

        page.update()

    def toggle_theme(e):
        state["is_dark"] = not state["is_dark"]
        apply_theme()
        apply_language()

    def set_lang(lang_code):
        state["lang"] = lang_code
        apply_theme()
        apply_language()

    # --- TOP BAR ---
    theme_btn = ft.Container(
        content=ft.Text("☀️", size=18),
        padding=10, border_radius=10, ink=True,
        on_click=toggle_theme
    )

    lang_row = ft.Row([
        ft.Container(content=ft.Text("EN", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("EN")),
        ft.Container(content=ft.Text("DE", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("DE")),
        ft.Container(content=ft.Text("FR", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("FR")),
        ft.Container(content=ft.Text("ES", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("ES")),
        ft.Container(content=ft.Text("IT", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("IT")),
        ft.Container(content=ft.Text("RU", weight="bold"), padding=10, ink=True, on_click=lambda _: set_lang("RU"))
    ], spacing=0)

    top_bar = ft.Row([theme_btn, ft.Container(expand=True), lang_row], alignment="spaceBetween")

    # --- PREVIEW ---
    def zeige_vorschau(pfad, kategorie):
        state["vorschau_pfad"] = pfad
        state["vorschau_kategorie"] = kategorie

        preview_container.content = ft.Image(src=pfad, fit="contain", border_radius=10, expand=True)

        if not state["is_working"]:
            btn_keep.visible = True

        page.update()

    def reset_vorschau():
        state["vorschau_pfad"] = None
        state["vorschau_kategorie"] = None
        txt_prev_empty.value = TEXTS[state["lang"]]["prev_empty"]
        preview_container.content = txt_prev_empty
        btn_keep.visible = False
        page.update()

    # --- MAIN LOGIC ---
    def hole_ordner_pfad():
        ordner_pfad = [""]
        def _dialog():
            root = None
            try:
                # Fallback to native OS dialog, avoids Flet bugs
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                dialog_titel = TEXTS[state["lang"]]["dialog"]
                auswahl = filedialog.askdirectory(title=dialog_titel)
                if auswahl:
                    ordner_pfad[0] = os.path.normpath(auswahl)
            except Exception:
                pass
            finally:
                if root:
                    try:
                        root.destroy()
                    except:
                        pass
        t = threading.Thread(target=_dialog)
        t.start()
        t.join()
        return ordner_pfad[0]

    def starte_ordner_auswahl(e):
        if state["is_working"]: return
        pfad = hole_ordner_pfad()
        if pfad:
            page.run_task(starte_analyse, pfad)

    async def starte_analyse(ordner_pfad):
        if state["is_working"]: return
        state["is_working"] = True
        l = state["lang"]

        try:
            state["ordner"] = ordner_pfad
            state["unscharf"].clear()
            state["duplikate"].clear()

            list_unscharf.controls.clear()
            list_duplikate.controls.clear()
            reset_vorschau()

            progress_bar.visible = True
            progress_bar.value = 0
            status_text.visible = True
            status_text.value = TEXTS[l]["search"]

            # Lock UI immediately
            btn_clean_blur.visible = False
            btn_clean_dup.visible = False
            btn_keep.visible = False

            btn_scan.disabled = True
            btn_scan.opacity = 0.5
            page.update()
            await asyncio.sleep(0.01) # Give the async event loop time to breathe

            unterstuetzte_formate = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')

            try:
                bilder = [os.path.join(ordner_pfad, f) for f in os.listdir(ordner_pfad)
                          if f.lower().endswith(unterstuetzte_formate)]
            except Exception:
                zeige_fehler(TEXTS[l]["err_read"])
                return

            total = len(bilder)
            if total == 0:
                zeige_fehler(TEXTS[l]["no_imgs"])
                return

            hashes = {}

            for i, pfad in enumerate(bilder):
                l = state["lang"]
                dateiname = os.path.basename(pfad)
                status_text.value = TEXTS[l]["analyzing"].format(i=i+1, total=total)

                ist_duplikat = False

                try:
                    with Image.open(pfad) as img_pil:
                        # LOW-END PC HACK: Resize image drastically before hashing to save RAM and CPU
                        img_pil.thumbnail((256, 256))
                        v_hash = imagehash.phash(img_pil)

                    for reg_hash, kopf_pfad in hashes.items():
                        if v_hash - reg_hash <= HAMMING_DISTANZ_LIMIT:
                            ist_duplikat = True
                            break

                    if ist_duplikat:
                        state["duplikate"].append(pfad)
                        item = erstelle_listen_eintrag(pfad, dateiname, kategorie="duplikate", is_dup=True)
                        list_duplikate.controls.append(item)
                    else:
                        hashes[v_hash] = pfad
                except Exception:
                    pass

                if not ist_duplikat:
                    try:
                        img_array = np.fromfile(pfad, np.uint8)
                        if img_array is not None and img_array.size > 0:
                            img_cv = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
                            if img_cv is not None:
                                varianz = cv2.Laplacian(img_cv, cv2.CV_64F).var()
                                if varianz < UNSCHAERFE_SCHWELLENWERT:
                                    state["unscharf"].append(pfad)
                                    item = erstelle_listen_eintrag(pfad, dateiname, kategorie="unscharf", is_dup=False)
                                    list_unscharf.controls.append(item)
                                del img_cv # Free RAM
                        del img_array # Free RAM
                    except Exception:
                        pass

                # Prevent Memory Leaks on massive folders (10,000+ images)
                if i % 100 == 0:
                    gc.collect()

                progress_bar.value = (i + 1) / total
                # Update UI every 10 images to keep it smooth on low-end PCs
                if i % 10 == 0 or i == total - 1:
                    page.update()
                    await asyncio.sleep(0.001)

            status_text.value = TEXTS[l]["finished"].format(b=len(state['unscharf']), d=len(state['duplikate']))

        except Exception as e:
            zeige_fehler(f"{TEXTS[l]['crit_err']} {e}")

        finally:
            await reset_ui_nach_scan()
            state["is_working"] = False

    def erstelle_listen_eintrag(pfad, dateiname, kategorie, is_dup=False):
        t = THEME["dark"] if state["is_dark"] else THEME["light"]
        l = state["lang"]

        text_val = f"{dateiname} {TEXTS[l]['copy']}" if is_dup else dateiname
        farbe = t["text_muted"] if is_dup else t["text_main"]

        container = ft.Container(
            content=ft.Text(text_val, color=farbe, overflow="ellipsis", text_align="center"),
            padding=15,
            bgcolor=t["card_inner"],
            border_radius=8,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e, p=pfad, k=kategorie: zeige_vorschau(p, k),
            ink=True,
            data={"pfad": pfad, "dateiname": dateiname} # Stores path & name as a dictionary
        )
        return container

    async def reset_ui_nach_scan():
        l = state["lang"]
        progress_bar.visible = False
        btn_scan.disabled = False
        btn_scan.opacity = 1.0

        has_blur = len(state["unscharf"]) > 0
        has_dup = len(state["duplikate"]) > 0

        btn_clean_blur.visible = has_blur
        btn_clean_dup.visible = has_dup

        btn_clean_blur.disabled = False
        btn_clean_blur.opacity = 1.0
        btn_clean_dup.disabled = False
        btn_clean_dup.opacity = 1.0

        page.update()

    def zeige_fehler(nachricht):
        page.snack_bar = ft.SnackBar(ft.Text(nachricht, text_align="center"), bgcolor=DANGER)
        page.snack_bar.open = True
        page.update()

    # Action to KEEP a SINGLE image
    async def aktion_einzelnes_bild_behalten():
        if state["is_working"]: return

        pfad = state["vorschau_pfad"]
        kategorie = state["vorschau_kategorie"]

        if not pfad or not kategorie: return

        # 1. Remove image from internal list
        if pfad in state[kategorie]:
            try:
                state[kategorie].remove(pfad)
            except ValueError:
                pass

        # 2. Remove image from the UI list
        ziel_liste = list_unscharf if kategorie == "unscharf" else list_duplikate

        # Iterate over a copy of the list to allow live deletion
        for item in ziel_liste.controls[:]:
            if item.data["pfad"] == pfad:
                ziel_liste.controls.remove(item)
                break

        # 3. Clear preview & hide button
        reset_vorschau()

        # 4. Check if we need to hide the main 'Move' buttons
        btn_clean_blur.visible = len(state["unscharf"]) > 0
        btn_clean_dup.visible = len(state["duplikate"]) > 0

        page.update()

    async def raeume_auf(kategorie, button, list_view):
        if state["is_working"]: return
        if not state[kategorie]: return

        state["is_working"] = True
        l = state["lang"]

        try:
            reset_vorschau()

            # IMMEDIATE UI Feedback
            button.content.value = TEXTS[l]["working"]
            button.disabled = True
            button.opacity = 0.5
            page.update()
            await asyncio.sleep(0.01)

            target_dir = os.path.join(state["ordner"], f"_Aussortiert_{kategorie}")
            os.makedirs(target_dir, exist_ok=True)

            erfolgreich = 0
            for pfad in state[kategorie]:
                try:
                    base_name = os.path.basename(pfad)
                    ziel_pfad = os.path.join(target_dir, base_name)
                    if os.path.exists(ziel_pfad):
                        name, ext = os.path.splitext(base_name)
                        ziel_pfad = os.path.join(target_dir, f"{name}_{uuid.uuid4().hex[:6]}{ext}")
                    shutil.move(pfad, ziel_pfad)
                    erfolgreich += 1
                except Exception:
                    pass

                # Give the PC a moment to breathe every 5 images
                if erfolgreich % 5 == 0: await asyncio.sleep(0.001)

            state[kategorie].clear()
            list_view.controls.clear()

            # Hide button completely after successful move
            button.visible = False

            msg = TEXTS[l]["moved"].format(n=erfolgreich)
            page.snack_bar = ft.SnackBar(ft.Text(msg, text_align="center"), bgcolor=PURPLE)
            page.snack_bar.open = True

        except Exception as e:
            zeige_fehler(f"{TEXTS[l]['crit_err']} {e}")

        finally:
            page.update()
            state["is_working"] = False

    # --- BUTTONS ---
    btn_scan = ft.Container(
        content=ft.Text("", color="white", weight="bold", text_align="center"),
        bgcolor=PURPLE, border_radius=30, padding=20, alignment=ft.Alignment(0, 0),
        ink=True, on_click=starte_ordner_auswahl
    )

    # The Keep button: Appears below the preview, only when an image is selected
    btn_keep = ft.Container(
        content=ft.Text("", weight="bold", text_align="center"),
        border_radius=30, padding=20, alignment=ft.Alignment(0, 0),
        ink=True, visible=False,
        on_click=lambda _: page.run_task(aktion_einzelnes_bild_behalten)
    )

    btn_clean_blur = ft.Container(
        content=ft.Text("", color=DANGER, weight="bold", text_align="center"),
        border_radius=30, padding=20, alignment=ft.Alignment(0, 0),
        ink=True, visible=False,
        on_click=lambda _: page.run_task(raeume_auf, "unscharf", btn_clean_blur, list_unscharf)
    )

    btn_clean_dup = ft.Container(
        content=ft.Text("", color=PURPLE, weight="bold", text_align="center"),
        border_radius=30, padding=20, alignment=ft.Alignment(0, 0),
        ink=True, visible=False,
        on_click=lambda _: page.run_task(raeume_auf, "duplikate", btn_clean_dup, list_duplikate)
    )

    # --- BUILD LAYOUT ---
    header = ft.Column(
        controls=[badge_container, txt_title, txt_desc],
        horizontal_alignment="center", spacing=5
    )

    card_blur.content = ft.Column([txt_col_blur, list_unscharf], horizontal_alignment="center")
    card_dup.content = ft.Column([txt_col_dup, list_duplikate], horizontal_alignment="center")

    # Keep button sits logically and elegantly right below the image preview
    card_prev.content = ft.Column([txt_col_prev, preview_container, btn_keep], horizontal_alignment="center")

    main_content = ft.Row(
        expand=True,
        controls=[card_blur, card_dup, card_prev]
    )

    footer = ft.Row(
        controls=[btn_scan, ft.Container(expand=True), btn_clean_blur, btn_clean_dup],
        alignment="spaceBetween"
    )

    page.add(
        top_bar,
        header,
        ft.Column([progress_bar, status_text], horizontal_alignment="center"),
        main_content,
        footer
    )

    # Initial Setup (Applies start colors & language)
    apply_theme()
    apply_language()

if __name__ == "__main__":
    # LATEST FLET VERSION COMMAND:
    ft.run(main, assets_dir="assets")