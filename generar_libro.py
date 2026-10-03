#!/usr/bin/env python3
"""
generar_libro.py - Generador integral de "Rust sin Dolor: La Guía Visual"
Incluye los 27 capítulos completos (con Unsafe, Macros declarativas y Workspaces),
control estricto de contrastes SVG, reparación de entidades XML (& -> &amp;),
prevención de bloques de código Markdown sin cerrar y soporte para gemini-3.5-flash-lite.
"""

import os
import sys
import time
import re
from pathlib import Path
from google import genai
from google.genai import types

# ==========================================
# 1. CONFIGURACIÓN Y ENTORNO
# ==========================================
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ ERROR: La variable de entorno GEMINI_API_KEY no está configurada.")
    print("Ejecuta: export GEMINI_API_KEY='tu_api_key'")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Modelo configurado por defecto
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

OUTPUT_DIR = Path("capitulos")
OUTPUT_DIR.mkdir(exist_ok=True)
COMPLETED_BOOK_MD = Path("libro_completo.md")
FINAL_PDF = Path("Rust_Sin_Dolor_Edicion_Visual.pdf")

# ==========================================
# 2. PROMPT DEL SISTEMA (TDAH + TS + CONTRASTE)
# ==========================================
SYSTEM_INSTRUCTION = """
Eres un autor técnico de élite y pedagogo especializado en neurodivergencia y aprendizaje visual para TDAH.
Tu misión es escribir capítulos para el libro "Rust sin Dolor: La Guía Visual y Directa al Grano".

REGLAS PEDAGÓGICAS Y DE FORMATO:
1. PUREZA DE IDIOMA Y CARACTERES (CRÍTICO):
   - Escribe en español impecable, usando los términos técnicos estándar de Rust en inglés ('trait', 'struct', 'enum', 'match', 'borrow', 'lifetime', 'unsafe', 'macro', 'workspace').
   - PROHIBICIÓN TOTAL de caracteres en chino, japonés, coreano o glifos parásitos adheridos a palabras.
   - Asegúrate de cerrar SIEMPRE todos los bloques de código abiertos (```).

2. COMPRENSIÓN TOTAL:
   - Explicaciones directas, accesibles para un joven de 12 años sin perder rigor para desarrolladores senior.
   - Párrafos cortos de máximo 2 a 3 líneas para evitar fatiga cognitiva.

3. CAJAS COGNITIVAS OBLIGATORIAS (Usa formato blockquote de Markdown):
   - > 🧠 **EN 10 SEGUNDOS (TDAH):** [Resumen ultra directo de 1-2 frases]
   - > 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** [Comparación clara de cómo se hace esto en TS/JS vs Rust]
   - > 🟥 **FRENAZO DEL COMPILADOR:** [Explicación de un error común de compilación y qué bug evitó]

4. ILUSTRACIONES VECTORIALES (SVG OBLIGATORIO):
   - Incluye 1 o 2 diagramas visuales en SVG puro (<svg>...</svg>) por capítulo.
   - REGLA CRÍTICA DE CONTRASTE:
     * FONDOS: Usa colores pastel claros (#eff6ff azul, #fef2f2 rojo, #ecfdf5 verde, #f8fafc gris suave).
     * TEXTOS (<text>): ESTRICTAMENTE PROHIBIDO usar grises claros, amarillos o blanco sobre fondo claro.
     * Todo texto debe usar negro azulado oscuro (#0f172a o #1e293b) con font-weight="600" o "bold".
     * Títulos destacados dentro de cajas: tonos oscuros saturados (#1e40af azul oscuro, #991b1b rojo oscuro).
     * El carácter '&' dentro de textos SVG debe escribirse como '&amp;' para no romper el XML.

5. CÓDIGO RUST MODERNO:
   - Rust edición 2024 (versión 1.85+). Bloques claros con comentarios concisos.
"""

