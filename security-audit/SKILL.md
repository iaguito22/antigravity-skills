---
name: security-audit
description: >-
  Aggressive search for vulnerabilities and bad practices. Activate to audit
  security, review endpoints, or when the code handles sensitive data, auth,
  payments, or external user inputs.
---

# Security Audit: Threat Modeling

Assume all input is malicious. Review the code searching for these vectors:

1. **Injection**
   - SQL: Is string interpolation (`f"{var}"` or literal `%s`) used in queries?
   - Command: Does user input end up in `os.system` or `subprocess` unsanitized?
   - Path Traversal: Can the user send `../../../etc/passwd` as a filename?

2. **Data Exposure**
   - Are entire objects (`SELECT *`, `user.__dict__`) returned, exposing passwords or tokens in APIs?
   - Are secrets, API keys, or passwords hardcoded in the code?
   - Are sensitive data logged (print/logger) in plain text?

3. **Cryptography & Session**
   - Using `MD5` or `SHA1` for passwords instead of bcrypt/argon2?
   - Are session tokens sequential or predictable (`random` vs `secrets`)?

4. **Business Logic**
   - IDOR: If I request `/api/user/5/delete`, is it checked that I AM user 5 or an admin?
   - Race Conditions: When spending balance, what happens if two exact requests hit the server in the same millisecond?

If you find anything, report it as 🔴 CRITICAL, indicating how to exploit it and how to mitigate it.
