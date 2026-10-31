# GLA Online Admissions

Prepared for **https://glaonlineadmission.com/** using PHP 8.2+ and MySQL.

## What changed

- Updated website URLs, canonical URLs, social metadata, structured data and sitemap.
- Public pages and the local search index contain no old-domain references.
  LMS-address FAQs were removed rather than redirected to nonexistent local
  portals. The application FAQ describes this website's enquiry-only flow.
  Source URLs remain in non-public download tools and provenance records so
  the mirror can still be refreshed.
- Website contact numbers and click-to-call links use **+91 93113 81814**.
- Removed the original web agency's footer credit and author metadata.
- Removed **Student Login navigation only**, as requested. Other student resources,
  exam/payment links, testimonials and course content remain.
- Replaced the original registration widgets and form handlers with local
  admissions/contact forms. All Apply Now buttons, including mobile buttons,
  open a local enquiry form.
- The compact hero form matches the original field order and styling, including
  alternate mobile, state and dependent district selection. State/district
  options are cached locally; they do not require the original registration API.
- Fixed malformed homepage nesting so alumni events, corporate learners,
  testimonials, masters, presence, social sections, FAQs and the footer remain
  visible outside the intentionally hidden faculty section.
- Brochure requests save an enquiry before offering the locally downloaded PDF.
  The former WhatsApp popup is not used; this implementation does not send WhatsApp
  messages, OTPs or automatic emails.
- Admission and brochure popups use a responsive two-column desktop layout,
  single-column mobile fields, clear focus indicators and a scrollable dialog.
  The compact hero form and backend submission behavior remain separate.
- Enquiries are stored in `form_submissions`, with consent, source page and time.
  No public submissions viewer or student login is provided.
- Added server-side validation, prepared SQL statements, session/CSRF protection,
  retry deduplication and a limit of five new submissions per network address
  in ten minutes. Failed saves are shown explicitly; they never display success.
- Captured the previously dynamic event listings and their linked detail pages,
  gallery images, brochures, CDN scripts and fonts. Blog pages remain excluded.

## Deploy to your hosting

1. Enable **PHP 8.2 or newer**, **PDO MySQL**, MySQL access and HTTPS for
   `glaonlineadmission.com`.
2. Upload the public website files into that domain's `public_html` directory.
   Include the hidden [.htaccess](.htaccess), [api/](api/), [siteassets/](siteassets/),
   [_external/](_external/) and all page/media directories. The files belong at the
   document root, not in an extra nested folder.
3. Select database **`u261758575_gla1`** in phpMyAdmin and import
   [tools/schema.sql](tools/schema.sql).
   If you already imported the previous schema, run
   [tools/migrate-alternate-phone.sql](tools/migrate-alternate-phone.sql) **once**
   instead to add the alternate mobile field without deleting existing enquiries.
4. Put the privately configured `gla-database.ini` file **one directory above
   `public_html`**, never inside the public website. A configured local copy was
   created alongside this workspace, outside the website folder.
   [tools/gla-database.example.ini](tools/gla-database.example.ini) documents its
   structure without exposing a password.
5. Ensure the private file is readable by the PHP hosting account only
   (typically Unix permissions `600`). Its host is `localhost`, and its database
   and user are `u261758575_gla1`. If necessary, the `GLA_DB_CONFIG` server
   environment variable can point to another private configuration file.
6. Submit an enquiry and a contact form on the deployed HTTPS site. Confirm the
   success message and the corresponding records in `form_submissions`.

The password is not embedded in browser files or public PHP source. Rotate the
password shared in chat before production and update the private configuration.
The private production database has **not** been connected to or modified from
this local machine; importing the schema and testing the live connection remain
deployment steps.

The [tools/](tools/) directory, downloader, SQL, configuration examples and
documentation do not need to be uploaded. If included, the provided Apache/
LiteSpeed access rules deny access to those files. Nginx deployments must add
equivalent access restrictions and redirect HTTP/www to the HTTPS canonical host.

## Local preview and refresh

A PHP CLI installation must be available. From this folder:

```powershell
php -S 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/>. To save forms locally, configure a local MySQL
database, import the schema, and point `GLA_DB_CONFIG` at its private INI file.
A plain static server or opening HTML files directly cannot execute the form API.

To refresh the mirror (including hosting changes):

```powershell
pip install -r requirements.txt
python download_site.py --reuse-assets
python tools\audit_mirror.py
```

Omit `--reuse-assets` to redownload existing assets as well. The source site can
change; review the refreshed output and rerun validation before deploying it.

## Verification and known limitations

- The completed mirror has **161 public HTML pages** and approximately **494 MB**
  of public files.
- The resource audit checks HTML, CSS, inline backgrounds, metadata, brochure
  links, local forms, legacy-domain references and blog exclusion.
- The PHP API is covered by **15 integration tests** against an isolated MariaDB 11.4
  instance using the MySQL protocol. Desktop, contact and mobile submissions were
  also exercised in the browser and checked in the database.
- Production hosting, Apache/LiteSpeed rules and the live MySQL connection still
  require the deployment checks above.
- Vimeo/YouTube videos, Google Maps and retained external portals remain
  online services; their streaming media are not standalone offline copies.
- Four references on the source site returned 404: `captions-en.vtt`,
  `siteassets/images/svg-icons/arrow-yellow.svg`,
  `siteassets/images/svg-icons/feature_blog_icon.svg` and the structured-data
  `assets/images/logo.png`. Dead caption/decorative references were removed, and
  structured data now uses the existing site logo.
- The mirror audit also checks that every lower homepage section is a direct
  child of the main content and that all original hero fields are present.
- The original convocation AJAX endpoint returned an empty response, and its
  shared event API returned no entries. The local page explicitly links to the
  captured 14th Convocation Ceremony archive instead of showing a blank listing.
