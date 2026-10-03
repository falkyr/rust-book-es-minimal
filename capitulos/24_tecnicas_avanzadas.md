# Capítulo 24: Técnicas Avanzadas del Día a Día: dyn Trait, Deref y Structs con Lifetimes

> 🧠 **EN 10 SEGUNDOS (TDAH):** Hoy aprenderemos herramientas de nivel senior: polimorfismo flexible con `dyn Trait`, conversión automática de tipos con `Deref`, cómo guardar referencias dentro de structs usando `lifetimes`, y cómo apagar hilos de forma ordenada con el trait `Drop`.

---

## 1. Polimorfismo: `impl Trait` (Estático) vs `dyn Trait` (Dinámico)

Hasta ahora hemos usado genéricos (`<T: Trait>`) y `impl Trait`. Esto se conoce como **despacho estático** (static dispatch). 
El compilador clona el código para cada tipo concreto que uses en tiempo de compilación (un proceso llamado *monomorphization*). Es ultra rápido, pero todos los elementos de una colección deben ser exactamente del mismo tipo.

¿Qué pasa si quieres una lista (`Vec`) que contenga structs totalmente diferentes pero que cumplan el mismo `Trait`? Aquí entra el **despacho dinámico** (dynamic dispatch) usando `dyn Trait` detrás de un puntero como `Box<dyn Trait>` o `&dyn Trait`.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS todo es dinámico por defecto; puedes meter objetos con la misma interfaz en un array sin preocuparte. En Rust, por defecto todo es estático y estricto. Usar `Box<dyn Trait>` es la forma explícita de decir: *"Quiero polimorfismo de tiempo de ejecución como en TypeScript"*.

### Ilustración: Despacho Estático vs Dinámico



![Diagrama 1](capitulos/24_tecnicas_avanzadas_img_1.svg)



> 🟥 **FRENAZO DEL COMPILADOR:** Si intentas crear `let lista: Vec<dyn Trait> = ...`, Rust te dirá que el trait no tiene un tamaño conocido en tiempo de compilación (*size known at compile-time*). Por eso siempre debes envolverlo en un puntero indirecto como `Box<dyn Trait>` o `&dyn Trait`.

---

## 2. Coerción Deref: Magia Limpia y Sin Coste

El operador `*` se usa para desreferenciar un puntero y acceder al valor interno. Pero Rust va más allá con el trait `Deref`. Gracias a esto, un `&String` se convierte automáticamente en un `&str`, y un `&Vec<T>` en un `&slice<T>` (`&[T]`).

Esto explica por qué puedes pasar una referencia a un `String` a una función que espera un `&str` sin escribir asteriscos molestos.

```rust
fn imprimir_texto(s: &str) {
    println!("Texto: {}", s);
}

fn main() {
    let meu_string = String::from("Hola Rust 2024");
    
    // Coerción Deref automática: &String se convierte en &str
    imprimir_texto(&meu_string);
}
```

---

## 3. Structs con Lifetimes: Almacenando Referencias

Si un `struct` contiene una referencia (ej. `&str`), el compilador de Rust **exige** que declares un parámetro de lifetime (`'a`) para garantizar que la referencia dentro del struct nunca sobreviva al dato original al que apunta.

```rust
// Este struct no posee los datos, solo los presta (borrow)
struct Articulo<'a> {
    titulo: &'a str,
    contenido: &'a str,
}

fn main() {
    let texto_largo = String::from("Rust es seguro y rápido.");
    
    let articulo = Articulo {
        titulo: "Aviso",
        contenido: &texto_largo,
    };

    println!("Artículo: {} -> {}", articulo.titulo, articulo.contenido);
} // articulo muere aquí, texto_largo muere después. ¡Todo seguro!
```

> 🟥 **FRENAZO DEL COMPILADOR:** Si omites el lifetime (`struct Articulo { titulo: &str }`), el compilador te lanzará un error de *missing lifetime specifier*. Rust se niega a compilar código donde no esté claro quién es el dueño del dato prestado.

---

## 4. El Lifetime `'static`

El lifetime `'static` es especial. Significa que el dato vive **durante toda la ejecución del programa**.

1. **Literales de texto:** Todos los strings escritos directamente en el código (`&str`) tienen por defecto el lifetime `'static` porque están incrustados en el binario ejecutable.
2. **Hilos concurrentes:** En concurrencia, `T: 'static` significa que el tipo no contiene referencias prestadas de vida corta, por lo que es seguro enviarlo a otro hilo mediante `std::thread::spawn`.

---

## 5. Graceful Shutdown usando el trait `Drop`

Cuando un recurso sale de scope en Rust, se ejecuta automáticamente su destructor implementando el trait `Drop`. Esto es la base del patrón RAII (*Resource Acquisition Is Initialization*).

Imagina un ThreadPool avanzado: cuando el pool se destruye, queremos avisar a los hilos de que terminen de procesar sus tareas pendientes de forma ordenada (*Graceful Shutdown*).

```rust
use std::thread;
use std::sync::{mpsc, Arc, Mutex};

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize) -> Worker {
        // Creamos un hilo simulado
        let handle = thread::spawn(move || {
            println!("Worker {} iniciado.", id);
        });

        Worker {
            id,
            thread: Some(handle),
        }
    }
}

struct MiThreadPool {
    workers: Vec<Worker>,
}

// Implementamos Drop para asegurar un apagado limpio
impl Drop for MiThreadPool {
    fn drop(&mut self) {
        println!("\nApagando ThreadPool ordenadamente (Graceful Shutdown)...");

        for worker in &mut self.workers {
            println!("Apagando worker id: {}", worker.id);
            
            if let Some(thread_handle) = worker.thread.take() {
                thread_handle.join().unwrap();
            }
        }
    }
}

fn main() {
    let pool = MiThreadPool {
        workers: vec![Worker::new(1), Worker::new(2)],
    };

    println!("El programa principal está haciendo tareas...");
} // <- Aquí la variable 'pool' sale de scope, se ejecuta Drop automáticamente y se unen los hilos.
```

---

## Resumen del Capítulo

- **Despacho Dinámico (`dyn Trait`):** Permite colecciones heterogéneas usando punteros inteligentes como `Box<dyn Trait>`.
- **Deref Coercion:** Conversión automática de tipos derivados a tipos base (`&String` a `&str`).
- **Structs con Lifetimes (`'a`):** Garantizan que las referencias internas no superen en vida al dato original.
- **Trait `Drop`:** Control total sobre el momento en que los recursos se destruyen, clave para un apagado seguro de hilos.