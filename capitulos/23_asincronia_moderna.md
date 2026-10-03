# Capítulo 23: Asincronía Moderna: async/.await y Futures Frente a Node.js

> 🧠 **EN 10 SEGUNDOS (TDAH):** 
> En Rust, un `Future` no hace nada hasta que alguien lo ejecuta (es perezoso). Usamos un runtime como Tokio para manejar millones de conexiones ligeras usando pocos hilos de sistema operativo.

---

## 1. El Problema del Millón de Conexiones (C10K) y los Hilos del Sistema Operativo

Imagina que estás organizando una fiesta. Si le asignas un mesero exclusivo a cada invitado (como hacen los hilos tradicionales del SO), tu casa colapsa rápido porque los meseros ocupan espacio y energía física, aunque los invitados estén en silencio. 

En programación, un hilo del sistema operativo consume memoria dedicada (unos 2 Megabytes para el Stack) y requiere cambios de contexto costosos en la CPU. Si intentas abrir 10,000 conexiones concurrentes con hilos puros, tu servidor se queda sin memoria o pasa más tiempo cambiando de hilo que procesando datos reales.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** 
> En Node.js estás acostumbrado al modelo *Event Loop*. Un solo hilo ejecuta tu código de JavaScript de forma asíncrona mediante callbacks, Promises y eventos del sistema operativo subyacente (como `libuv`). Rust te da una velocidad similar o superior, pero **sin un hilo principal obligatorio oculto**, permitiéndote decidir exactamente cómo y dónde corre tu código.

---

## 2. El Modelo de Rust: Futures Perezosos (Pull-Based) vs. Promesas de JS (Push-Based)

Aquí está la diferencia mental más importante que debes hacer:

*   **JavaScript (Push-based):** Una `Promise` en JS nace corriendo. En el momento exacto en que la creas, el motor comienza a trabajar en segundo plano.
*   **Rust (Pull-based):** Un `Future` en Rust es un objeto pasivo. No hace **absolutamente nada** hasta que alguien lo llama (`poll`) explícitamente y lo empuja hacia adelante.



![Diagrama 1](capitulos/23_asincronia_moderna_img_1.svg)



---

## 3. ¿Por qué Rust no trae Runtime por Defecto?

A diferencia de Go o Node.js, Rust no incluye un recolector de basura ni un motor asíncrono incrustado en el lenguaje. 

*   **Filosofía de Rust:** No pagas por lo que no usas. Si creas un microcontrolador embebido de 8 KB, no quieres un pesado sistema de tareas asíncronas consumiendo recursos.
*   **La Solución:** Delegamos el trabajo pesado a crates externos probados en batalla. El rey indiscutible del ecosistema es **Tokio**.

---

## 4. Sintaxis Práctica: async fn, .await y Tokio

Para usar asincronía en Rust, decoramos nuestras funciones con `async fn` y usamos la macro principal de Tokio para inicializar el motor del runtime.

```rust
// Agrega tokio = { version = "1.40", features = ["full"] } en tu Cargo.toml
use tokio::time::{sleep, Duration};

async fn descargar_datos(id: u32) -> String {
    // Simulamos una operación de red no bloqueante
    sleep(Duration::from_secs(1)).await;
    format!("Datos del usuario {}", id)
}

#[tokio::main]
async fn main() {
    println!("Iniciando descargas...");

    // Llamamos a la función async (devuelve un Future perezoso)
    let futuro_usuario = descargar_datos(42);

    // El .await pausa esta función hasta que el Future termine
    let resultado = futuro_usuario.await;
    
    println!("{}", resultado);
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si intentas llamar a una función `async fn` sin ponerle `.await` al final, el compilador te gritará algo como esto:
> ```text
> warning: unused `impl std::future::Future` that must be used
>   --> src/main.rs:10:5
>   |
> 10 |     descargar_datos(42);
>   |     ^^^^^^^^^^^^^^^^^^^^
>   |
>   = note: futures do nothing unless you `.await` or poll them
> ```
> **El bug que evita:** Olvidar el `.await` en JS suele devolver una `Promise` vacía y romper tu lógica silenciosamente. En Rust, el compilador te obliga a reconocer explícitamente que tienes un futuro pendiente de resolución.

---

## 5. Concurrencia Avanzada: tokio::spawn y tokio::select!

Cuando quieres ejecutar múltiples tareas en paralelo sin bloquear el hilo principal, usas `tokio::spawn` para lanzar tareas independientes (tasks) y `tokio::select!` para competir entre varias operaciones asíncronas (el primero que responda gana).

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    // Lanzamos dos tareas concurrentes en segundo plano
    let tarea_1 = tokio::spawn(async {
        sleep(Duration::from_millis(500)).await;
        "Resultado de Tarea 1"
    });

    let tarea_2 = tokio::spawn(async {
        sleep(Duration::from_millis(200)).await;
        "Resultado de Tarea 2"
    });

    // tokio::select! espera a que la primera tarea termine
    tokio::select! {
        res1 = tarea_1 => println!("Ganó: {:?}", res1),
        res2 = tarea_2 => println!("Ganó: {:?}", res2),
    }
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:**
> `tokio::spawn` es conceptualmente muy similar a disparar una promesa en JS sin hacerle `await` inmediato (ej. `Promise.all` o simplemente iniciar tareas independientes). Por su parte, `tokio::select!` es el equivalente robusto y seguro en tipos de `Promise.race([])`, pero optimizado a nivel de sistema para cancelar las ramas perdedoras de manera automática y limpia.