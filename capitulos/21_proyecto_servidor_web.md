# Capítulo 21: Proyecto Maestro: Servidor Web Concurrente

> 🧠 **EN 10 SEGUNDOS (TDAH):** Construiremos un servidor web multihilo desde cero. Usaremos un `TcpListener` para escuchar conexiones, peticiones HTTP básicas y un `ThreadPool` personalizado para manejar múltiples usuarios en paralelo sin fundir la CPU.

---

El momento de la verdad ha llegado. Vamos a juntar todo lo que has aprendido sobre ownership, concurrencia, canales (`channels`) y closures para construir un servidor web funcional de alto rendimiento.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En Node.js, creas un servidor HTTP con `http.createServer()` que maneja eventos de forma asíncrona en un solo hilo (event loop). En Rust, el enfoque por defecto es multihilo real: cada petición o lote de peticiones se reparte de forma segura entre varios hilos de CPU usando memoria totalmente controlada.

---

## 1. El Ciclo de Vida del Servidor y el `TcpListener`

Un servidor web es básicamente un bucle infinito que abre los oídos en un puerto de red, espera a que alguien toque la puerta, lee el mensaje HTTP y devuelve una respuesta.

```rust
use std::net::TcpListener;
use std::io::{Read, Write};

fn main() -> std::io::Result<()> {
    // Abrimos el puerto 7878 en localhost
    let listener = TcpListener::bind("127.0.0.1:7878")?;
    println!("Servidor activo en http://127.0.0.1:7878");

    for stream in listener.incoming() {
        let mut stream = stream?;
        handle_connection(&mut stream)?;
    }

    Ok(())
}

fn handle_connection(stream: &mut std::net::TcpStream) -> std::io::Result<()> {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer)?;

    // Respuesta HTTP básica en texto plano
    let response = "HTTP/1.1 200 OK\r\n\r\n¡Hola desde Rust sin Dolor!";
    stream.write_all(response.as_bytes())?;
    stream.flush()
}
```

Este código funciona, pero tiene un problema grave: es **secuencial**. Si un cliente se conecta y tarda 10 segundos en recibir la respuesta, el siguiente cliente se queda esperando congelado. Necesitamos un `ThreadPool`.

---

## 2. Diagrama del ThreadPool y Canales

Para evitar crear un hilo nuevo por cada petición (lo cual satura el sistema operativo), creamos un grupo fijo de hilos trabajadores (*workers*) que toman tareas de una cola compartida.



![Diagrama 1](capitulos/21_proyecto_servidor_web_img_1.svg)



---

## 3. Construyendo el `ThreadPool`

Vamos a empaquetar la lógica concurrente en una estructura limpia y reutilizable.

```rust
use std::thread;
use std::sync::{mpsc, Arc, Mutex};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    /// Crea un nuevo ThreadPool con un número determinado de hilos.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    /// Envía una tarea al pool para que la ejecute un hilo disponible.
    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.send(job).unwrap();
    }
}

struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || loop {
            let job = receiver.lock().unwrap().recv();

            match job {
                Ok(job) => {
                    println!("Worker {id} ejecutando la tarea.");
                    job();
                }
                Err(_) => {
                    println!("Worker {id} desconectado; apagando.");
                    break;
                }
            }
        });

        Worker { id, thread }
    }
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Al pasar el `receiver` compartido entre múltiples hilos, intentarás meterlo directamente en el bucle y el compilador te dirá que `Receiver` no implementa `Clone`. La solución es envolverlo en `Arc<Mutex<...>>` para permitir propiedad compartida segura entre hilos con exclusión mutua.

---

## 4. Ensamblando el Servidor Final en `main.rs`

Ahora unimos nuestro `ThreadPool` con el `TcpListener` para atender peticiones reales de forma concurrente y eficiente.

```rust
use std::net::TcpListener;
use std::io::{Read, Write};
use std::thread;
use std::time::Duration;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4); // Creamos un pool de 4 hilos

    for stream in listener.incoming() {
        let mut stream = stream.unwrap();

        pool.execute(move || {
            handle_connection(&mut stream);
        });
    }
}

fn handle_connection(stream: &mut std::net::TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";
    let sleep = b"GET /sleep HTTP/1.1\r\n";

    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK\r\n\r\n", "index.html")
    } else if buffer.starts_with(sleep) {
        thread::sleep(Duration::from_secs(5)); // Simulamos carga pesada
        ("HTTP/1.1 200 OK\r\n\r\n", "index.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND\r\n\r\n", "404.html")
    };

    let contents = format!("Servidor Rust respondiendo con éxito a petición: {filename}");
    let response = format!("{status_line}{contents}");
    
    stream.write_all(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}
```

¡Felicidades! Has construido un servidor web concurrente, robusto y ultrarrápido en Rust, aplicando gestión de memoria estricta, hilos seguros y sincronización sin condiciones de carrera.