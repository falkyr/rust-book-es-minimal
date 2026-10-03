# Capítulo 18: Programación Funcional: Closures e Iteradores

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los closures son bloques de código que recuerdan su entorno, y los iteradores son tuberías eficientes para procesar datos sin crear copias innecesarias. En Rust, todo esto es seguro porque el compilador rastrea exactamente cómo prestas y consumes tus variables.

---

## 1. Closures: Funciones Anónimas con Memoria

Un closure es una función que puedes guardar en una variable, pasar como argumento y que tiene superpoderes: puede capturar variables del ámbito que la rodea.

A diferencia de las funciones normales declaradas con `fn`, los closures no requieren que declares los tipos de sus parámetros (el compilador los deduce) y usan barras verticales `|` para sus argumentos.

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:**
> En JS/TS usas funciones flecha: `const sumar = (a, b) => a + b;`. 
> En Rust, escribes: `let sumar = |a, b| a + b;`. Sintácticamente son primas hermanas, pero por debajo Rust hace algo radicalmente distinto con la memoria.

### Los Tres Tratos de la Captura: Fn, FnMut y FnOnce

En JavaScript, si una función flecha accede a una variable externa, simplemente la lee o la modifica y el recolector de basura se encarga del resto. En Rust, cada closure implementa uno o más *traits* especiales basados en *cómo* captura su entorno:

1. **`FnOnce`**: Consume las variables que captura (las mueve al closure). Solo se puede ejecutar **una vez** porque destruye su entorno.
2. **`FnMut`**: Toma prestadas las variables del entorno **de forma mutable** (`&mut`). Puede modificar el entorno y ejecutarse varias veces.
3. **`Fn`**: Toma prestadas las variables del entorno **de forma inmutable** (`&`). Puede ejecutarse muchas veces en paralelo sin alterar nada.

```rust
fn main3() {
    let nombre = String::from("Rust");

    // Este closure toma la propiedad de 'nombre' (FnOnce)
    let consumir = || {
        let _propietario = nombre; 
    };

    consumir();
    // println!("{}", nombre); // ERROR DE COMPILACIÓN: 'nombre' ya no vive aquí.
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Si intentas usar un closure después de que se ha tragado una variable con `FnOnce`, el compilador te gritará que usaste un valor movido (*use of moved value*). Rust te protege de usar datos huérfanos.

---

## 2. Visualizando Closures y su Entorno

El siguiente diagrama muestra cómo un closure atrapa variables del stack dependiendo de su política de acceso (`Fn`, `FnMut` o `FnOnce`).



![Diagrama 1](capitulos/18_closures_e_iteradores_img_1.svg)



---

## 3. Iteradores: Cero Coste y Rendimiento Brutal

En muchos lenguajes, usar métodos como `.map()` o `.filter()` crea nuevos arreglos en memoria dinámicamente, penalizando el rendimiento. 

En Rust, **los iteradores son perezosos (lazy)**. No hacen absolutamente nada hasta que los consumes con un método como `.collect()` o `.forEach()`. El compilador optimiza estas cadenas de iteradores hasta convertirlas en bucles `for` nativos ultrarrápidos (abstracción de coste cero).

### Los Tres Reyes del Estilo Funcional

1. **`map`**: Transforma cada elemento aplicando un closure.
2. **`filter`**: Filtra elementos devolviendo un booleano basado en una condición.
3. **`fold`**: Reduce toda una colección a un solo valor acumulado (equivalente a `reduce` en JS).

```rust
fn main() {
    let numeros = vec![1, 2, 3, 4, 5];

    // Cadena funcional de iteradores
    let suma_cuadrados: i32 = numeros
        .iter()                    // Creamos un iterador de referencias (&i32)
        .map(|&x| x * x)           // Elevamos al cuadrado cada número
        .filter(|&x| x > 10)       // Filtramos los mayores a 10
        .fold(0, |acum, val| acum + val); // Sumamos todo acumulando en '0'

    println!("Resultado final: {}", suma_cuadrados); // 16 (9 + 25 = 34... espera: 3^2=9, 4^2=16, 5^2=25. >10 son 16 y 25 -> 41)
}
```

---

## 4. Anatomía Visual de un Pipeline de Iteradores

Observa cómo los datos fluyen perezosamente a través de adaptadores puramente lógicos antes de ser consumidos en una única pasada optimizada.



![Diagrama 2](capitulos/18_closures_e_iteradores_img_2.svg)



---

## 5. Resumen del Capítulo

* Los **closures** en Rust son funciones anónimas capaces de capturar su entorno de tres formas estrictas: `Fn`, `FnMut` y `FnOnce`.
* El sistema de ownership de Rust analiza con precisión milimétrica si un closure toma prestado o roba las variables externas.
* Los **iteradores** son perezosos (*lazy*): no ejecutan operaciones hasta que un consumidor los activa.
* Gracias al modelo de optimización de LLVM en Rust, el código funcional con iteradores compila siendo tan rápido o más que un bucle `for` manual escrito en C.