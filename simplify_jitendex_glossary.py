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


def simplify_notes(browser):
    glossary_field = mw.addonManager.getConfig(__name__)["glossary_field"]
    sense_separator = mw.addonManager.getConfig(__name__)["sense_separator"]
    subsense_separator = mw.addonManager.getConfig(__name__)["subsense_separator"]

    note_ids = browser.selectedNotes()
    if not note_ids:
        tooltip(tr.browsing_no_selection(), period=2000)
        return

    notes = []
    undo = mw.col.add_custom_undo_entry(NAME)
    mw.progress.start()
    for note_id in note_ids:
        note = mw.col.get_note(note_id)
        assert glossary_field in note.keys()
        soup = BeautifulSoup(note[glossary_field], "html.parser")
        definitions = []
        for glossary in soup.findAll(attrs={"data-sc-content": "glossary"}):
            glosses = [item.get_text() for item in glossary.findAll("li")]
            definitions.append(subsense_separator.join(glosses))

        note[glossary_field] = sense_separator.join(definitions)
        notes.append(note)

    mw.col.update_notes(notes)
    mw.col.merge_undo_entries(undo)
    mw.progress.finish()
    mw.reset()


gui_hooks.browser_menus_did_init.append(setup_menu)
