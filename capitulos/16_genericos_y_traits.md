# Capítulo 16: Genéricos y Traits: Interfaces con Superpoderes

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los genéricos permiten escribir código reutilizable para cualquier tipo de dato, mientras que los *traits* son contratos que obligan a un tipo a tener ciertas habilidades. El compilador verifica todo esto **antes** de ejecutar el programa.

---

## 1. Genéricos: Escribe Código una Sola Vez

En programación, a menudo necesitamos realizar la misma lógica para diferentes tipos de datos. Copiar y pegar código es el enemigo. Los genéricos nos permiten usar comodines (como `<T>`) para decir: *"esta función o struct funciona para cualquier tipo"*.

```rust
// Una función genérica que acepta cualquier tipo T que soporte la comparación
fn mayor<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    println!("{}", mayor(10, 20));       // Funciona con i32
    println!("{}", mayor(3.14, 2.71));   // Funciona con f64
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TypeScript usas funciones genéricas como `function mayor<T>(a: T, b: T): T`. La gran diferencia es que TypeScript borra los genéricos al compilar (borrado de tipos). En Rust, el compilador **examina cada uso real** y genera una versión de código nativo optimizada e hiper-rápida para cada tipo específico (*monomorfización*).

---

## 2. Visualizando los Genéricos y la Memoria

El siguiente diagrama muestra cómo un único molde genérico se convierte en código máquina especializado para enteros y decimales sin perder rendimiento.



![Diagrama 1](capitulos/16_genericos_y_traits_img_1.svg)



---

## 3. Traits: Contratos de Comportamiento

Un `trait` define un conjunto de métodos que un tipo debe implementar. Es muy similar a una `interface` en TypeScript o una interfaz en Java o C#.

Imagina que creas un videojuego y quieres que tanto un `Guerrero` como un `Mago` puedan emitir un grito de batalla.

```rust
// Definimos el contrato (trait)
trait Gritar {
    fn gritar(&self) -> String;
}

struct Guerrero;
struct Mago;

// Implementamos el trait para el Guerrero
impl Gritar for Guerrero {
    fn gritar(&self) -> String {
        String::from("¡Por la espada y el honor!")
    }
}

// Implementamos el trait para el Mago
impl Gritar for Mago {
    fn gritar(&self) -> String {
        String::from("¡Que la magia arda!")
    }
}

fn hacerle_gritar<T: Gritar>(item: T) {
    println!("{}", item.ritar());
}
```

---

## 4. Trait Bounds y Derivación Automática

A veces, al usar genéricos, necesitamos restringir qué tipos son aceptados. Esto se hace mediante **trait bounds** (límites de trait), usando dos sintaxis principales:

```rust
// Sintaxis con Trait Bound clásico
fn mostrar_elemento<T: std::fmt::Debug>(item: T) {
    println!("{:?}", item);
}

// Sintaxis con 'impl Trait' (más limpia para argumentos simples)
fn mostrar_elemento_corto(item: impl std::fmt::Debug) {
    println!("{:?}", item);
}
```

### Derivación Automática (`#[derive(...)]`)
Rust te evita escribir código repetitivo para comportamientos estándar comunes mediante macros de derivación. Los más vitales en el día a día son:

- **`Debug`**: Permite imprimir el struct usando la sintaxis `{:?}` para depurar.
- **`Clone`**: Permite duplicar el dato explícitamente con `.clone()`.
- **`PartialEq`**: Permite comparar dos instancias usando operadores de igualdad `==`.

```rust
#[derive(Debug, Clone, PartialEq)]
struct Usuario {
    id: u64,
    nombre: String,
}

fn main() {
    let u1 = Usuario { id: 1, nombre: String::from("Ada") };
    let u2 = u1.clone(); // Gracias a #[derive(Clone)]

    if u1 == u2 { // Gracias a #[derive(PartialEq)]
        println!("¡Son exactamente iguales!");
    }
    
    println!("{:?}", u1); // Gracias a #[derive(Debug)]
}
```

> 🟥 **FRENAZO DEL COMPILADOR:**
> Intenta hacer esto sin el macro de derivación:
> ```rust
> struct Secreto { codigo: u32 }
> 
> fn main() {
>     let s = Secreto { codigo: 42 };
>     println!("{:?}", s); // ERROR DE COMPILACIÓN
> }
> ```
> El compilador te dirá furioso: *``Secreto` doesn't implement `Debug*. Te explicará amablemente que Rust no adivina cómo quieres mostrar tu estructura y te sugerirá agregar `#[derive(Debug)]` en la línea superior. Cero sorpresas en producción.
```
```
