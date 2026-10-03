# Capítulo 12: Colecciones II: Strings UTF-8 en Profundidad

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los strings en Rust no son arreglos simples de caracteres; son secuencias seguras de bytes codificados en UTF-8. Como un carácter puede ocupar de 1 a 4 bytes, Rust te prohíbe usar índices como `s[0]` para evitar romper la memoria y corromper texto internacional.

---

## 1. El gran misterio: ¿Por qué no existe `s[0]` en Rust?

En JavaScript, si tienes un string, puedes hacer `s[0]` y obtienes la primera letra de inmediato. O eso crees. Bajo el capó, JS a veces sufre con caracteres especiales y emojis porque maneja mal los pares de sustitutos UTF-16.

Rust decide no mentirte. Un `String` es un vector de bytes (`Vec<u8>`) validado estrictamente para cumplir con el estándar UTF-8. 

Mira esta ilustración para entender por qué un índice directo destruiría el rendimiento y la seguridad:



![Diagrama 1](capitulos/12_strings_utf8_sin_miedo_img_1.svg)



> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS, `s[0]` busca unidades de código UTF-16. Los emojis altos como `🦀` usan dos unidades (un par de sustitutos). Si intentas cortarlos con métodos ingenuos de String, terminas rompiendo caracteres visuales (graphemes) y generando símbolos extraños.

---

## 2. Los Tres Niveles de Vista de un String

Para trabajar con texto en Rust sin volverte loco, debes entender que el mismo string se puede ver de tres formas distintas:

1. **Bytes (`.bytes()`):** Secuencia pura de números `u8`. Ideal para procesamiento de bajo nivel o red.
2. **Valores escalares (`.chars()`):** Caracteres Unicode individuales (`char` de 4 bytes). Por ejemplo, `🦀` es un `char`.
3. **Grafemas (Graphemes):** Lo que tus ojos humanos perciben como una sola letra con acentos o combinaciones (requiere la crate externa `unicode-segmentation`).

```rust
fn main() {
    let saludo = "Høla 🦀";

    // 1. Como bytes puros
    println!("Bytes: {}", saludo.len()); // Muestra los bytes totales (8 bytes)

    // 2. Como valores escalares (.chars())
    for c in saludo.chars() {
        print!("{} ", c);
    }
    // Imprime: H ø l a   🦀
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si intentas hacer esto en tu código:
> ```rust
> fn main() {
>     let s = String::from("Hola");
>     let letra = s[0]; // Error de compilación
> }
> ```
> El compilador te arrojará este error inconfundible:
> ```text
> error[E0277]: the type `str` cannot be indexed by `usize`
>    --> src/main.rs:3:19
>     |
> 3 |     let letra = s[0];
>     |                   ^ `str` cannot be indexed by `usize`
>     |
>     = help: the trait `Index<usize>` is not implemented for `str`
>     = help: the trait `Index<Range<usize>>` is implemented for `str`, but with caution!
> ```
> **¿Qué bug evitó?** Evitó que escribas código O(1) falso que en realidad requeriría recorrer el string desde el inicio si se permitiera indexación arbitraria sobre grafemas de longitud variable.

---

## 3. Manipulación Eficiente: `push_str` y `format!`

Como los strings crecen y se encogen en el Heap, modificar un `String` mutable es muy similar a manipular un `Vec<T>`.

### Agregando contenido con `push` y `push_str`

- `push(&mut self, ch: char)`: Añade un único carácter Unicode.
- `push_str(&mut self, string: &str)`: Añade un slice de string completo sin tomar posesión de él.

```rust
fn main() {
    let mut mensaje = String::from("Rust");
    
    mensaje.push_str(" es");
    mensaje.push(' ');
    mensaje.push_str("genial 🚀");

    println!("{}", mensaje); // "Rust es genial 🚀"
}
```

### Concatenación limpia con la macro `format!`

Cuando necesitas unir múltiples variables sin lidiar con reglas complejas de ownership de los operadores `+`, la macro `format!` es tu mejor aliada. Funciona exactamente igual que `println!`, pero en lugar de imprimir en consola, **devuelve un nuevo `String`**.

```rust
fn main() {
    let lenguaje = "Rust";
    let version = 2024;
    
    // format! toma referencias prestadas sin consumir las variables originales
    let info = format!("Estás programando en {} edición {}.", lenguaje, version);
    
    println!("{}", info);
}
```

> 🧠 **EN 10 SEGUNDOS (TDAH):** Usa `.chars()` si quieres iterar letras, `.push_str()` para mutar texto acumulando partes, y `format!` cuando quieras ensamblar strings complejos de forma limpia y sin pelearte con el ownership.
