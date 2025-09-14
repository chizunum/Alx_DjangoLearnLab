# Security Checklist & Notes

## Settings changes
- DEBUG = False in production
- SESSION_COOKIE_SECURE = True
- CSRF_COOKIE_SECURE = True
- SECURE_BROWSER_XSS_FILTER = True
- SECURE_CONTENT_TYPE_NOSNIFF = True
- X_FRAME_OPTIONS = "DENY"
- Consider django-csp for Content Security Policy

## Templates
- All POST forms include `{% csrf_token %}`
- Avoid `|safe` unless content is sanitized

## Views & Forms
- Always use Django ORM and ModelForm for input validation.
- Use `@login_required` and `@permission_required` to protect sensitive views.
- Use `POST` for create/edit/delete actions.

## Testing steps
1. Create test users and assign to groups (Viewers, Editors, Admins).
2. Login as each user and attempt:
   - Viewer: book list only.
   - Editor: add/edit but cannot delete.
   - Admin: can delete.
3. Try form submissions without CSRF token — should be blocked.
4. Try recipe for XSS: submit a string like `<script>alert(1)</script>` into a text field and verify it is escaped in the output.

## Notes
- In development (localhost) you may set cookie-secure flags to False until you enable HTTPS.
- When enabling HSTS and CSP in production, carefully test third-party scripts and CDN rules to avoid breaking the site.
