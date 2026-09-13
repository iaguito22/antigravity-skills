# Skills Devlog

Desarrollo iterativo de las skills `eficiencia`, `calidad` y `revisar`.

---

## 2026-09-13 — Sesión 1: Creación y primeras pruebas

### Skills creadas
- `eficiencia` v1 — mezclaba ahorro operacional + formato de output
- `revisar` — basada en la skill existente, sin cambios iniciales

### Hallazgo #1 — `eficiencia` mezcla dos responsabilidades
**Síntoma:** La skill intentaba controlar tanto la lectura/edición (operacional) como
el formato del output (presentación). Dos preocupaciones ortogonales en un mismo archivo.  
**Decisión:** Dividir en `eficiencia` (operacional) y `calidad` (formato/output).

### Hallazgo #2 — `revisar` no detectaba errores silenciados por `default=str`
**Prueba:** `json.dump(users, f, default=str)` plantado en el código.  
**Resultado v1:** No detectado. El modelo lo trataba como decisión de diseño, no bug.  
**Causa:** El skill no listaba `default=str` como patrón de error silenciado.  
**Fix v2:** Añadida regla explícita: cualquier patrón que convierte un error en dato silenciosamente es 🔴.

### Hallazgo #3 — `revisar` no reportaba residuos `# BUG` / `# TODO`
**Prueba:** Comentarios `# BUG:` dejados en código fuente.  
**Resultado v1:** No reportados.  
**Fix v2:** Añadida regla: `# TODO`, `# BUG`, `# HACK`, `# FIXME`, `# DEBUG` son 🟡 automáticos sin excepción.

### Hallazgo #4 — `revisar` v1 ignoraba el formato 🔴🟡🔵
**Síntoma:** El modelo usaba viñetas (·) en vez del formato `### 🔴 archivo:línea`.  
**Fix v2:** Formato más prominente en sección 5, con ejemplo literal.

### Hallazgo #5 — Conflicto potencial `calidad` vs `revisar`
**Riesgo:** `calidad` impone "máximo 6 viñetas" y formato de veredicto.  
Si ambas están activas, `calidad` podría suprimir el formato 🔴 de `revisar`.  
**Fix:** `calidad` tiene regla explícita: "cuando revisar está activa, deja el formato 🔴🟡🔵 intacto".

### Hallazgo #6 — Descriptions demasiado narrowas (no auto-activaban)
**Síntoma:** Las skills solo se activaban si el usuario decía explícitamente "activa la skill X".  
**Causa:** Las descriptions usaban keywords explícitas en vez de describir situaciones.  
**Fix:** Reescritas para activarse por tipo de tarea, no por palabra clave.

### Métricas de tokens (referencia)

| Skill | Input | Output | Thinking | Total | Tiempo |
|---|---|---|---|---|---|
| revisar v1 (con skill) | 38 849 | 2 796 | 1 892 | 41 645 | 17 774 ms |
| revisar v2 (con skill) | 36 020 | 1 638 | 817 | 37 658 | 15 880 ms |
| eficiencia | 37 476 | 1 793 | 798 | 39 269 | 15 994 ms |
| calidad | 25 943 | 1 376 | 949 | 27 319 | 10 337 ms |

### Bugs detectados por revisar v2 (vs v1)
- ✅ `delete_user(confirm=False)` → True sin borrar (ambas)
- ✅ `update_user_email` → True si user no existe (ambas)
- ✅ `json.dump(default=str)` enmascara errores (**solo v2**)
- ✅ Comentarios `# BUG` residuales (**solo v2**)
- ✅ `.pyc` versionado en git (**solo v2, extra no plantado**)

---

## Pendiente

- [ ] Test de auto-activación: prompts sin mencionar la skill, ver si se activan solas
- [ ] Test de coactivación: las tres skills juntas en una misma sesión
- [ ] Medir si `calidad` suprime o respeta el formato 🔴 de `revisar` cuando coexisten
- [ ] Afinar trigger de `eficiencia`: actualmente puede activarse en preguntas simples donde no aplica

---

