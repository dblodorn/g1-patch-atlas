# G1 Patch Atlas

A catalogue of where to find Nord Modular G1 and Micro Modular patches, plus editors, `.pch` format docs and reading.

A single static page (`index.html`) with no build step. Resources live in the `R` array in the inline script. Each entry has a `cat` (one of `CATS`), a `status` (`live`, `beta`, `archive`, `dead` or `unchecked`), and optional `count`, `compat` and `note` fields.

Styling follows the sigil-x-native sketch sheets. Space Mono comes from Google Fonts. All text uses the same mono face.

Deployed on Vercel. Pushes to `main` deploy to production.
