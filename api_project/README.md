## Authentication & Permissions

This API uses **Token Authentication** via Django REST Framework.

### Getting a Token

To obtain a token, send a POST request to:


with JSON body:

```json
{
  "username": "your_username",
  "password": "your_password"
}

{
  "token": "1a2b3c4d5e..."
}

Authorization: Token <your-token>


---

## **Step 3: Optional — Link Views and README**

- In `README.md`, you can add a table of endpoints and indicate which permission applies to each.  

| Endpoint          | Method | Permission       |
|------------------|--------|----------------|
| /api/books/       | GET    | IsAuthenticated |
| /api/books/       | POST   | IsAuthenticated |
| /api/authors/     | GET    | IsAdminUser     |
| /api/authors/     | POST   | IsAdminUser     |
| /api/token/       | POST   | Public (login)  |

---