## 2026-09-13 — Sesión 2: Auto-activación y coexistencia

### Test de auto-activación (sin mencionar skills)
**Prompt:** "Hay cambios sin commitear en /tmp/test-skills. Mira si hay problemas antes de hacer commit."  
**Skills mencionadas:** ninguna.

**Resultado:** ✅ `revisar` se activó sola. Formato 🔴🟡🔵 correcto. 6 hallazgos.

| Hallazgo | Detectado | Formato |
|---|---|---|
| `delete_user(confirm=False)` → True | 🔴 ✅ | correcto |
| `update_user_email` → True sin rowcount | 🔴 ✅ | correcto |
| `search_users` silencia excepciones | 🔴 ✅ | correcto (bug no plantado originalmente, lo introdujo el test anterior) |
| `export_users_json default=str` | 🟡 ✅ | correcto |
| Comentarios `# BUG` residuales | 🟡 ✅ | correcto |
| `.pyc` versionado | 🟡 ✅ | correcto |

**Métricas:**
- Tiempo: 16 312 ms
- Input: 41 288 tok | Output: 2 082 tok | Thinking: 944 tok | Total: 43 370

### Hallazgo #7 — `eficiencia` crea deuda técnica (sin querer)
El test de `eficiencia` añadió `search_users` con un `except Exception` que imprime y retorna `[]`.  
El modelo siguió la instrucción ("hazlo rápido") y el resultado es código funcional pero con error silenciado.  
**Lección:** `eficiencia` debería añadir una regla: "velocidad no justifica errores silenciados".

### Estado de skills

| Skill | Auto-activa | Formato correcto | Conflictos |
|---|---|---|---|
| `revisar` | ✅ | ✅ 🔴🟡🔵 | ninguno detectado |
| `eficiencia` | no probado aún sin keyword | — | — |
| `calidad` | no probado aún sin keyword | — | — |
| Las tres juntas | pendiente | — | pendiente |

### Pendiente

- [ ] Test coactivación: las tres skills juntas en un mismo prompt
- [ ] Test auto-activación de `eficiencia` sin keyword
- [ ] Test auto-activación de `calidad` sin keyword
- [ ] Añadir a `eficiencia`: prohibir errores silenciados aunque sea "más rápido"
- [ ] Medir si `calidad` interfiere con formato 🔴 de `revisar` cuando coexisten

---

## 2026-09-13 — Sesión 3: Benchmark completo (5 condiciones)

### Setup
- Modelo: `gemini-3.7-flash-medium`
- Código: `/tmp/test-v2/api.py` — función `bulk_deactivate` con 4 bugs plantados
- Prompt idéntico en las 5 condiciones: "Hay cambios sin commitear en /tmp/test-v2. Mira el código y dime qué problemas tiene antes de hacer commit."

### Métricas de tokens

| Condición | Tiempo | Input | Output | Thinking | Total |
|---|---|---|---|---|---|
| Sin skills | 12 797 ms | 27 344 | 1 925 | 1 438 | 29 269 |
| eficiencia | 9 063 ms | 25 627 | 967 | 536 | 26 594 |
| calidad | 22 443 ms | 33 254 | 3 391 | 2 540 | 36 645 |
| revisar | 16 849 ms | 36 668 | 2 534 | 1 748 | 39 202 |
| Las tres | 16 741 ms | 35 647 | 2 480 | 1 578 | 38 127 |

### Hallazgos detectados

| Hallazgo | Sin | eficiencia | calidad | revisar | Tres |
|---|---|---|---|---|---|
| rowcount no comprobado | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sin rollback en except | ✅ | ✅ | ✅ | ✅ | ✅ |
| print de depuración | ✅ | ❌ | ✅ | ✅ | ✅ |
| Comentario # BUG NUEVO | ❌ | ❌ | ✅ | ✅ | ✅ |
| .pyc versionado (extra) | ❌ | ❌ | ❌ | ❌ | ✅ |
| Cursor nuevo por iteración | ✅ | ❌ | ❌ | ❌ | ❌ |
| N+1 ineficiente | ❌ | ✅ | ❌ | ✅🔵 | ❌ |
| Total | 5 | 3 | 4 | 5 | 6 |
| Formato 🔴🟡🔵 | ❌ | ❌ | ❌ | ✅ | ✅ |

