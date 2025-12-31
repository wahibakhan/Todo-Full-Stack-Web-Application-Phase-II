# API Contract: Authentication Endpoints

**Feature**: Full-Stack Web Todo Application with Authentication
**Date**: 2025-12-29
**Phase**: Phase 1 - Design & Contracts
**Base URL**: `/api/auth`

## Overview

Authentication endpoints manage user registration, login, and logout flows using Better Auth with JWT tokens. All tokens are issued and stored in httpOnly cookies for XSS protection.

## Endpoints

### 1. POST /api/auth/signup

**Purpose**: Create a new user account

**Authentication**: Not required (public endpoint)

**Request**:

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | Yes | Valid email format, max 255 chars | User's email address |
| `password` | string | Yes | Min 8 characters | User's password (will be hashed) |

**Responses**:

**Success (201 Created)**:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "message": "Account created successfully"
}
```

**Error (400 Bad Request)** - Invalid input:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Error (409 Conflict)** - Email already exists:

```json
{
  "detail": "Email already registered"
}
```

**Example**:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "MyPassword123"}'
```

---

### 2. POST /api/auth/login

**Purpose**: Authenticate user and issue JWT token

**Authentication**: Not required (public endpoint)

**Request**:

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | Yes | Valid email format | Registered email address |
| `password` | string | Yes | Min 1 character | User's password |

**Responses**:

**Success (200 OK)**:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "message": "Logged in successfully"
}
```

**Cookies Set**:
```
Set-Cookie: auth-token=<JWT>; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=86400
```

**JWT Payload** (for reference - not sent in response body):
```json
{
  "sub": "123",  // user_id
  "email": "user@example.com",
  "exp": 1735574400  // Expiration timestamp (24 hours)
}
```

**Error (401 Unauthorized)** - Invalid credentials:

```json
{
  "detail": "Invalid credentials"
}
```

**Notes**:
- Generic error message prevents user enumeration
- Don't reveal whether email exists or password is wrong

**Example**:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "MyPassword123"}' \
  --cookie-jar cookies.txt
```

---

### 3. POST /api/auth/logout

**Purpose**: Clear user's authentication token

**Authentication**: Required (JWT in cookie)

**Request**: Empty body

**Responses**:

**Success (200 OK)**:

```json
{
  "message": "Logged out successfully"
}
```

**Cookies Cleared**:
```
Set-Cookie: auth-token=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0
```

**Error (401 Unauthorized)** - No valid token:

```json
{
  "detail": "Not authenticated"
}
```

**Example**:

```bash
curl -X POST http://localhost:8000/api/auth/logout \
  --cookie cookies.txt
```

---

## Authentication Flow Diagram

```
┌─────────┐                                 ┌─────────┐
│ Client  │                                 │ Server  │
└────┬────┘                                 └────┬────┘
     │                                           │
     │  POST /api/auth/signup                    │
     │  {email, password}                        │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                           │ Hash password
     │                                           │ Create user
     │                                           │
     │  201 Created                              │
     │  {user_id, email, message}                │
     │<──────────────────────────────────────────┤
     │                                           │
     │                                           │
     │  POST /api/auth/login                     │
     │  {email, password}                        │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                           │ Verify password
     │                                           │ Generate JWT
     │                                           │
     │  200 OK                                   │
     │  {user_id, email, message}                │
     │  Set-Cookie: auth-token=<JWT>             │
     │<──────────────────────────────────────────┤
     │                                           │
     │  [Subsequent requests include cookie]     │
     │                                           │
     │  POST /api/auth/logout                    │
     │  Cookie: auth-token=<JWT>                 │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                           │ Verify JWT
     │                                           │
     │  200 OK                                   │
     │  {message}                                │
     │  Set-Cookie: auth-token=; Max-Age=0       │
     │<──────────────────────────────────────────┤
     │                                           │
```

## Security Considerations

### Password Handling

1. **Never store plaintext passwords**:
   - Hash with bcrypt (via passlib)
   - Salt is generated automatically
   - Cost factor: 12 rounds (balance between security and performance)

2. **Password validation**:
   - Minimum 8 characters
   - No maximum (bcrypt handles long passwords)
   - Consider adding complexity requirements (optional for Phase 2)

### JWT Token Security

1. **httpOnly cookie**:
   - Prevents JavaScript access (XSS protection)
   - Cannot be read via document.cookie
   - Only sent automatically by browser

2. **Secure flag**:
   - Enabled in production (HTTPS only)
   - Disabled in development (localhost HTTP)

3. **SameSite attribute**:
   - Set to "Lax" (prevents CSRF, allows navigation)
   - Alternative: "Strict" (stricter but may break some flows)

4. **Token expiry**:
   - 24 hours (configurable)
   - Frontend redirects to login on 401 errors

### Error Messages

1. **Generic messages for authentication failures**:
   - "Invalid credentials" (don't reveal if email exists)
   - Prevents user enumeration attacks

2. **Specific messages for validation errors**:
   - Email format invalid
   - Password too short
   - Helps legitimate users

## Testing Checklist

- [ ] Signup with valid email/password creates account (201)
- [ ] Signup with invalid email returns 400
- [ ] Signup with short password (<8 chars) returns 400
- [ ] Signup with duplicate email returns 409
- [ ] Login with correct credentials returns 200 and sets cookie
- [ ] Login with wrong password returns 401
- [ ] Login with non-existent email returns 401
- [ ] Logout with valid token clears cookie (200)
- [ ] Logout without token returns 401
- [ ] JWT token in cookie is httpOnly and Secure (production)
- [ ] JWT token contains correct user_id (sub claim)
- [ ] JWT token expires after configured duration

---

**Authentication Contracts**: ✅ **COMPLETE**
**Next Contract**: Task Endpoints (contracts/task-endpoints.md)
