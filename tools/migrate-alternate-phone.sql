-- Run once if form_submissions was created from the previous schema.
ALTER TABLE form_submissions
    ADD COLUMN alternate_phone VARCHAR(20) NOT NULL DEFAULT '' AFTER phone;
