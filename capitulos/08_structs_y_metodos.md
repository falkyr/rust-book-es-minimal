# Capítulo 8: Structs: Modelando Datos sin Clases Clásicas

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust no usa clases ni herencia. Usa **structs** para agrupar datos y bloques `impl` para ponerles funciones y métodos. Simple, plano y sin jerarquías locas.

---

En Rust, los objetos y las clases de otros lenguajes se dividen en dos piezas separadas: 
1. Los **datos** viven en un `struct`.
2. Las **acciones** viven en un bloque `impl` (implementation).

Esta separación hace que el código sea mucho más fácil de leer para un cerebro con TDAH: sabes exactamente dónde están las variables y dónde están las funciones.



![Diagrama 1](capitulos/08_structs_y_metodos_img_1.svg)



---

## 1. Definiendo e Instanciando Structs

Un `struct` es una estructura de datos con nombre que agrupa varios valores relacionados. 

```rust
// Definimos el struct
struct Jugador {
    nombre: String,
    vida: u32,
    puntuacion: u64,
}

fn main() {
    // Instanciamos el struct
    let jugador1 = Jugador {
        nombre: String::from("Ferris"),
        vida: 100,
        puntuacion: 4200,
    };

    println!("Jugador: {}, Vida: {}", jugador1.nombre, jugador1.vida);
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TypeScript usas interfaces o tipos (`type User = { name: string; age: number }`) solo para chequear tipos en tiempo de compilación; en JavaScript plano eso desaparece. En Rust, un `struct` es real, vive en la memoria binaria de tu programa y define exactamente cómo se empaquetan los bytes.

---

## 2. Métodos y el bloque `impl`

Para asociar funciones a un `struct`, usamos la palabra clave `impl` (abreviatura de *implementation*).

Dentro de un bloque `impl`, el primer parámetro de un método suele ser `self`, que representa la instancia del struct que está llamando a la función.

Tenemos tres formas de recibir `self` según lo que necesitemos hacer:
1. `&self`: Solo lectura (toma prestado el struct sin modificarlo).
2. `&mut self`: Lectura y escritura (modifica el struct).
3. `self`: Consumo total (destruye el struct y toma posesión de sus datos).

```rust
struct Jugador {
    nombre: String,
    vida: u32,
}

impl Jugador {
    // Método de solo lectura (&self)
    fn saludar(&self) {
        println!("¡Hola, soy {}!", self.nombre);
    }

    // Método de modificación (&mut self)
    fn recibir_daño(&mut self, cantidad: u32) {
        self.vida = self.vida.saturating_sub(cantidad);
        println!("{} recibió daño. Vida restante: {}", self.nombre, self.vida);
    }
}

fn main() {
    let mut p = Jugador {
        nombre: String::from("Rustacean"),
        vida: 100,
    };

    p.saludar();         // Llama a &self
    p.recibir_daño(25);  // Llama a &mut self
}
```

---

## 3. Constructores Asociados (`Self::new`)

Rust no tiene la palabra clave `constructor` como JavaScript o TypeScript. En su lugar, por convención se crea una función asociada llamada `new` que devuelve una nueva instancia del `struct`.

Observa el uso de `Self` (con la 'S' mayúscula), que actúa como un alias del tipo del struct en el que estás trabajando.

```rust
struct Coordenada {
    x: i32,
    y: i32,
}

impl Coordenada {
    // Función asociada (no recibe self, se llama con Coordenada::new())
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    // Método normal que lee los datos
    fn mostrar(&self) {
        println!("Posición: ({}, {})", self.x, self.y);
    }
}

fn main() {
    // Usamos el constructor
    let punto = Coordenada::new(10, 20);
    punto.mostrar();
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Si intentas llamar a un método que modifica el struct (`&mut self`) pero olvidaste marcar tu variable como mutable (`let mut obj = ...`), Rust te detendrá en seco:
> 
> ```text
> error[E0596]: cannot borrow `p` as mutable, as it is not declared as mutable
>   --> src/main.rs:20:5
>   |
> 18 |     let p = Jugador { ... };
>   |         - help: consider changing this to be mutable: `let mut p`
> 19 |     p.recibir_daño(25);
>   |     ^^^^^^^^^^^^^^^^^^ cannot borrow as mutable
> ```
> *El compilador te cuida la espalda:* Te obliga a declarar explícitamente qué datos pueden cambiar en tu programa, evitando efectos secundarios ocultos tan comunes en JavaScript.