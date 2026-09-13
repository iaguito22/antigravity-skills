---
name: security-audit
description: >-
  Búsqueda agresiva de vulnerabilidades y malas prácticas. Activar para auditar
  seguridad, revisar endpoints, o cuando el código maneje datos sensibles,
  autenticación, pagos o inputs de usuarios externos.
---

# Security Audit: Modelo de Amenazas

Asume que todo input es malicioso. Revisa el código buscando estos vectores:

1. **Inyección**
   - SQL: ¿Se usa interpolación de strings (`f"{var}"` o `%s` literal) en queries?
   - Command: ¿El input acaba en `os.system` o `subprocess` sin sanitizar?
   - Path Traversal: ¿Puede el usuario enviar `../../../etc/passwd` como nombre de archivo?

2. **Exposición de Datos**
   - ¿Se devuelven objetos enteros (`SELECT *`, `user.__dict__`) exponiendo contraseñas o tokens en APIs?
   - ¿Hay secretos, API keys o contraseñas quemadas (hardcoded) en el código?
   - ¿Se loguean (print/logger) datos sensibles en texto plano?

3. **Criptografía y Sesión**
   - ¿Uso de `MD5` o `SHA1` para contraseñas en vez de bcrypt/argon2?
   - ¿Se generan tokens de sesión secuenciales o predecibles (`random` básico vs `secrets`)?

4. **Lógica de Negocio**
   - IDOR: ¿Si pido `/api/user/5/delete`, se comprueba que YO soy el user 5 o un admin?
   - Race Conditions: Al gastar saldo, ¿qué pasa si se hacen dos peticiones exactas en el mismo milisegundo?

Si encuentras algo, repórtalo como 🔴 CRÍTICO, indicando cómo explotarlo y cómo mitigarlo.
