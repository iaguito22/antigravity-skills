# Antigravity Skills

Colección de *skills* ultra-optimizadas y probadas bajo estrés para guiar el comportamiento de los agentes IA en el entorno [Antigravity](https://github.com/google/antigravity).

Estas skills han sido comprimidas (< 1.5 KB), refinadas y puestas a prueba para forzar al modelo a ser eficiente, metódico y seguro, mitigando los sesgos comunes de los LLMs (como el "hacer por hacer", adivinar bugs a ciegas, o escupir código basura).

## 🛠 Skills Disponibles

| Skill | Tamaño | Cuándo se activa | Objetivo Principal |
|-------|--------|------------------|--------------------|
| [`code-review.md`](code-review.md) | ~1.3 KB | Pre-commits, revisión de código | Encontrar roturas, fallos silenciosos y código residual, con formato estricto 🔴🟡🔵. |
| [`operational-efficiency.md`](operational-efficiency.md) | ~1.0 KB | Edición masiva, refactors | Usa comandos de shell (`sed`, `grep`) antes que `replace_file_content` para ahorrar tokens y tiempo. |
| [`output-quality.md`](output-quality.md) | ~1.4 KB | Cualquier output verbal | Eliminar relleno, justificaciones y generar resúmenes atómicos de lo comprobado. |
| [`unit-testing.md`](unit-testing.md) | ~1.3 KB | Escritura de pruebas | Evitar el *happy path*. Centrar pruebas en casos límite, input inválido y caídas (error cases). |
| [`git-hygiene.md`](git-hygiene.md) | ~1.4 KB | Comandos git, commits | Prohibir el `git add .` global. Forzar commits atómicos, semánticos y limpios. |
| [`root-cause-analysis.md`](root-cause-analysis.md) | ~1.2 KB | Resolución de bugs oscuros | Prohibir arreglos ciegos. Obligar a instrumentar (poner prints) para aislar el fallo. |
| [`security-audit.md`](security-audit.md) | ~1.4 KB | Manejo de datos y sesiones | Buscar intencionalmente SQLi, XSS, credenciales expuestas e IDORs en el código. |
| [`architecture-planning.md`](architecture-planning.md) | ~1.3 KB | Creación de sistemas nuevos | Bloquear la escritura de código, forzando a entregar un diagrama de arquitectura (Mermaid) primero. |

## 🚀 Instalación

Copia los archivos `.md` de este repositorio en el directorio de skills de tu configuración de Antigravity:

```bash
mkdir -p ~/.gemini/config/skills/nombre-de-la-skill
cp nombre-de-la-skill.md ~/.gemini/config/skills/nombre-de-la-skill/SKILL.md
```
