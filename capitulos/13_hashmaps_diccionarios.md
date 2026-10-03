# Capítulo 13: Colecciones III: HashMaps (Los Diccionarios de Rust)

> 🧠 **EN 10 SEGUNDOS (TDAH):** Un `HashMap<K, V>` es una estructura clave-valor almacenada en el Heap. Permite buscar, insertar y borrar datos usando una clave (`K`) para encontrar un valor (`V`) en tiempo casi constante, usando una función hash matemática.

---

### ¿Cómo funciona un HashMap por dentro?

A diferencia de los vectores que guardan datos en orden secuencial, el `HashMap` dispersa los datos en la memoria usando una función hash sobre la clave.



![Diagrama 1](capitulos/13_hashmaps_diccionarios_img_1.svg)



> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TS/JS usas objetos literales (`{ [key: string]: number }`) o `Map<string, number>`. En Rust, `HashMap<K, V>` se comporta conceptualmente igual al `Map` de JavaScript, pero con tipado estricto y gestión de memoria sin recolector de basura (Garbage Collector).

---

### Creación e Inserción Básica

Para usar un `HashMap`, primero debemos importarlo desde la librería estándar (`std::collections::HashMap`).

```rust
use std::collections::HashMap;

fn main() {
    // Creamos un mapa mutable
    let mut puntuaciones = HashMap::new();

    // Insertamos claves y valores
    puntuaciones.insert(String::from("Azul"), 10);
    puntuaciones.insert(String::from("Rojo"), 50);

    // Acceso seguro con .get(), devuelve un Option<&V>
    let equipo = String::from("Azul");
    match puntuaciones.get(&equipo) {
        Some(&puntos) => println!("El equipo {equipo} tiene {puntos} puntos."),
        None => println!("El equipo no existe."),
    }
}
```

---

### La joya de la corona: La API `entry()` y `or_insert()`

Al contar elementos o actualizar valores condicionalmente, comprobar si una clave existe manualmente es lento y tedioso. Rust provee el método `entry()`.

`entry()` inspecciona si la clave existe y devuelve un `enum` llamado `Entry`:
* Si existe, nos da acceso mutable al valor existente.
* Si no existe, inserta un valor por defecto.



![Diagrama 2](capitulos/13_hashmaps_diccionarios_img_2.svg)



---

### Ejemplo práctico: Conteo de frecuencias de palabras

Este patrón se usa constantemente para contar ocurrencias de elementos en un texto:

```rust
use std::collections::HashMap;

fn main() {
    let texto = "hola mundo hola rust mundo hola";
    let mut frecuencias = HashMap::new();

    for palabra in texto.split_whitespace() {
        let contador = frecuencias.entry(palabra).or_insert(0);
        *contador += 1; // Incrementamos el valor al que apunta la referencia mutable
    }

    println!("{:?}", frecuencias);
    // Salida esperada (el orden puede variar): 
    // {"mundo": 2, "hola": 3, "rust": 1}
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Intentar usar una clave después de insertarla en el HashMap (si implementa `String` o tipos que hacen `Move`) te dará un error de propiedad (*ownership*).
> ```rust
> let mut mapa = HashMap::new();
> let clave = String::from("id");
> mapa.insert(clave, 1);
> // ¡Error! 'clave' se movió al HashMap. Ya no puedes usarla aquí:
> println!("{clave}"); 
> ```
> *Solución:* Pasa una referencia con `.clone()` si necesitas conservar la variable original, o usa tipos primitivos como `i32` o `&str` que implementan el trait `Copy`.