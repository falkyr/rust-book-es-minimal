# Capítulo 3: Funciones, Sentencias y el Misterio del Punto y Coma

> 🧠 **EN 10 SEGUNDOS (TDAH):** En Rust, **quitar el punto y coma (`;`) al final de una línea significa "devuelve este valor automáticamente"**. Las sentencias hacen cosas; las expresiones producen valores.

---

Las funciones son los bloques de construcción fundamentales en Rust. Ya conoces `fn main()`, el punto de entrada de todo programa. Hoy vamos a desmitificar cómo devuelven datos y por qué un simple signo de puntuación cambia por completo el flujo de tu código.

## 1. Anatomía de una Función en Rust

Declarar una función es sencillo, pero exige precisión. Rust es un lenguaje fuertemente tipado: **debes** declarar el tipo de cada parámetro y el tipo de dato que la función va a retornar.

```rust
fn sumar(a: i32, b: i32) -> i32 {
    a + b // ¡Sin punto y coma! Esto es una expresión de retorno.
}

fn main() {
    let resultado = sumar(5, 10);
    println!("El resultado es: {}", resultado);
}
```

- `fn`: La palabra reservada para iniciar una función.
- `a: i32`: El parámetro `a` de tipo entero de 32 bits.
- `-> i32`: Indica que esta función devolverá un valor de tipo `i32`.

---

## 2. Sentencias (Statements) vs Expresiones (Expressions)

Esta es la trampa mental número uno para los desarrolladores que vienen de otros lenguajes. En Rust, casi todo es una **expresión**.

*   **Sentencia (Statement):** Una instrucción que realiza una acción y **no** devuelve un valor. Terminan con punto y coma (`;`). Ejemplo: `let x = 6;`
*   **Expresión (Expression):** Evalúa algo y **produce un valor**. Ejemplo: `5 + 6`, una llamada a función, o incluso un bloque de código `{ let x = 3; x + 1 }`.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:**
> En TypeScript/JavaScript moderno, estás acostumbrado a las arrow functions con retorno implícito:
> `const sumar = (a: number, b: number) => a + b;`
> En Rust, haces exactamente lo mismo, pero **omitiendo la flecha gorda (`=>`) y prohibiendo el punto y coma final**. Si le pones `;` al final en Rust, conviertes la expresión en una sentencia que devuelve `()`, el tipo vacío (*Unit*).

---

## 3. Visualizando el Poder del Punto y Coma

Mira este diagrama vectorial que explica visualmente qué pasa con y sin el punto y coma en el cuerpo de una función.



![Diagrama 1](capitulos/03_funciones_y_expresiones_img_1.svg)



---

## 4. El Gran Error de Principiante

Es muy común que, por fuerza de costumbre muscular, pongas un punto y coma al final de la última línea de una función. Cuando lo haces, el compilador de Rust se pone firme.

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si escribes esto:
> ```rust
> fn obtener_edad() -> u8 {
>     25; 
> }
> ```
> El compilador arrojará este error:
> ```text
> error[E0308]: mismatched types
>  --> src/main.rs:1:25
>   |
> 1 | fn obtener_edad() -> u8 {
>   |    ------------      ^^ expected `u8`, found `()`
> 2 |     25;
>   |       - help: remove this semicolon
> ```
> **Qué bug evitó:** Rust te protege de retornar silenciosamente datos vacíos o nulos cuando prometiste entregar un tipo de dato concreto. La ayuda del compilador (*help: remove this semicolon*) te muestra exactamente qué hacer.

---

## Resumen del Capítulo

1. Las funciones requieren tipos explícitos en sus parámetros y en su retorno (`-> T`).
2. Una **expresión** devuelve un valor; una **sentencia** ejecuta una acción y termina en `;`.
3. Para devolver un valor de forma implícita en Rust, **omite el punto y coma** en la última línea del bloque de código.