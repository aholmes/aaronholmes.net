.. meta::
    :date: 2026-05-25

Browser-Based URL and vCard QR Code Generator
=============================================

|pagedate|

.. tags:: JavaScript, QR Code, SVG, Utility, Frontend

This is a single HTML file that turns a URL or
`vCard <https://datatracker.ietf.org/doc/html/rfc2426>`_ contact details into a
QR code and saves it as a scalable SVG - handy for business cards, signage, or
anything headed to print. It runs entirely in your browser with no internet
connection, so nothing you type ever leaves your device.

Opening It
----------

`Open the generator </_static/files/2026/browser_based_vcard_qr_code_generator/qr-studio.html>`__
in your browser, or access it right in this page, or download that file and open a local copy - it behaves the
same either way, since the whole thing runs client-side. The build form is on
the left; the QR code, the download buttons, and the design controls are on the
right. The code re-renders automatically whenever you change a field - there is
no "generate" button to press.

.. raw:: html

    <iframe src="/_static/files/2026/browser_based_vcard_qr_code_generator/qr-studio.html" style="width:100%;height:500px;"></iframe>


Build a QR For
--------------

The buttons at the top pick what the code encodes:

* **URL** - any link, including ``https://``, ``mailto:``, ``tel:``, ``sms:``,
  ``geo:``, and custom app schemes. This is the default.
* **Contact (vCard)** - a contact card a phone can import directly into its
  address book.

The form below changes to match. Each mode keeps its own saved data, so you can
switch back and forth without losing what you'd typed.

Entering a URL
--------------

In URL mode, paste your address into the **URL** field. The same scheme prefixes
that work on a phone work here too. The preview updates live, and the encoded
payload is shown beneath it. **Clear URL** wipes the field and its saved copy.

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

Pick a **type** from the dropdown - Mobile, Work, Home, and so on. To give an
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

Designing the Code
------------------

The QR card on the right has its design controls in two places:

* The block of options directly beneath **Download SVG / Copy / Reset design**
  controls the QR matrix itself - background, color, gradient.
* The **LOGO / SHAPE / FRAME** tabs below it control everything that wraps the
  QR - a center icon, the module shape, and the surrounding frame and label.

Every choice applies live, is saved in your browser, and survives reloads.

Background and Color
^^^^^^^^^^^^^^^^^^^^

* **Background** - check **Transparent** to drop the white plate. Useful when
  placing the code over artwork.
* **Color** - click the swatch to open the color picker (hue strip, a 2D
  saturation/value square, and an editable hex field).
* **Gradient** - check the box to fill the QR's dark modules with a gradient
  instead of a flat color. A **To** row appears for the end color and a
  **Linear / Radial** toggle. Linear adds a **Direction** row with an
  eight-point compass; pick where the second color should sit. Radial doesn't
  need a direction - it goes center to edge. Turning the gradient on auto-bumps
  error correction to ``H``, because the varying contrast across modules is
  harder for scanners to threshold. If you pick a color light enough that the
  contrast against the white background gets soft, the tool warns you with a
  toast.

Error Correction
^^^^^^^^^^^^^^^^

Below the QR's options is a small **L / M / Q / H** selector. Higher levels
survive more wear and dirt but produce a denser code. ``M`` is a sensible
default; drop to ``L`` if a long contact won't fit. The tool auto-bumps to ``H``
whenever a center logo, a gradient, or a risky module shape is in use, so the
code can recover what's covered or softened.

Center Logo
^^^^^^^^^^^

The **LOGO** tab puts a small icon at the center of the code. Pick one of the
social presets (Instagram, Facebook, X, LinkedIn, YouTube, Email, Phone,
Website, Location) or use **Upload custom image** to load your own (PNG, JPEG,
GIF, WebP, or SVG - SVG keeps everything vector and stays sharp at any size).
The uploaded image shows up as a **Custom** tile in the picker, and re-uploading
replaces it.

* **Size** - the icon and its plate, as a percentage of the QR.
* **Background** - the shape of the plate behind the icon, **Square** or
  **Circle**. The plate clears the QR modules in its footprint exactly, with no
  partial-module artifacts.
* **Color** - the logo color. By default it tracks the QR's foreground; if you
  change the QR color, the logo follows. Once you pick a color explicitly it
  becomes independent, and a **Match QR** button appears next to the gradient
  toggle so you can re-inherit at any time. Custom raster images ignore this
  setting - the image has its own pixels.
