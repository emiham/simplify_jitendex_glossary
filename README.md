Jitendex adds a lot of information and styling to its glossaries. This addon
strips all that information, leaving only the definitions in plaintext.

## Usage

In the addon's settings, set `glossary_field` to the name of the field you want
to update. Optionally change the separator strings. If you don't want to
automatically format new cards, change `update_new` from `true` to `false`.
Note that if you overwrite the glossary field of an existing
note through Yomitan it won't get updated automatically

In the card browser, select the notes you want to update, and click "Simplify
Jitendex glossary" in the *Edit* menu.

Some words have an explanatory note, e.g. 見せ物. This will be added in
parentheses, as in the example below. There is another form of note, shown just
as *Note* in Jitendex. These will be added in square brackets.

## Example

### Jitendex definition

<img src="https://github.com/user-attachments/assets/5d767b6b-bfb7-4198-9a09-e48109b2c4b0" width=50% height=50%>

### Anki note content

```
misemono (type of Edo- and Meiji-period side show often held outdoors or in small temporarily erected shacks on temple and shrine grounds)
show; exhibition; spectacle; freakshow; side show
```
