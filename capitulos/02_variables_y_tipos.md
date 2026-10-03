# Capítulo 2: Variables, Mutabilidad y Tipos con Peso Real

> 🧠 **EN 10 SEGUNDOS (TDAH):** En Rust, las variables son **inmutables por defecto** para evitar accidentes. Si quieres cambiar su valor, debes usar la palabra clave `mut`. Los tipos son estrictos y no hay conversiones mágicas.

---

## 1. Inmutabilidad por Defecto (`let` vs `mut`)

Cuando declaras una variable con `let` en Rust, su valor se graba en piedra. El compilador asume que no cambiará jamás. Si intentas modificarla más adelante, el compilador se detendrá y te lanzará un error.

Para permitir que una variable cambie, debes usar `let mut`.

```rust
fn main() {
    let puntuacion = 10; // Inmutable por defecto
    // puntuacion = 20;  // <-- Esto daría error de compilación

    let mut vidas = 3;   // Mutable (puede cambiar)
    println!("Vidas iniciales: {}", vidas);

    vidas = 2;           // Permitido porque usamos 'mut'
    println!("Vidas actualizadas: {}", vidas);
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS tienes `const` (que es inmutable en su referencia, pero sus propiedades internas pueden cambiar) y `let`. En Rust, `let` es verdaderamente inmutable a nivel de valor. Para cambiar el valor, necesitas obligatoriamente declarar `let mut`.



![Diagrama 1](capitulos/02_variables_y_tipos_img_1.svg)



> 🟥 **FRENAZO DEL COMPILADOR:**
> ```text
> error[E0384]: cannot assign twice to immutable variable `puntuacion`
>   --> src/main.rs:3:5
>   |
> 2 |     let puntuacion = 10;
>   |        ----------
>   |        |
>   |        first assignment to `puntuacion`
>   |        help: consider introducing a mutable variable: `let mut puntuacion`
> ```
> *El compilador leyó tu código, vio que intentaste cambiar un valor inmutable y te ofreció la solución exacta antes de que ejecutes el programa.*

---

## 2. Shadowing (El arte de reutilizar nombres)

El *Shadowing* (sombra) no es lo mismo que cambiar el valor de una variable con `mut`. Consiste en declarar una **nueva** variable que reutiliza el nombre de una anterior usando la palabra clave `let` otra vez.

Esto te permite cambiar el tipo de dato o transformar el valor manteniendo el mismo identificador.

```rust
fn main() {
    let espacios = "   "; // Tipo String (&str)
    let espacios = espacios.len(); // Nuevo tipo: i32/usize (longitud)
    
    println!("Cantidad de espacios: {}", espacios);
}
```

Gracias al shadowing, la variable `espacios` pasa de ser un texto a ser un número entero en la siguiente línea, algo imposible si usaras `let mut`.

---

## 3. Tipos con Peso Real: Primitivos Numéricos y Booleans

En Rust, cada tipo de dato tiene un tamaño exacto en la memoria. No hay ambigüedades.

### Enteros (Signed vs Unsigned)
* **Con signo (`i`):** Pueden ser positivos y negativos (`i8`, `i16`, `i32`, `i64`, `i128`, `isize`).
* **Sin signo (`u`):** Solo números positivos, duplicando su rango positivo (`u8`, `u16`, `u32`, `u64`, `u128`, `usize`).

*Por defecto, si escribes un número entero suelto (ej: `42`), Rust le asignará el tipo `i32`.*

### Floats (Decimales)
* `f32` (Puntero flotante de 32 bits)
* `f64` (Puntero flotante de 64 bits - **Por defecto** por ser más preciso en CPUs modernas).

### Booleans
* `bool` (Ocupa exactamente 1 byte y solo acepta `true` o `false`).

---

## 4. Caracteres (`char`) vs Strings (`&str` y `String`)

Esta es una de las diferencias más importantes en Rust respecto a otros lenguajes.

* **`char` (Caracter):** Representa un único carácter Unicode. Se escribe con **comillas simples** (`'a'`, `'ñ'`, `'🚀'`). Ocupa exactamente **4 bytes** en memoria porque almacena puntos de código Unicode completos, no simples bytes de texto ASCII.
* **Strings (`&str` y `String`):** Son cadenas de texto completas y se escriben con **comillas dobles** (`"Hola Rust"`).

```rust
fn main/() {} // Cuidado con la sintaxis, el main correcto es sin barra diagonal:
```

```rust
fn main() {
    let letra: char = 'R';           // Comillas simples, 4 bytes
    let emoji: char = '🦀';          // Soporta emojis nativamente
    let saludo: &str = "Hola, Rust"; // Cadena estática prestada
}
```



![Diagrama 2](capitulos/02_variables_y_tipos_img_2.svg)



---

## Resumen del Capítulo

1. **`let` es inmutable** por defecto. Si necesitas cambiar datos, declara `let mut`.
2. El **Shadowing** te permite reutilizar nombres de variables cambiando incluso su tipo.
3. Los tipos numéricos (`i32`, `u8`, `f64`) definen explícitamente cuántos bits consumen en la memoria.
4. `'r'` es un `char` de 4 bytes con comillas simples; `"rust"` es una cadena con comillas dobles.