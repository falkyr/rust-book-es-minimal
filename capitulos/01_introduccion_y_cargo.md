# Capítulo 1: ¿Por qué Rust? De C y JavaScript al Vigilante en la Entrada

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust te da la velocidad brutal de C sin que tu programa explote por corrupción de memoria, y sin el recolector de basura lento de JavaScript o Java. El compilador es tu vigilante personal de seguridad.

---

¿Por qué existe tanto revuelo con Rust? Para entenderlo, debemos mirar los dos extremos del mundo de la programación actual: **JavaScript** y **C/C++**.

Por un lado, JavaScript (y TypeScript) oculta la memoria. Un conserje automático llamado *Garbage Collector* (GC) limpia la basura por ti. Es cómodo, pero impredecible: de repente, tu app se congresa unos milisegundos porque el GC decidió limpiar la casa.

Por otro lado, C y C++ te dan control total del hardware. Tú pides memoria y tú debes liberarla. Si olvidas liberarla, tienes una fuga. Si la liberas dos veces o escribes donde no debes, tu programa sufre un fallo catastrófico (*Segmentation Fault*) o abre brechas de seguridad críticas.

Rust entra en escena como una tercera vía revolucionaria: **control total sin Garbage Collector, pero con un compilador estricto que te impide cometer errores de memoria antes de que tu código corra.**

---

## Memoria: El Baile de las Sillas

Para entender por qué Rust es diferente, mira este diagrama de cómo se gestiona la memoria en los diferentes lenguajes:



![Diagrama 1](capitulos/01_introduccion_y_cargo_img_1.svg)



> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TS, si creas un objeto gigante, el motor V8 se encarga de borrarlo cuando ya no se usa. En Rust, el compilador calcula exactamente en qué línea de código ese objeto muere y genera la instrucción de limpieza en el código máquina de forma milimétrica.

---

## Instalación y el Ecosistema Cargo

Para empezar a programar en Rust, necesitamos instalar dos herramientas principales: `rustc` (el compilador) y `cargo` (el gestor de paquetes y sistema de compilación).

La forma oficial y recomendada en sistemas Unix (Linux/macOS) o WSL en Windows es ejecutar:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Cargo vs npm: Tu nuevo mejor amigo

Si vienes de Node.js, `cargo` te resultará familiar de inmediato. Es el equivalente combinado a **npm + webpack + tsconfig**.

| Característica | Node.js (npm) | Rust (Cargo) |
| :--- | :--- | :--- |
| **Archivo de Configuración** | `package.json` | `Cargo.toml` |
| **Bloqueo de Dependencias** | `package-lock.json` | `Cargo.lock` |
| **Carpeta de Módulos** | `node_modules/` | `target/` |
| **Comando para Ejecutar** | `npm run start` | `cargo run` |
| **Comando para Compilar** | N/A (Interpretado/JIT)| `cargo build --release` |

---

## Anatomía de un Proyecto y el archivo `main.rs`

Crea un nuevo proyecto ejecutable usando la terminal con Cargo:

```bash
cargo new hola_rust
cd hola_rust
```

Esto generará la siguiente estructura de archivos:

```text
hola_rust/
├── Cargo.toml
└── src/
    └── main.rs
```

### El archivo `Cargo.toml`

Aquí defines los metadatos de tu aplicación y las librerías externas (llamadas *crates*):

```toml
[package]
name = "hola_rust"
version = "0.1.0"
edition = "2024"

[dependencies]
# Aquí agregarás tus librerías externas más adelante
```

### El archivo `src/main.rs`

Ábrelo con tu editor favorito (como VS Code). Este es el punto de entrada clásico de cualquier programa en Rust:

```rust
fn main() {
    println!("¡Hola, mundo desde Rust!");
}
```

- **`fn main()`**: Define la función principal donde inicia la ejecución del programa.
- **`println!`**: Es una **macro** de Rust (notalo por el signo de exclamación `!`). Imprime texto en la consola de manera optimizada y segura.

> 🟥 **FRENAZO DEL COMPILADOR:** En JavaScript puedes escribir `console.log(x)` sin declarar variables y el código corre (hasta que peta en producción). En Rust, si olvidas el punto y coma `;` al final de una sentencia o escribes mal una llave, el compilador de Rust no generará ningún binario. Te detendrá en seco y te señalará exactamente el carácter erróneo con una amabilidad quirúrgica.