# ==========================================
# 3. ÍNDICE COMPLETO (27 CAPÍTULOS)
# ==========================================
CAPITULOS = [
    {
        "id": "01_introduccion_y_cargo",
        "titulo": "Capítulo 1: ¿Por qué Rust? De C y JavaScript al Vigilante en la Entrada",
        "tema": "Por qué la gestión de memoria sin Garbage Collector importa. Instalación, Cargo frente a npm (Cargo.toml vs package.json), y anatomía de main.rs."
    },
    {
        "id": "02_variables_y_tipos",
        "titulo": "Capítulo 2: Variables, Mutabilidad y Tipos con Peso Real",
        "tema": "Inmutabilidad por defecto (let vs mut frente a const/let en JS). Shadowing. Enteros con y sin signo (i32, u8), floats, booleans y char vs Strings."
    },
    {
        "id": "03_funciones_y_expresiones",
        "titulo": "Capítulo 3: Funciones, Sentencias y el Misterio del Punto y Coma",
        "tema": "Funciones y tipos de retorno. Sentencias vs Expresiones (retorno implícito sin ';' comparado con funciones flecha en TS)."
    },
    {
        "id": "04_control_de_flujo",
        "titulo": "Capítulo 4: Tomando Decisiones: If Expresión y Bucles",
        "tema": "If como expresión asignable a variables. Bucles: loop con retorno de valor con break, bucles while y for iterando rangos y colecciones."
    },
    {
        "id": "05_ownership_la_propiedad",
        "titulo": "Capítulo 5: El Jefe Final: Ownership (Propiedad) y la Memoria",
        "tema": "Stack vs Heap con analogías. Las 3 reglas de oro del Ownership. Transferencia de propiedad (Move) vs referencias en JS. Por qué s1 se invalida con let s2 = s1."
    },
    {
        "id": "06_borrowing_prestamos",
        "titulo": "Capítulo 6: Borrowing: El Arte de Prestar sin Perder la Propiedad",
        "tema": "Referencias inmutables (&T) y la regla de lectura. Referencias mutables (&mut T). La ley sagrada de Rust: muchos lectores o un solo escritor."
    },
    {
        "id": "07_slices_ventanas_de_datos",
        "titulo": "Capítulo 7: Slices: Ventanas a Trozos de Memoria sin Copiar",
        "tema": "El problema de los índices desconectados. String slices (&str vs String). Slices de arrays y colecciones. Prevención de errores en compilación."
    },
    {
        "id": "08_structs_y_metodos",
        "titulo": "Capítulo 8: Structs: Modelando Datos sin Clases Clásicas",
        "tema": "Definición e instanciación de structs (comparado con interfaces de TS). Métodos en bloques impl: &self, &mut self y constructores asociados (Self::new)."
    },
    {
        "id": "09_enums_y_option",
        "titulo": "Capítulo 9: Enums con Datos y el Fin de los Errores por Null",
        "tema": "Enums enriquecidos. El error del billón de dólares (null/undefined). El tipo Option<T> (Some y None) y desempaquetado seguro."
    },
    {
        "id": "10_match_y_pattern_matching",
        "titulo": "Capítulo 10: Pattern Matching: La Máquina Clasificadora Perfecta",
        "tema": "La instrucción match exhaustiva. Desestructuración de datos en variantes. Atajos: if let y let...else para mantener el happy path plano."
    },
    {
        "id": "11_vectores_en_memoria",
        "titulo": "Capítulo 11: Colecciones I: Vectores Vec<T> (Los Arrays Dinámicos)",
        "tema": "Crear, añadir y leer elementos. Acceso seguro con get() vs indexación directa. Iteración mutable e inmutable. Guardar varios tipos con enums."
    },
    {
        "id": "12_strings_utf8_sin_miedo",
        "titulo": "Capítulo 12: Colecciones II: Strings UTF-8 en Profundidad",
        "tema": "¿Por qué no se puede hacer s[0] en Rust? Bytes, valores escalares y grafemas. Manipulación, push_str, y la macro format!."
    },
    {
        "id": "13_hashmaps_diccionarios",
        "titulo": "Capítulo 13: Colecciones III: HashMaps (Los Diccionarios de Rust)",
        "tema": "Estructuras clave-valor en Heap. Inserción condicional con la API entry() y or_insert(). Conteo de frecuencia y propiedad de las claves."
    },
    {
        "id": "14_manejo_de_errores",
        "titulo": "Capítulo 14: Manejo de Errores: Result<T, E> y el Operador '?'",
        "tema": "Errores irrecuperables (panic!) vs recuperables (Result). Reemplazar el bloque try/catch por propagación con '?'. Uso responsable de expect y unwrap."
    },
    {
        "id": "15_modulos_y_visibilidad",
        "titulo": "Capítulo 15: Módulos y Crates: Arquitectura de Proyectos",
        "tema": "El árbol de módulos. Privacidad por defecto y el modificador pub. Rutas absolutas (crate::) y relativas (super::). Reexportación con pub use."
    },
    {
        "id": "16_genericos_y_traits",
        "titulo": "Capítulo 16: Genéricos y Traits: Interfaces con Superpoderes",
        "tema": "Genéricos en funciones y tipos frente a generics de TS. Traits como contratos de comportamiento. Trait bounds y derivación de Debug, Clone y PartialEq."
    },
    {
        "id": "17_lifetimes_sin_dolor",
        "titulo": "Capítulo 17: Lifetimes: El Tiempo de Vida de las Referencias",
        "tema": "Por qué existen los lifetimes y cómo previenen punteros colgantes. Sintaxis con 'a y reglas de elisión del compilador."
    },
    {
        "id": "18_closures_e_iteradores",
        "titulo": "Capítulo 18: Programación Funcional: Closures e Iteradores",
        "tema": "Closures frente a arrow functions de JS. Captura de entorno (Fn, FnMut, FnOnce). Iteradores y adaptadores funcionales: map, filter, fold."
    },
    {
        "id": "19_smart_pointers",
        "titulo": "Capítulo 19: Punteros Inteligentes: Box, Rc y RefCell",
        "tema": "Box<T> para memoria en Heap. Rc<T> para propiedad múltiple en un hilo. RefCell<T> y el patrón de mutabilidad interior."
    },
    {
        "id": "20_concurrencia_sin_miedo",
        "titulo": "Capítulo 20: Concurrencia sin Miedo: Hilos y Canales",
        "tema": "Creación de threads seguros con move. Canales de mensajes MPSC frente a eventos en Node.js. Estado compartido seguro con Mutex<T> y Arc<T>."
    },
    {
        "id": "21_proyecto_servidor_web",
        "titulo": "Capítulo 21: Proyecto Maestro: Servidor Web Concurrente",
        "tema": "Escucha TCP con TcpListener, lectura de peticiones HTTP, envío de respuestas y construcción de un ThreadPool multihilo para servir peticiones en paralelo."
    },
    {
        "id": "22_testing_automatizado",
        "titulo": "Capítulo 22: Testing Automatizado: El Arnés Nativo sin Jest ni Mocha",
        "tema": "El comando cargo test. Aserciones: assert!, assert_eq!, assert_ne!. Pruebas con #[should_panic]. Tests unitarios con #[cfg(test)] y mod tests. Tests de integración en /tests. Comparación con el ecosistema JS."
    },
    {
        "id": "23_asincronia_moderna",
        "titulo": "Capítulo 23: Asincronía Moderna: async/.await y Futures Frente a Node.js",
        "tema": "Problema C10K y límites de hilos del SO. Futures perezosos (pull-based) frente a Promises activas de JS (push-based). El runtime Tokio. async fn, bloques .await, tokio::spawn y carreras limpias con tokio::select!."
    },
    {
        "id": "24_tecnicas_avanzadas",
        "titulo": "Capítulo 24: Técnicas Avanzadas del Día a Día: dyn Trait, Deref y Structs con Lifetimes",
        "tema": "Despacho dinámico con Trait Objects (Box<dyn Trait>) frente a monomorfización estática. Coerción Deref automática. Structs con referencias usando 'a. El lifetime 'static y Graceful Shutdown con el trait Drop."
    },
    {
        "id": "25_unsafe_rust",
        "titulo": "Capítulo 25: Unsafe Rust: Rompiendo el Cristal de Emergencia",
        "tema": "¿Por qué existe unsafe y cuándo usarlo? Los 5 superpoderes de unsafe. Punteros crudos (*const T, *mut T) vs referencias seguras (&T). Modificar variables estáticas mutables globales. Llamar a código externo de C (FFI) y la regla de oro: encapsular código unsafe dentro de abstracciones seguras."
    },
    {
        "id": "26_macros_avanzadas",
        "titulo": "Capítulo 26: Macros Declarativas: Código que Escribe Código",
        "tema": "Diferencia fundamental entre funciones y macros. La sintaxis de macro_rules! y el pattern matching en código fuente. Metaprogramación frente a eval() o decorators de TypeScript. Creación paso a paso de una macro declarativa práctica."
    },
    {
        "id": "27_workspaces_cargo",
        "titulo": "Capítulo 27: Workspaces de Cargo: Monorrepositorios Profesionales",
        "tema": "Organización de grandes proyectos sin caos. El archivo Cargo.toml raíz con [workspace]. Compartir un único Cargo.lock y carpeta target/ de compilación. Dependencias internas entre crates. Comparativa directa con pnpm workspaces, Turborepo y npm monorepos."
    }
]

