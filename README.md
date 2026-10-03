# 🦀 Rust sin Dolor: La Guía Visual y Directa al Grano

[![Rust](https://img.shields.io/badge/Rust-2024_Edition-orange?logo=rust)](https://www.rust-lang.org/)
[![Typst](https://img.shields.io/badge/Compiled_with-Typst-239dad?logo=typst)](https://typst.app/)
[![Target](https://img.shields.io/badge/Focus-ADHD_%2F_TDAH_Friendly-blue)]()
[![Background](https://img.shields.io/badge/From-JavaScript_%2F_TypeScript-yellow?logo=typescript)](https://www.typescriptlang.org/)

Un generador automatizado y libro técnico completo para dominar **Rust** desde cero, diseñado específicamente para **mentes con TDAH**, desarrolladores que vienen del ecosistema **JavaScript / TypeScript**, y aprendices visuales.

Pasa de la comodidad del *Garbage Collector* al modelo de **Ownership, Concurrencia segura y Alto Rendimiento** sin la densidad académica de 700 páginas de texto plano.

---

## 🎯 ¿Por qué este libro?

* 🧠 **Diseñado para TDAH:** Párrafos de máximo 3 líneas, cero muros de texto, cajas de síntesis (*"En 10 segundos"*) y análisis quirúrgico de errores (*"Frenazo del compilador"*).
* 🟦 **El puente desde JS/TS:** Cada concepto clave se compara directamente con cómo funciona en Node.js, V8 o TypeScript (ej. `const` vs `let`, `Promise` vs `Future`, `null` vs `Option<T>`, `postMessage` vs `mpsc`).
* 🎨 **100% Vectorial y Visual:** Incluye diagramas SVG de alto contraste generados e incrustados directamente en el documento (Stack vs Heap, préstamos, punteros inteligentes, Tokio, etc.).
* ⚡ **Compilación ultrarrápida con Typst:** Genera un PDF editorial maquetado en segundos mediante **Pandoc + Typst**, prescindiendo de instalaciones pesadas de LaTeX.
* 📚 **Cobertura total (27 Capítulos):** Desde el primer `Hello World` hasta `async/.await`, `unsafe`, macros declarativas (`macro_rules!`) y monorrepositorios con `Cargo Workspaces`.

---

## 📑 Índice de Capítulos

| Bloque | Capítulos |
| :--- | :--- |
| **I. Los Cimientos** | 01. ¿Por qué Rust? • 02. Variables y Mutabilidad • 03. Funciones y Expresiones • 04. Control de Flujo |
| **II. El Motor de Memoria** | 05. Ownership (Propiedad) • 06. Borrowing (Préstamos) • 07. Slices de Memoria |
| **III. Estructuras y Tipos** | 08. Structs y Métodos • 09. Enums y `Option<T>` • 10. Pattern Matching (`match`, `if let`, `let...else`) |
| **IV. Colecciones y Errores** | 11. Vectores (`Vec<T>`) • 12. Strings UTF-8 en Profundidad • 13. HashMaps • 14. `Result<T, E>` y el Operador `?` |
| **V. Arquitectura y Abstracciones** | 15. Módulos y Crates • 16. Genéricos y Traits • 17. Lifetimes (`'a`) • 18. Closures e Iteradores |
| **VI. Punteros y Sistemas** | 19. Smart Pointers (`Box`, `Rc`, `RefCell`) • 20. Concurrencia e Hilos • 21. Proyecto: Servidor Web Multihilo |
| **VII. Rust Profesional** | 22. Testing Automatizado • 23. Asincronía con Tokio • 24. Técnicas Avanzadas (`dyn Trait`, `Deref`) • 25. Unsafe Rust • 26. Macros Declarativas • 27. Workspaces de Cargo |

---

## 🛠️ Requisitos Previos

El flujo de trabajo está optimizado para **Linux (Arch / Manjaro / Fedora / Ubuntu)**, **macOS** o **WSL2** en Windows.

### 1. Dependencias del sistema (Manjaro / Arch Linux)
```bash
sudo pacman -S pandoc typst python ttf-liberation

```

*(En Ubuntu/Debian: `sudo apt install pandoc python3 python3-venv fonts-liberation`, e instala [Typst](https://github.com/typst/typst/releases)).*

### 2. Entorno virtual de Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-genai

```

### 3. Clave de API de Gemini

El script utiliza los modelos de Google Gemini para la generación asistida de capítulos. Obtén tu clave en [Google AI Studio](https://aistudio.google.com/):

```bash
export GEMINI_API_KEY="tu_api_key_aqui"
# Opcional (por defecto usa gemini-3.5-flash-lite):
export GEMINI_MODEL="gemini-3.5-flash-lite"

```

---

## 🚀 Uso Rápido

### Compilar el libro existente a PDF (Sin llamar a la API)

Si ya tienes los archivos Markdown en la carpeta `capitulos/` y solo deseas compilar el PDF:

```bash
python generar_libro.py --clean-only

```

Esto saneará cualquier etiqueta XML/SVG, ensamblará `libro_completo.md` y compilará `Rust_Sin_Dolor_Edicion_Visual.pdf` en segundos.

### Generar capítulos pendientes o nuevos

```bash
python generar_libro.py

```

El script detecta automáticamente los capítulos presentes en disco. Si falta alguno, invocará la API para redactarlo, extraer sus diagramas vectoriales en archivos `.svg` independientes y ensamblar el documento final.

### Regenerar toda la obra desde cero

```bash
python generar_libro.py --force

```

---

## 📂 Estructura del Repositorio

```text
├── capitulos/                  # Archivos Markdown y diagramas SVG generados
│   ├── 01_introduccion_y_cargo.md
│   ├── 01_introduccion_y_cargo_img_1.svg
│   └── ...
├── generar_libro.py            # Orquestador: llamadas LLM, extracción SVG y Typst
├── libro_completo.md           # Archivo concatenado listo para compilación
├── Rust_Sin_Dolor_Edicion_Visual.pdf # Binario final maquetado
└── README.md                   # Documentación del proyecto

```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

* Si encuentras un concepto técnico que pueda explicarse con una metáfora aún más simple, abre un *Issue* o *Pull Request*.
* Si diseñas mejores esquemas vectoriales SVG o mejoras la plantilla de Typst, tus sugerencias son bien recibidas.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Puedes usarlo, compartirlo y adaptarlo libremente para tus propios entornos de estudio o docencia.

```
