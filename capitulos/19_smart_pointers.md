# Capítulo 19: Punteros Inteligentes: Box, Rc y RefCell

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los punteros inteligentes en Rust son structs que manejan datos en la memoria y añaden superpoderes (como saber cuándo borrar los datos automáticamente o permitir múltiples dueños). Olvídate de hacer `free` o `delete` manual.

En Rust, las reglas de propiedad y el *Borrow Checker* son muy estrictas. Por defecto, cada valor tiene un único dueño y los datos viven en el *Stack* (Pila). 

Pero la vida real es compleja: a veces necesitas datos gigantescos, estructuras recursivas, o que varias partes de tu programa posean el mismo dato. Aquí es donde entran los **Punteros Inteligentes** (*Smart Pointers*).

---

## 1. Box&lt;T&gt;: Tu boleto al Heap

Un `Box<T>` te permite almacenar datos en el *Heap* (Montículo) en lugar del *Stack*. ¿Por qué harías esto?

1. Cuando tienes un tipo cuyo tamaño no se conoce en tiempo de compilación (como una estructura recursiva, por ejemplo, un nodo de árbol o lista enlazada).
2. Cuando quieres transferir la propiedad de una cantidad masiva de datos sin copiar los datos reales, solo moviendo su dirección de memoria (el puntero).

```rust
// Una estructura recursiva necesita un Box, de lo contrario
// el compilador no sabría cuánto espacio reservar en el Stack.
#[allow(dead_code)]
enum Lista {
    Nodo(i32, Box<Lista>),
    Vacio,
}

fn main() {
    // Creamos una lista en el Heap usando Box
    let mi_lista = Lista::Nodo(
        1, 
        Box::new(Lista::Nodo(2, Box::new(Lista::Vacio)))
    );
    
    println!("Lista creada exitosamente en el Heap.");
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS, **todos** los objetos y arrays viven automáticamente en el *Heap* y el recolector de basura (*Garbage Collector*) se encarga de ellos. `Box<T>` en Rust es como crear un objeto, pero con una diferencia clave: Rust sabe exactamente en qué línea de código morirá y liberará la memoria de inmediato, sin pausas de recolección.

---

## 2. Visualizando Box&lt;T&gt;: Stack vs Heap



![Diagrama 1](capitulos/19_smart_pointers_img_1.svg)



---

## 3. Rc&lt;T&gt;: Propiedad Múltiple en un Solo Hilo

Normalmente, Rust te prohíbe tener más de un dueño para el mismo valor. ¿Qué pasa si construyes un grafo donde varios nodos apuntan al mismo hijo? 

`Rc<T>` significa **Reference Counted** (Conteo de Referencias). Mantiene un contador de cuántos propietarios tiene el dato. Cada vez que clonas el `Rc`, el contador sube en 1. Cuando un dueño sale de ámbito, el contador baja. Cuando llega a cero, el dato se destruye automáticamente.

> ⚠️ **Aviso importante:** `Rc<T>` **no es seguro para hilos** (*not thread-safe*). Si necesitas compartir datos entre múltiples hilos de CPU, usarás `Arc<T>` (Atomic Reference Counted).

```rust
use std::rc::Rc;

fn main() {
    // Creamos un dato compartido dentro de un Rc
    let sol = Rc::new(String::from("Sol de verano"));
    
    // Clonar el Rc NO clona el String, solo incrementa el contador de referencias
    let planetoide_1 = Rc::clone(&sol);
    let planetoide_2 = Rc::clone(&sol);

    println!("Referencias activas: {}", Rc::strong_count(&sol)); // Muestra 3
    
    // Al salir de main, planetoide_2, planetoide_1 y sol se destruyen.
    // El string se libera cuando el contador llega a 0.
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Si intentas enviar un `Rc<T>` a otro hilo usando `std::thread::spawn`, Rust te arrojará un error masivo diciendo que `Rc` no implementa el trait `Send`. El compilador te protege de corrupciones de memoria concurrentes. Usa `Arc<T>` para multihilo.

---

## 4. RefCell&lt;T&gt; y Mutabilidad Interior

Las reglas de Rust dicen: *puedes tener múltiples referencias inmutables (`&T`) O una sola referencia mutable (`&mut T`), pero nunca ambas a la vez.* Esto se valida en **tiempo de compilación**.

Pero a veces tu lógica necesita ser mutable por fuera, aunque parezca inmutable por dentro. Aquí entra `RefCell<T>`.

`RefCell<T>` traslada la comprobación de reglas de préstamo del **tiempo de compilación** al **tiempo de ejecución** (*runtime*). Si rompes las reglas, tu programa entrará en pánico (*panic*) y se cerrará en lugar de compilar mal.

### El patrón definitivo: `Rc<RefCell<T>>`
Combinar ambos punteros inteligentes es una técnica muy común en Rust para crear estructuras de datos complejas (como grafos o árboles con referencias cruzadas):

```rust
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    // Un dato compartido (Rc) que además permite mutabilidad interior (RefCell)
    let configuracion = Rc::new(RefCell::new(42));

    // Dos dueños diferentes pueden modificar el mismo valor subyacente
    let ref_cliente_a = Rc::clone(&configuracion);
    let ref_cliente_b = Rc::clone(&configuracion);

    // Mutamos a través del cliente A
    *ref_cliente_a.borrow_mut() = 100;

    // Leemos a través del cliente B
    println!("Nueva configuración vista por B: {}", *ref_cliente_b.borrow());
}
```

---

## Resumen del Arsenal de Punteros

| Puntero Inteligente | ¿Dónde vive? | ¿Cuántos dueños? | ¿Cuándo se valida? | Caso de uso típico |
| :--- | :--- | :--- | :--- | :--- |
| **`Box<T>`** | Heap | 1 solo | Compilación | Datos recursivos o grandes |
| **`Rc<T>`** | Heap | Múltiples (Un hilo) | Compilación | Grafos, árboles, compartir lectura |
| **`RefCell<T>`** | Stack / Heap | 1 (con mutabilidad interior) | **Ejecución** | Patrones de diseño flexibles / Mocking |