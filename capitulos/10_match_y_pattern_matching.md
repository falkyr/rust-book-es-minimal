# Capítulo 10: Pattern Matching: La Máquina Clasificadora Perfecta

> 🧠 **EN 10 SEGUNDOS (TDAH):** El `match` es un switch con esteroides. Obliga a tu código a considerar *absolutamente todos* los casos posibles de un dato. Si olvidas uno, el compilador explota antes de que toques el teclado.

---

El pattern matching en Rust no es solo comparar valores; es una **máquina clasificadora** que desarma estructuras complejas, extrae sus datos internos y dirige el flujo del programa con precisión milimétrica.

## 1. La instrucción `match` exhaustiva

Imagina una máquina de correos ultra estricta. Si llega un paquete, debe estar clasificado en una categoría conocida. No existe el "caso por defecto" flojo (`default` en JS) a menos que lo pidas explícitamente.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS usas `switch`. Si olvidas un `break`, el código cae en cascada (bug clásico). En TS usas `switch` con `never` para forzar exhaustividad. Rust hace esto de serie, por diseño y sin trucos.

```rust
enum EstadoServidor {
    Apagado,
    Iniciando(u32), // Contiene el puerto de arranque
    Activo(&amp;'static str), // Contiene la URL
}

fn auditar_estado(estado: EstadoServidor) {
    match estado {
        EstadoServidor::Apagado => {
            println!("El servidor está durmiendo.");
        }
        EstadoServidor::Iniciando(puerto) => {
            println!("Arrancando en el puerto {}...", puerto);
        }
        EstadoServidor::Activo(url) => {
            println!("¡En línea y sirviendo en {}!", url);
        }
    }
}
```

---

## 2. Desestructuración de datos en variantes

El `match` abre las cajas (`structs`, `enums`, `tuples`) y te entrega su contenido directamente en las variables que defines en los brazos (`arms`).

```rust
struct Coordenada {
    x: i32,
    y: i32,
}

fn analizar_punto(punto: Coordenada) {
    match punto {
        Coordenada { x: 0, y: 0 } => println!("Origen exacto"),
        Coordenada { x, y: 0 } => println!("Sobre el eje X en {}", x),
        Coordenada { x: 0, y } => println!("Sobre el eje Y en {}", y),
        Coordenada { x, y } => println!("Punto libre en ({}, {})", x, y),
    }
}
```

### Visualizando el Desarme de Datos (SVG)



![Diagrama 1](capitulos/10_match_y_pattern_matching_img_1.svg)



---

## 3. Atajos elegantes: `if let` y `let...else`

A veces, un `match` completo es demasiado pesado cuando solo te importa **un** caso y quieres ignorar el resto. Para eso existen los atajos del "camino feliz" (*happy path*).

### `if let`: Cuando solo te importa un caso

```rust
fn procesar_config(modo_oscuro: Option<bool>) {
    // Si es Some(true), entra. Si es None o Some(false), lo ignora limpiamente.
    if let Some(true) = modo_oscuro {
        println!("Activando interfaz nocturna...");
    }
}
```

### `let...else`: Protección temprana (*guard clauses*)

Introducido para evitar la pirámide de la perdición (anidaciones profundas). Si el patrón falla, ejecutas código que rompe el flujo obligatoriamente (`return`, `break`, `panic!`).

```rust
fn obtener_id(usuario: Option<u32>) -> u32 {
    // Si es Some(id), lo extrae. Si es None, ejecuta el bloque else y sale.
    let Some(id) = usuario else {
        return 0; // Valor por defecto de salida rápida
    };

    id + 100 // Código principal limpio, sin indentación extra
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Si omites un caso en un `match`, el compilador te gritará con furia:
> `error[E0004]: non-exhaustive patterns: \`None\` not covered`.
> **Bug evitado:** Cero excepciones en producción por estados no contemplados como `null` o `undefined` imprevistos. Rust te obliga a pensar en cada escenario antes de compilar.