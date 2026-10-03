# Capítulo 25: Unsafe Rust: Rompiendo el Cristal de Emergencia

> 🧠 **EN 10 SEGUNDOS (TDAH):** `unsafe` no desactiva el compilador de Rust. Solo te otorga 5 superpoderes para saltarte temporalmente el chequeo de borrowing estático, permitiéndote interactuar con hardware, código C o construir estructuras de datos complejas bajo tu propia responsabilidad.

Rust es famoso por su seguridad estricta en tiempo de compilación. Sin embargo, el mundo real es complejo: necesitamos hablar con sistemas operativos, hardware de bajo nivel o bibliotecas escritas en C. 

Para eso existe `unsafe`. No significa "código mal hecho", significa: *"Compilador, confía en mí, yo me encargo de mantener las reglas lógicas"*.

---

## Los 5 Superpoderes de `unsafe`

La palabra clave `unsafe` por sí sola no hace nada. Desbloquea exactamente cinco capacidades que el código seguro tiene prohibidas:

1. Desreferenciar punteros crudos (*raw pointers*).
2. Llamar a funciones o métodos `unsafe` (incluyendo funciones C externas).
3. Implementar traits `unsafe`.
4. Mutar o leer variables estáticas mutables (`static mut`).
5. Acceder a campos de un `union`.

Veamos visualmente cómo el compilador actúa como guardia de seguridad, y cómo `unsafe` abre la puerta blindada bajo tu supervisión:



![Diagrama 1](capitulos/25_unsafe_rust_img_1.svg)



---

## Punteros Crudos (*const T, *mut T) vs Referencias Seguras (&T)

Las referencias seguras (`&T` y `&mut T`) siempre apuntan a datos válidos, no pueden ser nulas y respetan estrictamente las reglas de préstamo. 

Los punteros crudos (`*const T` y `*mut T`) son exactamente iguales a los punteros de C o C++:
* Pueden ser nulos (null).
* Pueden apuntar a memoria inválida o liberada.
* Ignoran por completo las reglas de mutabilidad compartida del compilador.

```rust
fn main() {
    let mut num = 5;

    // Crear punteros crudos es SEGURO (no requiere bloque unsafe)
    let r1 = &num as *const i32;
    let r2 = &mut num as *mut i32;

    // DESREFERENCIARlos requiere un bloque unsafe obligatoriamente
    unsafe {
        println!("r1 apunta a: {}", *r1);
        println!("r2 apunta a: {}", *r2);
        
        // Modificamos a través del puntero crudo mutable
        *r2 = 10;
        println!("num ahora es: {}", num);
    }
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS, *todo* es esencialmente un puntero crudo o una referencia mutable compartida bajo el capó. Mutas objetos globales o pasas referencias sin que el motor V8 te detenga. En Rust, jugar con memoria directa requiere declarar explícitamente el bloque `unsafe`.

---

## Modificar Variables Estáticas Mutables Globales

En Rust, el estado global mutable es peligroso porque múltiples hilos pueden acceder a él causando condiciones de carrera (*data races*). Por defecto está prohibido, pero `static mut` te deja hacerlo bajo tu propio riesgo:

```rust
static mut CONTADOR_GLOBAL: u32 = 0;

fn incrementar(val: u32) {
    // Modificar un static mut es unsafe porque no hay exclusión mutua automática
    unsafe {
        CONTADOR_GLOBAL += val;
    }
}

fn main() {
    incrementar(5);
    unsafe {
        println!("Contador global: {}", CONTADOR_GLOBAL);
    }
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> ```text
> error[E0133]: use of mutable static is unsafe and requires unsafe block
>  --> src/main.rs:5:5
>   |
> 5 |     CONTADOR_GLOBAL += val;
>   |     ^^^^^^^^^^^^^^^^^^^^^^ use of mutable static
>   |
>   = note: mutable statics can be mutated by multiple threads: race conditions
> ```
> **Por qué ocurre:** Rust te obliga a poner el bloque `unsafe` para recordarte que si dos hilos tocan `CONTADOR_GLOBAL` al mismo tiempo, tu programa tendrá comportamiento indefinido (*Undefined Behavior*).

---

## Llamando a Código C Externo (FFI)

Uno de los usos más legítimos de `unsafe` es interactuar con bibliotecas escritas en C utilizando la Interfaz de Idioma Foráneo (FFI).

```rust
// Declaramos una función externa escrita en C (por ejemplo, la función abs de la libc)
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    // Llamar a código externo siempre se considera unsafe porque Rust no puede
    // garantizar qué hará ese código C por debajo.
    let resultado = unsafe {
        abs(-42)
    };
    
    println!("El valor absoluto de -42 es: {}", resultado);
}
```

---

## La Regla de Oro: Encapsular lo Inseguro

Nunca debes propagar `unsafe` por todo tu código de aplicación. La regla de oro en Rust es: **Usa `unsafe` en las tripas de una estructura, pero expón una API totalmente segura al exterior.**

Imagina construir tu propio vector o puntero inteligente. Por dentro usas punteros crudos y memoria manual, pero por fuera el usuario usa código 100% seguro:



![Diagrama 2](capitulos/25_unsafe_rust_img_2.svg)



Al encapsular el peligro, garantizas que los errores de memoria queden confinados en un espacio muy pequeño, facilitando las auditorías de seguridad de tu software.