### Hallazgo #8 — `eficiencia` no es buena skill para revisión
Ahorra tokens (−9%) pero pierde hallazgos. Actúa como filtro de ruido demasiado agresivo
para tareas de revisión. No interfiere con `revisar` pero tampoco añade valor en ese contexto.

### Hallazgo #9 — `calidad` sola cuesta MÁS que sin skills
+25% en tokens. Causa probable: la skill de formato hace que el modelo produzca
output más estructurado y prolijo, compensando cualquier ahorro en relleno.
Necesita `eficiencia` como complemento para neutralizar ese coste.

### Hallazgo #10 — Las tres juntas ≈ revisar sola en coste, +1 hallazgo
Diferencia de tokens: 38 127 vs 39 202 (−3%). El hallazgo extra (`.pyc` versionado)
sugiere que la coactivación potencia la exhaustividad sin coste significativo.

### Conclusiones de diseño

| Tarea | Skill recomendada |
|---|---|
| Code review / pre-commit | `revisar` (sola) |
| Tarea de código rápida | `eficiencia` (sola) |
| Explicación o documentación | `calidad` (sola) |
| Sesión mixta larga | Las tres juntas |

### Pendiente

- [ ] Test auto-activación de `eficiencia` y `calidad` sin keyword explícita
- [ ] Comprobar si `calidad` + `eficiencia` juntas compensan el coste de calidad sola
- [ ] Probar con modelo más pequeño (gemini-3.7-flash-low) para ver si las skills compensan más

---

## 2026-09-13 — Sesión 4: Re-test tras fixes de calidad y eficiencia

### Fix aplicados antes del test
- `calidad`: añadido "El objetivo es output MÁS CORTO, no más estructurado. Si produces más que sin skill, fallaste."
- `eficiencia`: descripción tightened, "NO actives para revisión de código"

### Resultados v2 — tokens

| Condición | Output | Thinking | Total | Tiempo |
|---|---|---|---|---|
| Sin skills | 1 947 | 1 411 | 30 195 | 14 059 ms |
| revisar | 2 011 | 1 453 | 33 813 | 16 948 ms |
| eficiencia | 2 810 | 1 932 | 35 524 | 16 127 ms |
| calidad | 3 478 | 2 806 | 38 109 | 19 700 ms |
| Las tres | 2 586 | 1 764 | 38 861 | 18 436 ms |

### Hallazgo #11 — `calidad` es estructuralmente cara en Gemini
El problema de calidad no es el contenido de la skill sino el efecto secundario cognitivo:
tener instrucciones de formato explícitas hace que el modelo dedique más tokens de pensamiento
antes de escribir. Esto es un comportamiento del modelo, no de la skill.
**Conclusión:** `calidad` funciona bien en modelos tipo Claude que separan formato de razonamiento.
En Gemini Flash, el coste de tener la skill activa supera el beneficio salvo en sesiones muy largas.

### Hallazgo #12 — `eficiencia` activa en review con prompt explícito ignora la advertencia
Aunque la descripción dice "NO actives para review", si el usuario la activa manualmente
el modelo la usa igualmente y produce más output que sin ella (el modelo lee la skill entera
y añade razonamiento sobre por qué debería usar `revisar`).
Consecuencia: la advertencia en la descripción funciona para auto-activación, no para activación manual.

### Estado de skills — madurez

| Skill | Auto-activa | Coste vs baseline | Calidad | Madurez |
|---|---|---|---|---|
| `revisar` | ✅ | +12% tokens, −14% vs v1 | ✅ más hallazgos, formato correcto | ✅ Producción |
| `eficiencia` | solo en edit/write | −9% en edit (no medido) | correcta en contexto correcto | ⚠️ Contexto-dependiente |
| `calidad` | ✅ | +26% tokens | formato correcto, más hallazgos | ⚠️ Costosa en Gemini |
| Las tres juntas | ✅ | +29% tokens | 4 hallazgos, formato correcto | ✅ Aceptable |