# ==========================================
# 4. SANEAMIENTO Y LIMPIEZA ANTI-GLITCH
# ==========================================
PATRON_CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff\uac00-\ud7af\ufffd]')
PATRON_AMPERSAND = re.compile(r"&(?!(?:amp|lt|gt|quot|apos);)")

def sanitizar_texto(texto: str, cap_id: str) -> str:
    """Elimina glifos parásitos, caracteres corruptos y garantiza el cierre de bloques de código."""
    texto = re.sub(r'([a-zA-Z0-9_]+)[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff\uac00-\ud7af\ufffd]+', r'\1', texto)
    texto = re.sub(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff\uac00-\ud7af\ufffd]+([a-zA-Z0-9_]+)', r'\1', texto)

    if cap_id != "12_strings_utf8_sin_miedo":
        texto = PATRON_CJK.sub('', texto)

    texto = texto.replace('\ufffd', '')

    # REPARACIÓN DE BLOQUES DE CÓDIGO ABIERTOS:
    # Si el número de delimitadores ``` es impar, se añade el cierre antes de que el archivo termine.
    bloques_codigo = re.findall(r'```', texto)
    if len(bloques_codigo) % 2 != 0:
        texto = texto.rstrip() + "\n```\n"

    return texto

# ==========================================
# 5. PROCESADOR DE SVGS Y CONTRASTE
# ==========================================
COLORES_ILEGIBLES = [
    r"#64748b", r"#94a3b8", r"#cbd5e1", r"#e2e8f0", r"#f1f5f9",
    r"#a1a1aa", r"#71717a", r"#d4d4d8", r"#e4e4e7",
    r"#f59e0b", r"#eab308", r"#fbbf24", r"#fde047",
    r"#38bdf8", r"#60a5fa", r"#818cf8",
    r"#4ade80", r"#86efac",
    r"#f87171", r"#fca5a5"
]
PATRON_COLORES_DEBILES = re.compile("|".join(COLORES_ILEGIBLES), re.IGNORECASE)

