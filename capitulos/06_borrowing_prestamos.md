# Capítulo 6: Borrowing: El Arte de Prestar sin Perder la Propiedad

> 🧠 **EN 10 SEGUNDOS (TDAH):** Prestar (*borrow*) significa permitir que otra función o variable use tus datos sin robarte la propiedad. Usas `&` para leer y `&mut` para modificar. Al terminar su turno, el permiso se devuelve automáticamente.

---

Imagina que tienes un libro de cómics favorito. Quieres que tu amigo lo lea, pero no quieres regalárselo para siempre. Lo que haces es **prestárselo** un rato. Tu amigo lo lee, te lo devuelve, y tú sigues siendo el dueño legítimo. 

En Rust, esto se llama **Borrowing** (Préstamo). En lugar de transferir la propiedad (*Move*) cada vez que pasamos una variable, creamos una **referencia** apuntando a los datos originales.



![Diagrama 1](capitulos/06_borrowing_prestamos_img_1.svg)



---

## 1. Referencias Inmutables (`&T`): El Club de Lectura

Cuando antepones un `&` a un tipo, creas una **referencia inmutable**. Esto significa que puedes **leer** los datos, pero **no puedes cambiarlos**.

```rust
fn main() {
    let titulo = String::from("Rust sin Dolor");

    // Pasamos una referencia inmutable con &titulo
    imprimir_titulo(&titulo);

    // ¡La variable 'titulo' sigue viva y usable aquí!
    println!("Aun tengo mi titulo: {}", titulo);
}

fn imrimir_titulo(s: &String) {
    // s es una referencia inmutable
    println!("Leyendo: {}", s);
} // s sale de ámbito, pero el dueño original no pierde nada
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS, **todos** los objetos y arrays se pasan por referencia de forma predeterminada y mutable. Cualquiera puede modificar el objeto original por debajo, causando bugs fantásticos (y terroríficos). Rust te obliga a declarar explícitamente cuándo cedes acceso y si ese acceso permite alterar el valor.

---

## 2. Referencias Mutables (`&mut T`): El Escritor Solitario

¿Qué pasa si quieres que una función modifique tus datos sin adueñarse de ellos? Usas una **referencia mutable** (`&mut`).

```rust
fn main() {
    let mut puntaje = 10; // Debe ser mut para permitir préstamos mutables

    agregar_bonus(&mut puntaje); // Prestamos con permiso de escritura

    println!("Nuevo puntaje: {}", puntaje); // Imprime 20
}

fn agregar_bonus(p: &mut i32) {
    *p += 10; // Desreferenciamos con * para modificar el valor original
}
```

Para cambiar el valor dentro de la función, usamos el operador de desreferencia `*p`. Esto le dice a Rust: *"Ve al lugar de memoria al que apunta esta referencia y cambia el valor guardado allí"*.

---

## 3. La Ley Sagrada de Rust: Lectores vs. Escritores

Aquí es donde el compilador se pone estricto y te salva la vida. La regla de oro del sistema de tipos de Rust es:

> **Puedes tener CUALQUIER cantidad de referencias inmutables (`&T`) a la vez, o una ÚNICA referencia mutable (`&mut T`). NUNCA ambas al mismo tiempo.**

Imagina que estás escribiendo en un diario personal (`&mut`) y cinco amigos están leyendo el mismo diario por encima de tu hombro (`&`). Es un caos absoluto: lo que leen cambia mientras lo miran. Rust prohíbe esta inestabilidad en tiempo de compilación.



![Diagrama 2](capitulos/06_borrowing_prestamos_img_2.svg)



---

> 🟥 **FRENAZO DEL COMPILADOR:**
> Intenta hacer esto en tu código:
> ```rust
> let mut texto = String::from("Hola");
> let r1 = &texto; // Primer préstamo (inmutable)
> let r2 = &mut texto; // Segundo préstamo (mutable)
> println!("{} y {}", r1, r2);
> ```
> **El compilador gritará:**
> *cannot borrow `texto` as mutable because it is also borrowed as immutable*. 
> **Qué bug evitó:** Evitó que `r1` intente leer un texto cuya memoria subyacente podría haber sido redimensionada y movida en el Heap por `r2`, previniendo un cuelgue catastrófico o una lectura de basura en memoria.
