# Capítulo 5: El Jefe Final: Ownership (Propiedad) y la Memoria

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust gestiona tu memoria sin un recolector de basura (Garbage Collector). Lo hace mediante una sola regla estricta: cada dato tiene un único dueño. Cuando el dueño sale de escena, el dato se borra solo. Fin de los memory leaks.

---

## 1. El Escenario: Stack (Pila) vs Heap (Montón)

Para entender cómo Rust maneja la memoria, imagina que estás organizando tu dormitorio.

El **Stack** es tu escritorio. Todo está ordenado, a la vista y al alcance de la mano. Las cosas aquí tienen un tamaño fijo y conocido (un número entero, un booleano). Poner y quitar cosas del escritorio es rapidísimo.

El **Heap** es el trastero del fondo del pasillo. Guardas cosas grandes, cuyo tamaño no conoces de antemano (un texto gigante, un archivo JSON kilométrico). En el escritorio (Stack) solo dejas una nota que dice: *"El texto gigante está en la caja 42 del trastero"*. Esa nota es un **puntero**.



![Diagrama 1](capitulos/05_ownership_la_propiedad_img_1.svg)



---

## 2. Las 3 Reglas de Oro del Ownership

Para que Rust compile tu código sin un Garbage Collector (como V8 en JS), te obliga a seguir estas tres reglas sagradas:

1. Cada valor en Rust tiene un **dueño** (llamado *owner*).
2. Solo puede haber **un dueño a la vez**.
3. Cuando el dueño sale del ámbito (*scope*, delimitado por llaves `{}`), el valor se **destruye** automáticamente (`drop`).

---

## 3. Transferencia de Propiedad (Move)

Mira este código en Rust:

```rust
fn main() {
    let s1 = String::from("Rust");
    let s2 = s1; // ¡Aquí ocurre la magia oscura!

    // println!("{}", s1); // Error de compilación si descomentas esto
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS, si haces `let s2 = s1;`, ambos apuntan al mismo objeto en el Heap (copia por referencia implícita). Si modificas uno, el otro sufre cambios inesperados. En Rust, `s2 = s1` **transfiere la propiedad**. `s1` deja de ser válido instantáneamente. JS te oculta esto; Rust te lo muestra de frente para evitar bugs.

### ¿Por qué `s1` se invalida con `let s2 = s1`?

Para evitar **doble liberación de memoria** (*double free bug*). Si tanto `s1` como `s2` apuntaran al mismo bloque en el Heap, al terminar la función, ambos intentarían borrar el mismo espacio de memoria dos veces. Eso provoca fallos de seguridad críticos. 

Rust previene esto haciendo que `s1` muera en el momento exacto en que sus datos se mudan a `s2`.



![Diagrama 2](capitulos/05_ownership_la_propiedad_img_2.svg)



---

> 🟥 **FRENAZO DEL COMPILADOR:**
> 
> Si intentas usar `s1` después de asignarlo a `s2`, obtendrás este error:
> 
> ```text
> error[E0382]: use of moved value: `s1`
>  --> src/main.rs:5:20
>   |
> 3 |     let s2 = s1;
>   |              -- value moved here
> 4 | 
> 5 |     println!("{}", s1);
>   |                    ^^ value used here after move
> ```
> 
> **¿Qué bug evitó?** Evitó que leas una variable que ya no controla sus recursos, previniendo comportamientos indefinidos en memoria RAM que en C o C++ causarían pantallas azules o agujeros de seguridad.