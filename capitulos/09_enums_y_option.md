# Capítulo 9: Enums con Datos y el Fin de los Errores por Null

> 🧠 **EN 10 SEGUNDOS (TDAH):** En Rust, los `enum` pueden guardar datos adentro, y el infame `null` no existe. Usamos `Option<T>` para representar algo que puede estar o no, obligándote a manejar el caso vacío de forma segura.

---

### El error del billón de dólares

En lenguajes antiguos, Tony Hoare inventó la referencia `null` en 1965 porque era "fácil de implementar". Él mismo lo llamó su error de los mil millones de dólares. 

¿Por qué? Porque intentar acceder a una propiedad o método de un valor `null` o `undefined` rompe tu aplicación en producción de la nada. Rust elimina este problema de raíz: no hay valores nulos.



![Diagrama 1](capitulos/09_enums_y_option_img_1.svg)



---

### Enums Enriquecidos: Mucho más que simples números

En lenguajes como C o Java, un `enum` es solo una lista de números enteros disfrazados. En Rust, los `enum` son **tipos algebraicos de datos**. Cada variante puede contener estructuras de datos completamente diferentes.

```rust
// Definimos un enum para manejar mensajes de una interfaz gráfica
enum Mensaje {
    Salir,                        // Sin datos
    Escribir(String),             // Contiene un String
    Coordenada { x: i32, y: i32 }, // Contiene una estructura con nombres
    CambiarColor(u8, u8, u8),     // Contiene tres números
}

fn procesar_mensaje(msg: Mensaje) {
    match msg {
        Mensaje::Salir => {
            println!("Saliendo del programa...");
        }
        Mensaje::Escribir(texto) => {
            println!("Texto recibido: {}", texto);
        }
        Mensaje::Coordenada { x, y } => {
            println!("Mover a X: {}, Y: {}", x, y);
        }
        Mensaje::CambiarColor(r, g, b) => {
            println!("Color RGB: {}, {}, {}", r, g, b);
        }
    }
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TypeScript puedes lograr algo similar usando *Discriminated Unions* (`type Msg = { type: 'salir' } | { type: 'escribir', texto: string }`). La diferencia clave es que Rust valida de forma estricta en el compilador que **nunca** olvides cubrir un caso en el `match`.

---

### El tipo `Option<T>` al rescate

Cuando una función puede devolver un resultado o nada, Rust no devuelve `null`. Devuelve una variante del enum `Option<T>`, que está definido en la biblioteca estándar de esta manera:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Imagina que buscas un usuario en una base de datos. O lo encuentras (`Some(usuario)`), o no existe (`None`).

```rust
fn buscar_usuario(id: u32) -> Option<String> {
    if id == 1 {
        Some(String::from("Carlos"))
    } else {
        None
    }
}

fn main() {
    let resultado = buscar_usuario(2);

    match resultado {
        Some(nombre) => println!("Usuario encontrado: {}", nombre),
        None => println!("El usuario no existe en el sistema."),
    }
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** 
> Si intentas usar un `Option<String>` directamente como si fuera un `String` sin antes abrir la caja con `match` o métodos seguros, el compilador se detendrá inmediatamente:
> ```text
> error[E0308]: mismatched types
>  --> src/main.rs:10:20
>   |
> 9 |     let longitud = resultado.len();
>   |                    ^^^^^^^^^^^^^^^ no method named `len` found for enum `Option<String>`
>   |
>   = note: Usar `match` o métodos como `.unwrap_or()` para acceder al valor interno.
> ```
> El compilador te obliga físicamente a pensar: *"¿Qué pasa si esto es `None`?"*.

---

### Desempaquetado seguro y elegante

Aunque `match` es la herramienta definitiva, Rust provee métodos muy útiles para casos comunes sin escribir tanta planilla de código:

1. **`unwrap_or(valor_por_defecto)`**: Si es `Some(v)`, devuelve `v`. Si es `None`, devuelve el valor por defecto que tú elijas.
2. **`if let`**: Ideal cuando solo te interesa un caso específico y quieres ignorar el resto.



![Diagrama 2](capitulos/09_enums_y_option_img_2.svg)



Ejemplo práctico usando `if let`:

```rust
fn main() {
    let configuracion_puerto: Option<u16> = Some(8080);

    // Solo nos importa si hay un puerto configurado
    if let Some(puerto) = configuracion_puerto {
        println!("Servidor corriendo en el puerto {}", puerto);
    } else {
        println!("Usando puerto por defecto.");
    }
}
```
