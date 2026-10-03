# Capítulo 14: Manejo de Errores: Result<T, E> y el Operador '?'

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust no usa excepciones invisibles (`try/catch`). Los errores normales se manejan explícitamente con el `enum Result<T, E>`, que dice: *"O tengo el dato exitoso T, o tengo el error E"*. El operador `?` es un atajo limpio para propagar errores hacia arriba sin escribir código repetitivo.

---

## 1. El Choque de Trenes: Errores Irrecuperables vs Recuperables

En la programación tradicional, cuando algo falla (como intentar leer un archivo que no existe), lanzamos una excepción mágica que viaja por la pila de llamadas. En Rust, dividimos los problemas en dos mundos completamente separados:

1. **Irrecuperables (`panic!`):** Son bugs de programación catastróficos. Intentar acceder a un array fuera de sus límites o dividir por cero. El programa se detiene de inmediato para evitar corromper la memoria.
2. **Recuperables (`Result<T, E>`):** Son situaciones esperadas del mundo real. La red se cayó, el usuario escribió mal su contraseña, o el archivo no está en el disco. Rust te obliga a mirar el error a los ojos y decidir qué hacer.

```rust
fn conectar_base_datos(url: &str) -> Result<Conexion, ErrorRed> {
    if url.is_empty() {
        return Err(ErrorRed::UrlInvalida); // Error recuperable
    }
    
    // Si la máquina explota físicamente, usamos panic!
    if !servidor_encendido() {
        panic!("¡El servidor de base de datos se desintegró!");
    }

    Ok(Conexion { ... })
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TS/JS usas `try { ... } catch (e) { ... }` y asumes que cualquier función puede lanzar un error invisible. En Rust, **no hay excepciones**. El tipo de retorno de la función te avisa explícitamente si puede fallar mediante el `Result`.

---

## 2. Anatomía Visual de un `Result` y el Operador `?`

Imagina que el `Result` es una caja blindada que puede contener un regalo brillante (`Ok`) o una carta de desalojo (`Err`).



![Diagrama 1](capitulos/14_manejo_de_errores_img_1.svg)



### El Poder del Operador `?`

El signo de interrogación (`?` colocado al final de una expresión) es un werolk (atajo mágico) que reemplaza cientos de líneas de código repetitivo de manejo de errores. 

Veamos cómo se lee: *"Intenta ejecutar esto. Si da `Ok`, extrae su valor interno y continúa. Si da `Err`, sal de esta función inmediatamente devolviendo ese error"*.

```rust
use std::fs::File;
use std::io::{self, Read};

fn leer_configuracion() -> Result<String, io::Error> {
    // Si File::open falla, retorna el error io::Error de inmediato
    let mut archivo = File::open("config.json")?;
    
    let mut contenido = String::new();
    
    // Si read_to_string falla, también propaga el error hacia arriba
    archivo.read_to_string(&mut contenido)?;

    Ok(contenido)
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS moderno, el operador `?` se usa para encadenar propiedades nulas (`user?.name`). En Rust, el operador `?` equivale conceptualmente a hacer un `try/catch` implícito que hace `return err` si ocurre un fallo.

---

## 3. Las Muletas Peligrosas: `unwrap()` y `expect()`

A veces, escribir código robusto toma tiempo y solo quieres probar algo rápido. Rust te ofrece dos métodos para "forzar" la extracción de un `Result` sin manejar el error:

- **`unwrap()`**: Extrae el valor `Ok`. Si encuentra un `Err`, **hace pánico (`panic!`) y crashea el programa**.
- **`expect("mensaje")`**: Hace lo mismo que `unwrap()`, pero imprime un mensaje personalizado en la consola antes de morir.

```rust
fn main() {
    // PELIGRO: Si el archivo no existe, el programa explota.
    let archivo = File::open("inexistente.txt").unwrap();

    // MEJOR: Al menos dejamos una pista clara de por qué morimos.
    let configuracion = File::open("settings.toml")
        .expect("¡FATAL! No se encontró el archivo de configuración principal.");
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Usar `unwrap()` en código de producción es una mala práctica mal vista en la comunidad de Rust. Si dejas un `unwrap()` suelto, el compilador no te impedirá compilar, pero tu aplicación se derrumbará ante el primer imprevisto real.
> 
> **Regla de oro:** Reserva `unwrap()` y `expect()` exclusivamente para **prototipos rápidos**, **tests automatizados**, o cuando estás **100% seguro** de que un estado es imposible de alcanzar (por ejemplo, al compilar una expresión regular estática).

---

## 4. Combinando `Result` con Pattern Matching (`match`)

Cuando el error no debe propagarse, sino resolverse localmente, el `match` es tu mejor aliado. Puedes inspeccionar ambas variantes con precisión quirúrgica:

```rust
use std::fs::File;

fn main() {
    let resultado = File::open("datos.csv");

    let _archivo = match resultado {
        Ok(f) => {
            println!("¡Archivo abierto con éxito!");
            f
        }
        Err(e) => {
            println!("No se pudo abrir el archivo por esta razón: {e}");
            // Creamos un archivo por defecto o manejamos la situación
            return;
        }
    };
}
```

Con este dominio del `Result` y el operador `?`, ya no dependes de la suerte ni de bloques `try/catch` ocultos. Tus programas en Rust son transparentes, predecibles y seguros frente a cualquier imprevisto del mundo real.