* **Gradient** - same controls as the QR's gradient. Applies to preset SVG icons
  by substituting their stroke and fill references; custom raster images aren't
  affected.

Selecting any logo automatically bumps error correction to ``H`` so the code can
recover the modules the logo covers.

Shape
^^^^^

The **SHAPE** tab changes how the data modules look. The default is **Square**.
Other choices include **Dots** (small circles), **Rounded** (corner radii fill
in where neighbors are absent), **Horizontal rounded** (pill-shaped), and
several decorative variants: **Pointed**, **Notched**, **Hooks**, and
**Triangles**.

The three corner finder patterns stay as plain squares regardless of the shape
- scanners use them to locate the code, so leaving them predictable keeps things
scannable. The more decorative shapes (dots, hooks, triangles, notched)
auto-bump error correction to ``H`` for the same reason.

Frame
^^^^^

The **FRAME** tab puts a border around the code and an optional text label:

* Style: **None**, **Square**, **Rounded**, or **Circle**.
* **Color** - the frame's stroke color, independent of the QR's foreground.
* **Gradient** - a gradient fill for the frame's stroke, with the same Linear /
  Radial / Direction controls as the QR. For a **Circle** frame, Radial does
  what you'd expect: the gradient transitions exactly across the stroke's inside
  edge to its outside edge, since the geometry is naturally radial. For Square
  and Rounded frames a true inside-to-outside gradient isn't representable on a
  rectangular stroke; Radial falls back to a centered halo where the corners
  pick up more of the end color than the side midpoints do. Linear works as
  expected on every frame shape.
* **Padding** - the gap between the QR matrix and the inner edge of the frame.
  ``0`` makes the frame touch the QR's outermost dark modules; higher values add
  space between them. If you turn on a gradient while padding is ``0``, the tool
  bumps it to ``1`` - a frame touching gradient-filled modules with no quiet
  zone tends to defeat scanners.
* **Thickness** - the stroke width. ``0`` is allowed, useful for text-only
  setups where you want the label but not a visible border.

Below those, a divider separates the frame's appearance from its text:

* **Text** - up to 40 characters, e.g. ``SCAN ME``.
* **Font** - **Sans**, **Serif**, or **Mono**.
* **Placement** - **Outside** the frame (the canvas grows beyond it) or
  **Inside** (the frame grows to enclose the text alongside the QR). Circle
  frames only support outside.
* **Position** - **Top** or **Bottom**.
* **Size** - how big the text is.
* **Text color** - independent of the frame color. Like the logo color, it
  defaults to tracking the frame color until you pick something explicitly; a
  **Match frame** button reverts to inheriting.
* **Gradient** - end color, Linear / Radial, and Direction, applied to the text
  fill. At small text sizes the effect is subtle because the gradient spans only
  the text's bounding box - pick high-contrast endpoints or a horizontal
  direction if you want a strongly visible gradient.

Resetting the Design
--------------------

**Reset design**, to the right of Download and Copy, clears every visual setting
- background, color, all four gradients (QR, frame, logo, text), logo, shape,
frame, frame text, error correction - back to defaults. The contact or URL
itself isn't touched.

Saving Your Work
----------------

Everything you enter is saved in your browser automatically, so what you had
open is still there when you come back. **Clear all fields** wipes the vCard
form and its saved copy; **Clear URL** does the same in URL mode. **Reset
design** clears just the design choices.

**Note:** the saved copy is tied to the specific browser and file location.
Moving or renaming the file starts fresh, and some browsers are strict about
storage on ``file://`` URLs - serving the file over ``http`` avoids that.

Exporting
---------

* **Download SVG** - the QR code as a vector file, for print or design tools.
  Stays crisp at any size. The one exception is a custom raster image used as a
  logo; if you want full vector all the way through, upload an SVG.
* **Download .vcf** - the raw contact card, to import or share directly. (vCard
  mode only.)
* **Copy URL** / **Copy vCard** - copies the encoded payload to your clipboard.

Before You Print
----------------

**Always scan and import the finished code on a real phone before sending
anything to print.** A code that looks fine but imports the wrong details is
worse than none at all. Gradients, dense shapes, and tight padding all push on a
scanner's ability to find and decode the code - the tool nudges settings toward
safer choices (ECC, padding) when you turn those on, but nothing beats verifying
on the actual device the recipient will use.

One harmless quirk to expect: on Windows the country flags in vCard mode appear
as two-letter codes instead of emoji - the dial code is always shown beside
them, so nothing is actually missing.

|cta|
|disqus|