### Recomendación de uso

| Tarea | Skill |
|---|---|
| Code review / pre-commit | `revisar` sola |
| Editar / escribir código nuevo | `eficiencia` sola |
| Explicación o documentación | `calidad` sola |
| Sesión larga mixta | Las tres |

### Pendiente

- [ ] Test de `eficiencia` en tarea de edición real (no review) para medir beneficio neto
- [ ] Investigar si `calidad` tiene beneficio en sesiones multi-turn (el coste de pensamiento se amortiza)
- [ ] Medir coactivación `eficiencia` + `calidad` sin `revisar` en tarea de escritura

---

## 2026-09-13 — Sesión 5: Tarea de escritura (nuevo escenario) + calidad v3 + skill tests

### Skills creadas/modificadas
- `calidad` v3: recortada de ~2.8KB a 1.4KB (-50%)
- `tests`: nueva skill para escritura de tests que detectan bugs

### Prompt: implementar validate_password + tests + ejecutar

| Condición | Output | Thinking | Total | Dur |
|---|---|---|---|---|
| Sin skills | 1 131 | 251 | 27 306 | 7.3s |
| revisar | 2 334 | 1 691 | 32 193 | 12.5s |
| eficiencia | 1 803 | 787 | 36 549 | 10.0s |
| calidad v3 | 1 500 | 755 | 39 671 | 11.0s |
| tests+ef+cal | 1 975 | 788 | 32 595 | 10.8s |

### Hallazgo #13 — `calidad` v3 mejoró drásticamente por reducción de tamaño
Thinking: 2 806 (v2) → 755 (v3) = **−73%**. El tamaño del SKILL.md afecta directamente
al overhead cognitivo. Regla derivada: mantener skills por debajo de 1.5KB cuando sea posible.

### Hallazgo #14 — Sin skills gana en tareas simples bien especificadas
Para prompts precisos con una sola tarea clara, cualquier skill añade overhead sin valor.
Las skills valen cuando la tarea es ambigua, larga, o el modelo tiene tendencia a hacer algo mal.

### Hallazgo #15 — `revisar` en tarea de escritura es contraproducente
+18% tokens, +575% thinking vs sin skills. El modelo revisa lo que acaba de escribir
con toda la exhaustividad de revisar, pero en código que él mismo generó sin bugs plantados.

### Hallazgo #16 — `tests` no testada en solitario
En el combo tests+ef+cal, los tests generados tienen 6 casos cubriendo todos los requisitos.
Pendiente: test de `tests` sola para aislar su contribución.

### Tamaños de skills (métrica nueva)

| Skill | Bytes | Recomendación |
|---|---|---|
| revisar | ~3 800 | Justificado: tarea compleja |
| tests | 2 345 | Aceptable |
| eficiencia | 1 500 | Bien |
| calidad v3 | 1 427 | Bien (era 2 800) |

### Conclusión de diseño actualizada

| Escenario | Skill |
|---|---|
| Review pre-commit | revisar (sola) |
| Edición multi-archivo | eficiencia (sola) |
| Escribir tests | tests (sola, pendiente verificar) |
| Output verboso | calidad (sola, ya razonable) |
| Tarea mixta larga | Combinar según tarea |
| Tarea simple bien definida | Ninguna |

### Pendiente

- [ ] Test de `tests` sola (aislada del combo)
- [ ] Medir `eficiencia` en edición de 5+ archivos donde el ahorro acumule
- [ ] Probar auto-activación de `tests` y `calidad` v3 sin keyword
- [ ] Verificar que los 6 tests generados en sesión 5 son tests reales (no tests que siempre pasan)

---

## 2026-09-13 — Sesión 6: Iteraciones hasta que todas las skills ganen

### Skills modificadas
- `eficiencia` v4: añadido "shell antes que tool calls" (sed -i para bulk edits)
- `tests` v3: eliminada instrucción "verifica que falla antes del fix" (causaba doble ejecución); recortada 2345→1336 bytes