def optimizar_svg(codigo_svg: str) -> str:
    """Corrige entidades XML, sanea caracteres y optimiza contraste."""
    idx = codigo_svg.find("<svg")
    if idx != -1:
        codigo_svg = codigo_svg[idx:]

    codigo_svg = PATRON_AMPERSAND.sub("&amp;", codigo_svg)

    def reemplazar_fill(match):
        return PATRON_COLORES_DEBILES.sub("#0f172a", match.group(0))

    codigo_svg = re.sub(r'<text\b[^>]*>', reemplazar_fill, codigo_svg, flags=re.IGNORECASE)
    codigo_svg = re.sub(r'(<text\b(?![^>]*font-weight)[^>]*)>', r'\1 font-weight="600">', codigo_svg)
    codigo_svg = sanitizar_texto(codigo_svg, cap_id="")
    return codigo_svg

def procesar_y_extraer_svgs(texto_md: str, cap_id: str) -> str:
    """Extrae bloques SVG a archivos físicos e inserta enlaces Markdown."""
    patron_bloques = re.compile(r'```(?:xml|html|svg)?\s*(<svg[\s\S]*?</svg>)\s*```', re.IGNORECASE)
    patron_sueltos = re.compile(r'(<svg[\s\S]*?</svg>)', re.IGNORECASE)

    estado = {"contador": 1}

    def reemplazar_svg(match):
        num = estado["contador"]
        raw_svg = match.group(1).strip()
        svg_limpio = optimizar_svg(raw_svg)

        nombre_archivo = f"{cap_id}_img_{num}.svg"
        ruta_svg = OUTPUT_DIR / nombre_archivo
        ruta_svg.write_text(svg_limpio, encoding="utf-8")

        estado["contador"] += 1
        return f"\n\n![Diagrama {num}](capitulos/{nombre_archivo})\n\n"

    texto_procesado = patron_bloques.sub(reemplazar_svg, texto_md)
    texto_procesado = patron_sueltos.sub(reemplazar_svg, texto_procesado)
    return texto_procesado

