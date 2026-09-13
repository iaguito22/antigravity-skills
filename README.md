# Antigravity Skills

Colección de *skills* ultra-optimizadas y probadas bajo estrés para guiar el comportamiento de los agentes IA en el entorno [Antigravity](https://github.com/google/antigravity).

Estas skills han sido comprimidas (todas entre 1 KB y 1.5 KB), refinadas y puestas a prueba de forma iterativa para forzar al modelo a ser eficiente, metódico y seguro. Puedes leer el historial científico de estas pruebas y nuestros hallazgos (coste de tokens por KB, desobediencias de modelos, etc.) en el [`DEVLOG.md`](DEVLOG.md).

## 🛠 Skills Disponibles

| Skill | Objetivo Principal |
|-------|--------------------|
| [`code-review`](code-review/SKILL.md) | Encontrar roturas, fallos silenciosos y código residual, con formato estricto 🔴🟡🔵. |
| [`operational-efficiency`](operational-efficiency/SKILL.md) | Usa comandos de shell (`sed`, `grep`) antes que llamadas API para refactors masivos ahorrando tokens. |
| [`output-quality`](output-quality/SKILL.md) | Elimina relleno, justificaciones y genera resúmenes atómicos de lo comprobado. |
| [`unit-testing`](unit-testing/SKILL.md) | Centra las pruebas en casos límite, input inválido y *error handling*. |
| [`git-hygiene`](git-hygiene/SKILL.md) | Prohíbe el `git add .` global. Fuerza commits atómicos, semánticos y sin basura. |
| [`root-cause-analysis`](root-cause-analysis/SKILL.md) | Prohíbe arreglos ciegos. Obliga a instrumentar el código para aislar un fallo desconocido. |
| [`security-audit`](security-audit/SKILL.md) | Busca intencionalmente vectores como SQLi, XSS, secretos expuestos e IDORs en el código. |
| [`architecture-planning`](architecture-planning/SKILL.md) | Bloquea el sistema impidiendo escribir código fuente hasta que el diseño sea aceptado. |

## 🚀 Instalación

La estructura de este repositorio refleja exactamente la requerida por Antigravity. Simplemente copia el contenido a tu directorio local de skills:

```bash
# Copia todas las carpetas a tu configuración de Gemini/Antigravity
cp -r * ~/.gemini/config/skills/
```

O si prefieres clonarlo directamente y crear un enlace simbólico (recomendado para mantenerlo actualizado):
```bash
git clone https://github.com/iaguito22/antigravity-skills.git ~/antigravity-skills
ln -s ~/antigravity-skills/* ~/.gemini/config/skills/
```
