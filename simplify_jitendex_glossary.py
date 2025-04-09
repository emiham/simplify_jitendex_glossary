from anki import hooks
from aqt import mw, gui_hooks
from aqt.qt import QKeySequence
from aqt.utils import tooltip, tr
from bs4 import BeautifulSoup

NAME = "Simplify Jitendex glossary"


def setup_menu(browser):
    browser.form.menuEdit.addSeparator()
    action = browser.form.menuEdit.addAction(NAME)
    action.setShortcut(QKeySequence("Ctrl+Alt+Shift+J"))
    action.triggered.connect(lambda _, b=browser: simplify_notes(b))


def simplify_field_content(field):
    sense_separator = mw.addonManager.getConfig(__name__)["sense_separator"]
    subsense_separator = mw.addonManager.getConfig(__name__)["subsense_separator"]

    soup = BeautifulSoup(field, "html.parser")
    definitions = []

    content = soup.findAll(attrs={"data-sc-content": "glossary"})
    if content:
        for glossary in content:
            glosses = [item.get_text() for item in glossary.findAll("li")]

            append_text = ""
            explanation = glossary.find_next(attrs={"data-sc-content": "info-gloss"})
            if explanation:
                explanation = explanation.get_text(strip=True, separator=" ")
                explanation = explanation.replace("Explanation", "", 1).strip()
                append_text +=  f" ({explanation})"

            note = glossary.find_next(attrs={"data-sc-content": "sense-note"})
            if note:
                note = note.get_text(strip=True, separator=" ")
                note = note.replace("Note", "", 1).strip()
                append_text +=  f" [{note}]"

            definitions.append(subsense_separator.join(glosses) + append_text)

        return sense_separator.join(definitions)


def simplify_note(note):
    glossary_field = mw.addonManager.getConfig(__name__)["glossary_field"]
    if glossary_field not in note.keys():
        return note

    simplified_field_content = simplify_field_content(note[glossary_field])
    if simplified_field_content and simplified_field_content != note[glossary_field]:
        note[glossary_field] = simplify_field_content(note[glossary_field])
    return note


def simplify_notes(browser):
    note_ids = browser.selectedNotes()
    if not note_ids:
        tooltip(tr.browsing_no_selection(), period=2000)
        return

    notes = []
    undo = mw.col.add_custom_undo_entry(NAME)
    mw.progress.start()
    glossary_field = mw.addonManager.getConfig(__name__)["glossary_field"]

    for note_id in note_ids:
        note = mw.col.get_note(note_id)
        if glossary_field in note.keys():
            simplified_field_content = simplify_field_content(note[glossary_field])
            if (
                simplified_field_content
                and simplified_field_content != note[glossary_field]
            ):
                notes.append(simplify_note(note))

    mw.col.update_notes(notes)
    mw.col.merge_undo_entries(undo)
    tooltip(tr.browsing_notes_updated(len(notes)), period=2000)
    mw.progress.finish()
    mw.reset()


def on_add_note(collection, note, deck_id):
    if mw.addonManager.getConfig(__name__)["modify_new"]:
        simplify_note(note)
    return


gui_hooks.browser_menus_did_init.append(setup_menu)
hooks.note_will_be_added.append(on_add_note)
