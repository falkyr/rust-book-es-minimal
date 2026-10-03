# Capítulo 20: Concurrencia sin Miedo: Hilos y Canales

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust te deja correr código en paralelo (varias cosas a la vez) bloqueando los peores bugs antes de compilar. Si intentas compartir datos sin protección, el compilador te grita. Punto.

---

## 1. El Caos del Estado Compartido vs Concurrencia Segura

En la programación tradicional, correr múltiples hilos (*threads*) en paralelo es una receta para el desastre: dos hilos modifican el mismo espacio de memoria al mismo tiempo y ¡boom!, corrupción de datos o comportamientos raros imposibles de replicar.

Rust elimina el 100% de las *Data Races* (carreras de datos) directamente en su sistema de tipos y ownership.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En Node.js vives en un mundo de un solo hilo con un *Event Loop* asíncrono. Si quieres paralelismo real, usas `Worker Threads` y pasas mensajes mediante `postMessage()`. Rust te da hilos nativos del sistema operativo de verdad, pero con un guardián incorruptible (el compilador).

---

## 2. Creando Hilos con `std::thread::spawn` y la palabra clave `move`

Para crear un hilo nuevo en Rust usamos `thread::spawn`. Le pasamos un closure con el código que queremos ejecutar en segundo plano.

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..5 {
            println!("Hola desde el hilo secundario: {}", i);
            thread::sleep(Duration::from_millis(100));
        }
    });

    for i in 1..3 {
        println!("Hola desde el hilo principal: {}", i);
        thread::sleep(Duration::from_millis(100));
    }

    // Esperamos a que el hilo secundario termine
    handle.join().unwrap();
}
```

¿Qué pasa si el hilo secundario necesita usar una variable que fue creada en el hilo principal? Por defecto, Rust intentará hacer un préstamo (*borrow*), pero el hilo principal podría morir antes de que el secundario use el dato.

La solución es usar la palabra clave `move` para transferir la propiedad (*ownership*) al nuevo hilo:

```rust
use std::thread;

fn main() {
    let mensaje = String::from("¡Hola desde el hilo con ownership!");

    // 'move' fuerza a que este hilo sea dueño absoluto de 'mensaje'
    let handle = thread::spawn(move || {
        println!("{}", mensaje);
    });

    handle.join().unwrap();
    // println!("{}", mensaje); // ERROR: 'mensaje' ya fue movido al otro hilo
}
```

---

## 3. Ilustración Visual: El Ciclo de Vida y el Movimiento (`move`)



![Diagrama 1](capitulos/20_concurrencia_sin_miedo_img_1.svg)



---

## 4. Canales de Mensajes: MPSC (Multi-Producer, Single-Consumer)

En lugar de compartir datos directamente, la filosofía recomendada en Rust es: *"No compartas memoria comunicándote mediante variables; comunícate compartiendo memoria mediante mensajes"*.

Usamos un canal `mpsc` (*Multiple Producer, Single Consumer*): muchos hilos pueden enviar datos, pero uno solo los recibe.

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    // Creamos el canal: tx (transmitter), rx (receiver)
    let (tx, rx) = mpsc::channel();

    let tx1 = tx.clone(); // Clonamos el emisor para el segundo hilo

    // Hilo 1
    thread::spawn(move || {
        let vals = vec![String::from("hi"), String::from("from"), String::from("thread 1")];
        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_millis(200));
        }
    });

    // Hilo 2
    thread::spawn(move || {
        let vals = vec![String::from("saludos"), String::from("desde"), String::from("hilo 2")];
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_millis(200));
        }
    });

    // Hilo principal recibiendo los mensajes bloqueándose hasta que llegan
    for recibido in rx {
        println!("Mensaje got: {}", recibido);
    }
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS, para pasar mensajes entre Web Workers, usas `worker.postMessage()` y escuchas eventos `on('message')`. El canal MPSC de Rust hace exactamente lo mismo, pero tipado fuertemente de extremo a extremo, garantizando que el receptor sepa exactamente qué tipo de estructura de datos va a leer.

---

## 5. Estado Compartido Seguro: `Mutex<T>` y `Arc<T>`

A veces necesitas que múltiples hilos modifiquen exactamente el mismo dato en memoria. Para lograrlo de forma segura usamos dos herramientas combinadas:

1. **`Mutex<T>` (Mutual Exclusion):** Permite que un solo hilo acceda al dato a la vez. Bloquea a los demás hasta que libera el recurso.
2. **`Arc<T>` (Atomic Reference Counted):** Un contador de referencias atómico y seguro para hilos que permite que múltiples dueños apunten al mismo `Mutex` en diferentes hilos.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    // Envolvemos el contador en un Mutex y luego en un Arc
    let contador = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let contador_clon = Arc::clone(&contador);
        let handle = thread::spawn(move || {
            // .lock().unwrap() adquiere el permiso de escritura de forma segura
            let mut num = contador_clon.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Resultado final: {}", *contador.lock().unwrap());
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si intentas usar un `Rc<T>` normal en lugar de un `Arc<T>` para compartir datos entre hilos, el compilador te detendrá inmediatamente:
> ```text
> error[E0277]: `Rc<Mutex<i32>>` cannot be sent between threads safely
>   --> src/main.rs:8:36
>   |
> 8 |         let handle = thread::spawn(move || {
>   |                      ^^^^^^^^^^^^^ `Rc<Mutex<i32>>` cannot be sent between threads safely
> ```
> **¿Por qué?** `Rc` no es seguro para hilos porque su conteo interno de referencias no usa operaciones atómicas de CPU, lo que rompería la memoria en entornos multihilo. Rust te obliga a usar `Arc` (*Atomic Rc*).

---

## 6. Ilustración Visual: Arc y Mutex Trabajando Juntos



![Diagrama 2](capitulos/20_concurrencia_sin_miedo_img_2.svg)



---

## Resumen del Capítulo
- Los hilos en Rust se lanzan con `thread::spawn`.
- La palabra clave `move` transfiere la propiedad de las variables del hilo principal al secundario.
- Los canales `mpsc` permiten enviar mensajes entre hilos de forma ordenada.
- La combinación de `Arc<T>` y `Mutex<T>` te permite compartir y modificar estado de manera segura sin carreras de datos.