# Capítulo 26: Macros Declarativas: Código que Escribe Código

> 🧠 **EN 10 SEGUNDOS (TDAH):** Las funciones ejecutan código en tiempo de ejecución. Las macros declarativas son robots que leen tu código y **escriben más código** antes de que el programa siquiera compile.

---

## 1. La Diferencia Fundamental: ¿Función o Macro?

Para entender las macros, imagina que estás en una pizzería:

*   **Una Función:** Es un pizzero trabajando en la cocina. Le pasas ingredientes (argumentos) y te devuelve una pizza (un resultado) cuando se lo pides.
*   **Una Macro:** Es una fábrica automática de pizzerias. Le das un plano rápido y la fábrica construye una cocina entera antes de abrir el restaurante.

En Rust, las funciones operan con **datos**. Las macros operan con la **sintaxis misma del lenguaje** (el código fuente).



![Diagrama 1](capitulos/26_macros_avanzadas_img_1.svg)



---

## 2. Metaprogramación: Rust vs. TypeScript/JavaScript

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TS/JS, si quieres generar código dinámicamente o evitar repetir lógica compleja, usas `eval()`, funciones de orden superior, o decoradores experimentales. Pero `eval()` es peligroso, lento y un infierno para el tipado estricto. Las macros en Rust ocurren en el **servidor de compilación**, son totalmente seguras contra inyecciones y devienen en código nativo ultrarrápido sin penalización en runtime.

---

## 3. Anatomía de `macro_rules!` y Pattern Matching

Las macros declarativas en Rust se construyen usando `macro_rules!`. Funcionan como un sistema de `match` pero aplicado a **estructuras sintácticas** (tokens), no a valores numéricos o de texto.

Construyamos paso a paso una macro llamada `habla!` que imprima un mensaje dependiendo de si le pasamos un perro o un gato.

```rust
macro_rules! habla {
    // 1. Patrón para cuando recibe "perro"
    (perro) => {
        println!("¡Guau guau!");
    };
    
    // 2. Patrón para cuando recibe "gato"
    (gato) => {
        println!("¡Miau!");
    };
}

fn main() {
    habla!(perro); // Imprime: ¡Guau guau!
    habla!(gato);  // Imprime: ¡Miau!
}
```

### ¿Qué significan los símbolos raros ($)?

En las macros verás símbolos como `$x:expr`. Esto se llama un **fragment specifier** (capturador):
*   `$` indica una variable de macro.
*   `x` es el nombre que le das a esa parte del código capturado.
*   `:expr` le dice a Rust qué tipo de estructura sintáctica debe coincidir (en este caso, una **expresión**).

Otros fragmentos comunes son `:ident` (para nombres de variables o funciones) y `:block` (para bloques de código `{}`).

---

## 4. Creación Práctica: Una Macro de Vectores Seguros

Imagina que estás harto de escribir `vec![1, 2, 3]` y quieres una macro propia que cree vectores multiplicando cada elemento por 2 automáticamente.



![Diagrama 2](capitulos/26_macros_avanzadas_img_2.svg)



Aquí tienes el código completo usando repeticiones (`$()*`):

```rust
macro_rules! duplica_vec {
    // El asterisco (*) significa "se puede repetir cero o más veces" separado por comas
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x * 2);
            )*
            temp_vec
        }
    };
}

fn main3() {
    let mi_vector = duplica_vec![10, 20, 30];
    println!("{:?}", mi_vector); // Imprime: [20, 40, 60]
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si intentas usar tu macro pasando un token incorrecto, por ejemplo olvidando la coma o pasando un bloque donde esperaba una expresión, el compilador te mostrará un error críptico señalando la expansión:
> ```text
> error: no rules expected the token `+`
>   --> src/main.rs:15:20
>    |
> 15 |     duplica_vec![1 + ];
>    |                    ^
> ```
> **Por qué ocurre:** Las macros comparan la sintaxis literal contra patrones predefinidos. Si escribes código incompleto, el patrón no hace `match` y el compilador grita. **Consejo Pro:** Usa `cargo rustc -- -Z unstable-options --pretty=expanded` para ver exactamente en qué se convierte tu macro.