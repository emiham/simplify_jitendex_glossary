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


def simplify_note(note):
    glossary_field = mw.addonManager.getConfig(__name__)["glossary_field"]
    assert glossary_field in note.keys()

    sense_separator = mw.addonManager.getConfig(__name__)["sense_separator"]
    subsense_separator = mw.addonManager.getConfig(__name__)["subsense_separator"]

    soup = BeautifulSoup(note[glossary_field], "html.parser")
    definitions = []


    content = soup.findAll(attrs={"data-sc-content": "glossary"})
    if content:
        for glossary in content:
            glosses = [item.get_text() for item in glossary.findAll("li")]

            explanation = glossary.find_next(attrs={"data-sc-content": "info-gloss"})
            if explanation:
                explanation = explanation.get_text(strip=True, separator=" ")
                explanation = explanation.replace("Explanation", "", 1).strip()
                definitions.append(subsense_separator.join(glosses) + f" ({explanation})")

            else:
                definitions.append(subsense_separator.join(glosses))

        note[glossary_field] = sense_separator.join(definitions)
    return note


def on_flush_note(note):
    if mw.addonManager.getConfig(__name__)["modify_new"]:
        simplify_note(note)
    return


def simplify_notes(browser):
    note_ids = browser.selectedNotes()
    if not note_ids:
        tooltip(tr.browsing_no_selection(), period=2000)
        return

    notes = []
    undo = mw.col.add_custom_undo_entry(NAME)
    mw.progress.start()
    for note_id in note_ids:
        notes.append(simplify_note(mw.col.get_note(note_id)))

    mw.col.update_notes(notes)
    mw.col.merge_undo_entries(undo)
    tooltip(tr.browsing_notes_updated(len(notes)), period=2000)
    mw.progress.finish()
    mw.reset()


gui_hooks.browser_menus_did_init.append(setup_menu)
hooks.note_will_flush.append(on_flush_note)
