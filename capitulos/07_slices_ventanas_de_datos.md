# Capítulo 7: Slices: Ventanas a Trozos de Memoria sin Copiar

> 🧠 **EN 10 SEGUNDOS (TDAH):** Un `slice` es una ventana de lectura que se asoma a una colección existente sin clonarla ni robar su propiedad. Es como mirar por la rendija de una puerta: ves lo que hay dentro, pero no te lo llevas a casa.

---

### El Problema de los Índices Desconectados

Imagínate que tienes una lista de tareas pendientes. Le pides a una función que te devuelva las primeras tres tareas usando índices numéricos (`0..3`). 

En lenguajes tradicionales, devuelves esos números y cruzas los dedos. ¿Qué pasa si el array original cambia, se reordena o se borra por completo? Los números ya no significan nada, o peor aún, apuntan a basura en memoria.

Rust previene esto mediante **slices**. Un slice no es solo un número: es una estructura ligera de dos palabras en la memoria Stack que guarda:
1. Un puntero al primer elemento del array u origen en el Heap.
2. La longitud exacta de la ventana.



![Diagrama 1](capitulos/07_slices_ventanas_de_datos_img_1.svg)



> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS, si haces `str.slice(0, 3)`, el motor crea un **nuevo string** duplicando caracteres en memoria. En TypeScript, los arrays devuelven sub-arreglos (`array.slice()`) que también son copias superficiales. En Rust, `&str` o `&[T]` **jamás copian datos**: prestan una referencia directa al bloque original.

---

### String Slices: `&str` vs `String`

Un `String` es una estructura propietaria que vive en el Heap, es dinámica y puede crecer. En cambio, un `&str` es un **slice de string**, una vista inmutable hacia UTF-8 válido.

```rust
fn main() {
    let saludo = String::from("Hola, Rustáceos");

    // Creamos slices usando rangos inclusivos/exclusivos
    let hola: &str = &saludo[0..4];
    let rust: &str = &saludo[6..10];

    println!("Ventana 1: {}", hola);
    println!("Ventana 2: {}", rust);
}
```

#### Regla de Oro de las Firmas de Funciones
Si escribes una función que acepta texto, **nunca pidas `&String`**. Pide siempre `&str`. ¿Por qué? Porque un `&str` acepta tanto literales de texto estáticos (`"hola"`) como referencias a `String` (`&mi_string`), dándole máxima flexibilidad a tu código.

```rust
fn imprimir_texto(texto: &str) {
    println!("Texto recibido: {}", texto);
}

fn main() {
    let s = String::from("Dinámico");
    let literal = "Estático";

    imprimir_texto(&s);        // Funciona perfectamente
    imprimir_texto(literal);   // También funciona perfectamente
}
```

---

### Slices de Arrays y Colecciones Genéricas

Los slices no son exclusivos de textos. Funcionan con cualquier tipo de colección lineal, como arrays estáticos o vectores (`Vec<T>`). La sintaxis universal para un slice de tipo genérico es `&[T]`.

```rust
fn procesar_numeros(lista: &[i32]) {
    println!("El primer número del slice es: {}", lista[0]);
    println!("La longitud de este slice es: {}", lista.len());
}

fn main() {
    // Array en el Stack
    let numeros_stack: [i32; 5] = [10, 20, 30, 40, 50];
    
    // Vector en el Heap
    let numeros_heap: Vec<i32> = vec![100, 200, 300];

    // Ambos se pueden pasar como slice gracias a la magia del coercion de Rust
    procesar_numeros(&numeros_stack[1..4]); // Pasa [20, 30, 40]
    procesar_numeros(&numeros_heap[..2]);     // Pasa [100, 200]
}
```



![Diagrama 2](capitulos/07_slices_ventanas_de_datos_img_2.svg)



---

### Prevención de Errores en Compilación

El sistema de ownership y lifetimes de Rust brilla con intensidad al trabajar con slices. El compilador actúa como un guardián implacable contra los punteros colgantes (*dangling pointers*).

> 🟥 **FRENAZO DEL COMPILADOR:**
> 
> Intenta compilar este código donde un slice intenta sobrevivir al objeto que lo creó:
> 
> ```rust
> fn devolver_slice() -> &str {
>     let s = String::from("Ayuda");
>     &s[..3] // ¡ERROR! Intentas retornar un slice de una variable local
> }
> ```
> 
> **El Compilador grita:**
> ```text
> error[E0515]: cannot return value referencing local variable `s`
>   --> src/main.rs:3:5
>   |
> 3 |     &s[..3]
>   |     - ^--`s` is borrowed here
>   |     |
>   |     returns a value referencing data owned by the current function
> ```
> **Por qué te salva la vida:** La variable `s` muere al finalizar la función `devolver_slice()`. Si Rust te dejara retornar ese `&str`, estarías apuntando a una dirección de memoria liberada, lo que en C o C++ provocaría fallos de seguridad críticos (Vulnerabilidades de tipo *Use-After-Free*). Rust lo bloquea antes de que escribas tu primer test.