# ==========================================
# 6. GENERACIÓN Y LLAMADAS A LA API
# ==========================================
def generar_capitulo(capitulo_info, forzar=False):
    file_path = OUTPUT_DIR / f"{capitulo_info['id']}.md"

    if not forzar and file_path.exists() and file_path.stat().st_size > 1000:
        contenido = file_path.read_text(encoding="utf-8")
        contenido_saneado = sanitizar_texto(contenido, capitulo_info['id'])
        if contenido != contenido_saneado:
            file_path.write_text(contenido_saneado, encoding="utf-8")
            print(f"🧹 Archivo existente saneado de formato/glifos: {file_path.name}")
        else:
            print(f"⏩ Omitiendo (ya existe y está limpio): {capitulo_info['titulo']}")
        return contenido_saneado

    print(f"⏳ Generando con {MODEL_NAME}: {capitulo_info['titulo']}...")

    prompt = f"""
Escribe en su totalidad el siguiente capítulo del libro:
TÍTULO: {capitulo_info['titulo']}

CONTENIDO OBLIGATORIO A CUBRIR:
{capitulo_info['tema']}

RECUERDA:
- Cierra SIEMPRE todos los bloques de código (```).
- Español pulcro sin mezclar caracteres asiáticos.
- Incluye 1 o 2 ilustraciones en formato SVG puro (<svg>...</svg>) con textos en color oscuro #0f172a.
- Cajas de resumen TDAH (🧠 EN 10 SEGUNDOS), comparaciones directas con TypeScript (🟦) y errores didácticos de compilación (🟥).
"""

    max_intentos = 3
    for intento in range(max_intentos):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3,
                ),
            )

            texto_crudo = sanitizar_texto(response.text, capitulo_info['id'])
            texto_final = procesar_y_extraer_svgs(texto_crudo, capitulo_info['id'])
            texto_final = sanitizar_texto(texto_final, capitulo_info['id'])
            file_path.write_text(texto_final, encoding="utf-8")
            print(f"✅ Guardado correctamente: {file_path}")
            time.sleep(3)
            return texto_final

        except Exception as e:
            print(f"⚠️ Error al generar {capitulo_info['id']} (Intento {intento+1}/{max_intentos}): {e}")
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print("Límite de cuota detectado. Esperando 25 segundos...")
                time.sleep(25)
            else:
                time.sleep(8)

    print(f"❌ No se pudo generar el capítulo {capitulo_info['id']}.")
    return ""

# ==========================================
# 7. ENSAMBLADO Y COMPILACIÓN TYPST
# ==========================================
def ensamblar_libro():
    print("\n📚 Ensamblando todos los capítulos en libro_completo.md...")
    with open(COMPLETED_BOOK_MD, "w", encoding="utf-8") as f_out:
        f_out.write("""# 🦀 Rust sin Dolor: La Guía Visual y Directa al Grano
*Aprende gestión de memoria sin basura desde TypeScript y JavaScript con enfoque neurodivergente.*

---

\\pagebreak

""")
        for cap in CAPITULOS:
            file_path = OUTPUT_DIR / f"{cap['id']}.md"
            if file_path.exists():
                texto = file_path.read_text(encoding="utf-8")
                texto = sanitizar_texto(texto, cap['id'])
                f_out.write(texto)
                f_out.write("\n\n\\pagebreak\n\n")

    print(f"✔ Archivo Markdown global listo: {COMPLETED_BOOK_MD}")

def compilar_pdf():
    print("\n⚙️ Compilando PDF final con Pandoc y Typst...")
    comando = (
        f"pandoc {COMPLETED_BOOK_MD} "
        f"-o {FINAL_PDF} "
        f"--pdf-engine=typst "
        f"--toc "
        f"--toc-depth=2 "
        f"-V mainfont=\"Liberation Sans\" "
        f"-V fontsize=11pt"
    )
    resultado = os.system(comando)
    if resultado == 0:
        print(f"\n🎉 ¡LIBRO GENERADO CON ÉXITO! Ubicación: {FINAL_PDF.resolve()}")
    else:
        print("\n⚠ Ocurrió un error al compilar el PDF con Pandoc.")
        print(f"Comando utilizado: {comando}")

# ==========================================
# 8. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    forzar_regeneracion = "--force" in sys.argv
    limpiar_solamente = "--clean-only" in sys.argv

    if forzar_regeneracion:
        print("⚡ Modo --force: Se regenerarán todos los capítulos.")
    elif limpiar_solamente:
        print("🧹 Modo --clean-only: Saneando archivos existentes sin llamar a la API...")

    if not limpiar_solamente:
        for cap in CAPITULOS:
            generar_capitulo(cap, forzar=forzar_regeneracion)
    else:
        for cap in CAPITULOS:
            f = OUTPUT_DIR / f"{cap['id']}.md"
            if f.exists():
                txt = sanitizar_texto(f.read_text(encoding="utf-8"), cap['id'])
                f.write_text(txt, encoding="utf-8")
        print("✔ Limpieza completada.")

    ensamblar_libro()
    compilar_pdf()
