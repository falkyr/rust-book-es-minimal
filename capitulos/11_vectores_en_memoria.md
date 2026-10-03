# Capítulo 11: Colecciones I: Vectores Vec&lt;T&gt; (Los Arrays Dinámicos)

> 🧠 **EN 10 SEGUNDOS (TDAH):** Un `Vec<T>` es una lista de elementos que puede crecer, encogerse y cambiar en tiempo de ejecución. A diferencia de un array fijo, vive en el Heap, por lo que Rust gestiona su memoria automáticamente sin que tengas que liberarla a mano.

---

### El Problema del Espacio: Arrays Fijos vs Vectores

Imagina que organizas una fiesta. Un array clásico en Rust (`[i32; 3]`) es como reservar una mesa exacta para tres personas. Si llega un cuarto invitado, la mesa colapsa. No puedes cambiar su tamaño.

El vector (`Vec<T>`) es un organizador profesional: empieza con un espacio inicial, y si la fiesta crece, busca un local más grande, muda a todos los invitados de golpe y destruye el local viejo.



![Diagrama 1](capitulos/11_vectores_en_memoria_img_1.svg)



---

### Crear, Añadir y Leer Elementos

Para crear un vector vacío o con valores iniciales, usamos la macro `vec!` o la función asociada `Vec::new()`.

```rust
fn main() {
    // Forma rápida con macro (inferencia de tipos automática)
    let mut numeros: Vec<i32> = vec![1, 2, 3];

    // Añadir un elemento al final con push
    numeros.push(4);
    numeros.push(5);

    // Leer el primer elemento usando indexación directa
    let primero = numeros[0]; 
    println!("El primer número es: {}", primero);
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS, un array (`let arr = [1, 2, 3]`) puede mezclar tipos libremente y crece con `.push()`. En Rust, el vector `Vec<T>` es estrictamente homogéneo: **todos** sus elementos deben ser exactamente del mismo tipo `T`.

---

### Acceso Seguro: Indexación Directa `[]` vs `.get()`

La indexación directa (`numeros[indice]`) es rápida, pero tiene un peligro mortal si te equivocas de número: **hace que tu programa falle (panic)** y se cierre abruptamente.

El método `.get(indice)` devuelve un `Option<&T>`, obligándote a manejar el caso de que la posición no exista.

```rust
fn main() {
    let vector = vec![10, 20, 30];

    // PELIGROSO: Si pides el índice 99, el programa explota aquí.
    // let elemento_malo = vector[99]; 

    // SEGURO: Usando .get() manejamos el error con gracia
    match vector.get(99) {
        Some(valor) => println!("Encontrado: {}", valor),
        None => println!("¡Ups! Esa posición no existe en el vector."),
    }
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> ```text
> error[E0502]: cannot borrow `vector` as mutable because it is also borrowed as immutable
>   --> src/main.rs:5:5
>    |
> 4  |     let elemento = &vector[0];
>    |                     ------ immutable borrow occurs here
> 5  |     vector.push(4);
>    |     ^^^^^^^^^^^^^^ mutable borrow occurs here
> ```
> **Por qué ocurre:** Rust te protege de un bug clásico de C++. Si guardas una referencia a un elemento y luego haces `.push()`, el vector podría mudarse a otra dirección de memoria en el Heap, dejando tu referencia apuntando a la basura. Rust lo detecta en tiempo de compilación y lo prohíbe.

---

### Iteración Mutable e Inmutable

Puedes recorrer los elementos de un vector para leerlos o para modificarlos sobre la marcha.

```rust
fn main() {
    let mut puntuaciones = vec![50, 70, 90];

    // 1. Iteración mutable (&mut) para modificar valores
    for puntaje in &mut puntuaciones {
        *puntaje += 10; // Usamos el operador de desreferencia (*) para cambiar el valor al que apunta
    }

    // 2. Iteración inmutable (&) para solo leer
    for puntaje in &puntuaciones {
        println!("Puntuación actualizada: {}", puntaje);
    }
}
```



![Diagrama 2](capitulos/11_vectores_en_memoria_img_2.svg)



---

### Guardar Varios Tipos con Enums

¿Qué pasa si necesitas un vector que guarde texto, números y booleanos mezclados, como harías en un array de JavaScript? Como el `Vec<T>` exige un solo tipo `T`, usamos un `enum` para empaquetar diferentes variantes bajo un mismo tipo de dato.

```rust
#[derive(Debug)]
enum ElementoCelda {
    Texto(String),
    Numero(i32),
    Booleano(bool),
}

fn main() {
    // Creamos un vector homogéneo cuyo tipo es 'ElementoCelda'
    let hoja_excel: Vec<ElementoCelda> = vec![
        ElementoCelda::Texto(String::from("Edad")),
        ElementoCelda::Numero(30),
        ElementoCelda::Booleano(true),
    ];

    for celda in &hoja_excel {
        match celda {
            ElementoCelda::Texto(t) => println!("Celda de texto: {}", t),
            ElementoCelda::Numero(n) => println!("Celda numérica: {}", n),
            ElementoCelda::Booleano(b) => println!("Celda booleana: {}", b),
        }
    }
}
```

¡Listo! Ya dominas la estructura de datos más utilizada en Rust. En el siguiente capítulo veremos cómo manejar texto real en formato UTF-8 con `String`.