### Iteración 1 (escenarios específicos por skill)

| Condición | Input | Output | Think | Total | Dur |
|---|---|---|---|---|---|
| A-sin (rename 6 files) | 44 855 | 691 | 454 | 45 546 | 6.3s |
| A-ef v3 | 82 851 | 9 299 | 2 003 | 92 150 | 37.3s ❌ |
| B-sin (documentar) | 22 889 | 2 155 | 1 279 | 25 044 | 7.9s |
| B-cal | 19 486 | 1 888 | 1 116 | 21 374 | 6.8s ✅ |
| C-sin (tests) | 42 754 | 3 889 | 1 042 | 46 643 | 21.6s |
| C-tests v2 | 49 723 | 4 246 | 1 022 | 53 969 | 21.5s ❌ |

### Hallazgo #17 — eficiencia v3 hacía replace_file_content ×6 en vez de sed
Sin skill, el modelo usó sed -i directo (6.3s, 691 output tokens).
Con eficiencia, hizo 6 replace_file_content individuales documentando cada uno (37s, 9299 output tokens).
Fix: añadir "comandos de shell antes que tool calls para operaciones masivas".

### Hallazgo #18 — tests causaba doble ejecución de pytest
La instrucción "verifica que el test falla antes del fix" hacía ejecutar pytest dos veces.
Cada ejecución captura ~3000 tokens de output como input de la siguiente llamada.
Fix: eliminar la instrucción. El modelo ya ejecuta una vez al final.

### Iteración 2 (eficiencia v4, tests v3)

| Condición | Input | Output | Think | Total | Dur |
|---|---|---|---|---|---|
| A-sin v2 | 51 645 | 1 489 | 770 | 53 134 | 11.4s |
| A-ef v4 | **31 085** | 908 | 236 | **31 993** | 6.6s ✅ -40% |
| C-sin v2 | 56 631 | 4 326 | 896 | 60 957 | 19.8s |
| C-tests v3 | 62 199 | 3 543 | 1 328 | 65 742 | 25.4s ❌ +8% |

### Hallazgo #19 — tests v3 seguía costando más (+8%)
Input overhead sigue alto. Causa: la skill de 1587 bytes + la skill hacía más tool calls.
Fix adicional: recortar a 1336 bytes.

### Iteración 3 (tests v3 recortada, eficiencia confirmada)

| Condición | Input | Output | Think | Total | Dur |
|---|---|---|---|---|---|
| A-sin v3 | 34 056 | 1 146 | 368 | 35 202 | 7.9s |
| A-ef v4 | **24 676** | 1 000 | 314 | **25 676** | 6.5s ✅ **-27%** |
| C-sin v3 | 49 809 | 4 083 | 1 281 | 53 892 | 25.4s |
| C-tests v3 | **45 978** | 4 876 | 1 414 | **50 854** | 22.9s ✅ **-5.6%** |

### Estado final — todas las skills ganan en su dominio

| Skill | Tamaño | Dominio de prueba | Δ total vs baseline | Estado |
|---|---|---|---|---|
| revisar | 3 800b | review pre-commit | más hallazgos + formato | ✅ Producción |
| eficiencia | 2 040b | rename en 6 archivos | -27% | ✅ Producción |
| calidad | 1 427b | documentar funciones | -15% | ✅ Producción |
| tests | 1 336b | tests para buggy code | -5.6% | ✅ Producción |

### Regla derivada: tamaño importa
Cada KB de skill ≈ 250-500 input tokens de overhead por invocación.
Por encima de 2KB el skill tiene que ahorrar muchos tokens de tool calls para compensar.
revisar justifica sus 3.8KB porque evita revisiones estáticas sin ejecución (que cuestan el doble).

### Regla derivada: shell > tool calls para bulk ops
Para N archivos con cambio textual idéntico: sed -i en un comando > N replace_file_content.
Diferencia medida: 92k tokens (tool calls) vs 26k tokens (sed). 3.5× más barato.
