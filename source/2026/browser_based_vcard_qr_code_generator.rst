.. meta::
    :date: 2026-05-25

Browser-Based vCard QR Code Generator
=====================================

|pagedate|

.. tags:: JavaScript, QR Code, SVG, Utility, Frontend

This is a single HTML file that turns contact details into a
`vCard <https://datatracker.ietf.org/doc/html/rfc2426>`_ QR code and saves it
as a scalable SVG — handy for business cards, signage, or anything headed to
print. It runs entirely in your browser with no internet connection, so nothing
you type ever leaves your device.

Opening It
----------

`Open the generator </_static/files/2026/browser_based_vcard_qr_code_generator/contact-qr-studio.html>`__
in your browser, or download that file and open a local copy — it behaves the
same either way, since the whole thing runs client-side. The contact form is on
the left; the QR code, the download buttons, and the render options are on the
right. The code re-renders automatically whenever you change a field — there is
no "generate" button to press.

Entering a Contact
------------------

Fill in whatever applies: name, organization, title, address, website, and a
note. Every field is optional, and blank ones are simply left out of the code.
As you type, the preview and the vCard payload beneath it update live.

Phones and Emails
-----------------

Use **+ Add phone** and **+ Add email** to add rows, and the **×** on a row to
remove it. Each row has a type, an optional custom label, and a primary star.

Types and Labels
^^^^^^^^^^^^^^^^^

Pick a **type** from the dropdown — Mobile, Work, Home, and so on. To give an
entry a custom name like *Store*, type it into the **label** field on the row.

For an entry you really want to read as its label, set the type to
**None / label only**. On Android a standard type can override the label, so
dropping the type lets the label win. iOS shows the label either way.

The Primary Star
^^^^^^^^^^^^^^^^

Tap the **★** to mark one phone and one email as primary. Whatever imports the
card treats that entry as the default.

Country Codes
^^^^^^^^^^^^^

Phone rows have a country picker; search it by country name or dial code. If you
paste or type a number that begins with ``+``, the tool detects the country and
strips the prefix for you, leaving just the local number.

Render Options
--------------

Below the QR code:

* **Error correction** (L/M/Q/H) — higher levels survive more wear and dirt but
  produce a denser code. ``M`` is a sensible default; drop to ``L`` if a long
  contact won't fit.
* **Module px** — the pixel size of each square. The output is SVG, so it stays
  sharp at any size; this only sets the nominal dimensions.
* **Color** — choose a foreground color, or use the Ink and Big Frog green
  presets. **Transparent bg** removes the white background, which is useful when
  placing the code over artwork.

Saving Your Work
----------------

Everything you enter is saved in your browser automatically, so the contact is
still there when you reopen the file. **Clear all fields** wipes both the form
and the saved copy.

**Note:** the saved copy is tied to the specific browser and file location.
Moving or renaming the file starts fresh, and some browsers are strict about
storage on ``file://`` URLs — serving the file over ``http`` avoids that.

Exporting
---------

* **Download SVG** — the QR code as a vector file, for print or design tools.
* **Download .vcf** — the raw contact card, to import or share directly.
* **Copy vCard** — copies the text payload to your clipboard.

Before You Print
----------------

**Always scan and import the finished code on a real phone before sending
anything to print.** A code that looks fine but imports the wrong details is
worse than none at all. One harmless quirk to expect: on Windows the country
flags appear as two-letter codes instead of emoji — the dial code is always
shown beside them, so nothing is actually missing.

|cta|
|disqus|