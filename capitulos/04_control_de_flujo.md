# Capítulo 4: Tomando Decisiones: If Expresión y Bucles

> 🧠 **EN 10 SEGUNDOS (TDAH):** En Rust, los `if` y los bucles `loop` devuelven valores directamente. Puedes asignar un `if` a una variable sin necesidad de operadores ternarios raros.

---

## 1. El `if` no es una sentencia, ¡es una Expresión!

En otros lenguajes, un `if` solo ejecuta código. En Rust, como todo es una expresión, un `if` **devuelve un valor**. 

Imagina que quieres asignar una puntuación según una condición. Olvídate del operador ternario `condicion ? a : b`. En Rust, haces esto:

```rust
fn main() {
    let tengo_hambre = true;

    // El if entero se evalúa y su resultado se guarda en 'comida'
    let comida = if tengo_hambre {
        "Pizza" // Sin punto y coma (es la expresión de retorno)
    } else {
        "Agua"  // Sin punto y coma
    };

    println!("Voy a consumir: {}", comida);
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS usas el operador ternario: `const comida = tengoHambre ? "Pizza" : "Agua";`. En Rust, el bloque `if/else` nativo hace exactamente eso, pero con la legibilidad de múltiples líneas si lo necesitas.

### Diagrama: El `if` como Expresión



![Diagrama 1](capitulos/04_control_de_flujo_img_1.svg)



> 🟥 **FRENAZO DEL COMPILADOR:** 
> Si pones un punto y coma al final de las ramas, el compilador fallará:
> ```rust
> let x = if true { 5; } else { 10; }; // Error: tipo de retorno es '()' (vacío)
> ```
> *Por qué:* El punto y coma convierte la expresión en una sentencia que descarta el valor. Recuerda: **sin punto y coma** en la última línea si quieres devolver el valor.

---

## 2. Bucles: El infinito controlado (`loop`)

Rust tiene tres tipos de bucles: `loop`, `while` y `for`. El rey de la flexibilidad es `loop`, porque crea un bucle infinito del que puedes **extraer un valor** al salir con `break`.

```rust
fn main() {
    let mut contador = 0;

    // El bucle loop puede retornar un valor usando break
    let resultado = loop {
        contador += 1;

        if contador == 10 {
            break contador * 2; // Rompe el bucle y devuelve 20
        }
    };

    println!("El resultado del bucle es: {}", resultado); // Imprime 20
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS harías malabares con variables externas modificadas dentro de un `while(true)` o usarías patrones complejos de promesas. En Rust, `loop` con `break valor;` es una construcción nativa limpia y súper rápida.

---

## 3. Navegando con `while` y `for`

### El clásico `while`
Funciona exactamente igual que en otros lenguajes: se ejecuta mientras la condición sea verdadera.

```rust
fn main() {
    let mut energia = 3;

    while energia > 0 {
        println!("Energía restante: {}", energia);
        energia -= 1;
    }

    println!("¡Batería agotada!");
}
```

### El poderoso `for` (Adiós a los bugs de índices)
En Rust, el bucle `for` es seguro y elegante. No necesitas controlar índices manuales `i = 0; i < len; i++`. Iteras directamente sobre rangos o colecciones.

```rust
fn main() {
    // Iterar en un rango exclusivo (del 1 al 4)
    println!("--- Rango exclusivo ---");
    for numero in 1..5 {
        println!("Número: {}", numero);
    }

    // Iterar sobre un vector (colección)
    let lenguajes = vec!["Rust", "TypeScript", "Python"];

    println!("--- Colección ---");
    for lang in lenguajes {
        println!("Me gusta {}", lang);
    }
}
```

---

## Resumen del Capítulo

1. **`if` es expresión:** Devuelve valores directamente y se puede asignar a variables.
2. **Cuidado con los `;`:** No pongas punto y coma en la última línea de las ramas del `if` si quieres retornar un valor.
3. **`loop` con retorno:** Permite salir de bucles infinitos devolviendo datos mediante `break expresion;`.
4. **`for` seguro:** Prefiere `for` sobre `while` para recorrer rangos y colecciones; evita errores fuera de límites de forma nativa.