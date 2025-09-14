# Django Permissions & Groups Setup

## Custom Permissions
Added in `Book` model:
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

## Groups
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → all permissions

## Usage
- Permissions are enforced in `views.py` using `@permission_required`.
- Assign users to groups via Django Admin under "Groups".
- Example:
  - A Viewer cannot access `/add/` or `/edit/`.
  - An Editor can add & edit but not delete.
  - An Admin can do everything.
