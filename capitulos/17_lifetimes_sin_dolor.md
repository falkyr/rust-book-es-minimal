# Capítulo 17: Lifetimes: El Tiempo de Vida de las Referencias

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los *lifetimes* son etiquetas invisibles que el compilador usa para asegurarse de que una referencia nunca viva más tiempo que el dato al que apunta. ¡Adiós a los punteros colgantes (dangling pointers)!

---

## 1. El Problema: ¿Cuánto vive una referencia?

En Rust, cuando prestas un valor usando una referencia (`&`), el compilador necesita saber con absoluta certeza cuánto tiempo será válido ese préstamo. Si el propietario original del dato muere (sale de su scope), la referencia se vuelve peligrosa.

Imagina que alquilas un apartamento. El dueño del apartamento decide demolerlo. Si tú sigues adentro, estás usando un recurso que ya no existe. En programación, esto se llama **puntero colgante**.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS existe el *Garbage Collector*. Si un objeto sigue referenciado, el recolector no lo borra. Si ya no se usa, lo limpia tarde o temprano. En Rust **no hay recolector de basura**. El compilador previene estos desastres analizando el tiempo de vida en tiempo de compilación.

---

## 2. La Sintaxis de los Lifetimes (`'a`)

Para decirle al compilador cómo se relacionan los tiempos de vida de diferentes referencias, usamos anotaciones de lifetime. Su símbolo es una comilla simple seguida de una letra minúscula, por lo general `'a`.

Observa este diagrama SVG que ilustra cómo una referencia no puede sobrevivir a su propietario en el Stack:



![Diagrama 1](capitulos/17_lifetimes_sin_dolor_img_1.svg)



Cuando creas una función que toma prestados dos strings y devuelve el más largo, el compilador no sabe si devolverá el primero o el segundo. Necesita que le asegures que la referencia resultante vivirá tanto como el menor de los dos inputs.

```rust
// Anotamos 'a para vincular los tiempos de vida
fn mas_largo<'a>(s1: &'a str, s2: &'a str) -> &'a str {
    if s1.len() > s2.len() {
        s1
    } else {
        s2
    }
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> ```text
> error[E0106]: missing lifetime specifier
>   --> src/main.rs:1:33
>    |
> 1  | fn mas_largo(s1: &str, s2: &str) -> &str {
>    |                  ----      ----     ^ expected named lifetime parameter
> ```
> **Por qué ocurre:** Rust te obliga a poner una anotación de lifetime cuando devuelves una referencia, porque no sabe a qué parámetro pertenecerá el dato retornado en tiempo de ejecución.

---

## 3. Reglas de Elisión (El compilador hace el trabajo sucio)

Escribir `'a` en todas partes sería agotador. Por suerte, los creadores de Rust diseñaron **reglas de elisión de lifetimes**. El compilador aplica tres reglas automáticas para deducir los lifetimes sin que tengas que escribirlos:

1. Cada parámetro de referencia recibe su propio parámetro de lifetime. (Ej: `fn foo(s1: &str, s2: &str)` se convierte en `fn foo<'a, 'b>(s1: &'a str, s2: &'b str)`).
2. Si hay exactamente un parámetro de entrada con referencia, su lifetime se asigna a *todos* los outputs.
3. Si hay múltiples parámetros de entrada, pero uno de ellos es `&self` o `&mut self` (en métodos de structs), el lifetime de `self` se asigna a todos los outputs.

Si el compilador aplica estas reglas y aún quedan dudas, te pedirá amablemente que escribas las anotaciones de forma explícita.

---

## Resumen del Capítulo

- Los **lifetimes** previenen punteros colgantes garantizando que una referencia nunca viva más que su recurso.
- La sintaxis usa comillas y una letra (ej. `'a`), indicando que los datos comparten el mismo periodo de validez.
- El compilador calcula muchos lifetimes automáticamente gracias a las **reglas de elisión**, por lo que solo debes intervenir en firmas de funciones complejas.