# Capítulo 15: Módulos y Crates: Arquitectura de Proyectos

> 🧠 **EN 10 SEGUNDOS (TDAH):** Los crates son tus bibliotecas compilables. Los módulos (`mod`) son carpetas y archivos virtuales dentro del crate que organizan tu código como un armario ordenado, controlando quién puede ver qué con la regla de oro: **todo es privado por defecto**.

---

## 1. El Árbol de Módulos: Tu Código como un Mapa Mental

Imagina tu proyecto de Rust como un edificio de oficinas. Cada archivo y cada bloque `mod` es una habitación. El compilador empieza a buscar siempre desde la recepción principal: el archivo raíz (`main.rs` o `lib.rs`).

```rust
// main.rs o lib.rs
mod red {
    pub fn conectar() {
        println!("Conectando al servidor...");
    }
}

fn main() {
    red::conectar(); // Llamando a una función dentro del módulo red
}
```

Para visualizar cómo Rust conecta estos espacios lógicamente, mira el siguiente árbol jerárquico:



![Diagrama 1](capitulos/15_modulos_y_visibilidad_img_1.svg)



> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En TS/JS usas `import { algo } from './archivo'` creando rutas basadas en archivos físicos de forma muy flexible. Rust separa los archivos físicos de la estructura lógica: defines qué existe con la palabra `mod` y controlas el acceso estrictamente por jerarquía de padres e hijos.

---

## 2. Privacidad por Defecto y el Poder de `pub`

En Rust, **todo es privado por defecto**. Si creas una función, un struct o un módulo, sus hermanos y el mundo exterior no pueden verlo a menos que abras explícitamente la puerta con `pub`.

```rust
mod cafeteria {
    // Privado por defecto: solo visible dentro de 'cafeteria'
    fn calentar_agua() {
        println!("Calentando agua...");
    }

    // Público: visible para cualquiera que alcance este módulo
    pub fn servir_cafe() {
        calentar_agua(); // Permitido internamente
        println!("Aquí tienes tu café.");
    }
}

fn main() {
    cafeteria::servir_cafe(); // Funciona perfecto
    // cafeteria::calentar_agua(); // ERROR DE COMPILACIÓN: es privado
}
```

> 🟥 **FRENAZO DEL COMPILADOR:** Si intentas acceder a un campo de un struct público cuyos campos no son públicos, Rust te detendrá en seco:
> ```text
> error[E0616]: field `password` of struct `User` is private
>   --> src/main.rs:10:20
>    |
> 10 |     let p = user.password;
>    |                  ^^^^^^^^ private field
> ```
> **La solución:** Debes marcar explícitamente el campo como `pub struct User { pub password: String }` o proveer un método getter público (`pub fn password(&self) -> &str`).

---

## 3. Navegando el Laberinto: Rutas Absolutas y Relativas

Para encontrar código dentro de tu crate, puedes usar dos tipos de rutas:

1. **Rutas Absolutas:** Comienzan desde la raíz del crate usando la palabra clave `crate::`. Son ideales para saltar desde submódulos profundos directamente a servicios globales.
2. **Rutas Relativas:** Comienzan desde el módulo actual usando `self`, el nombre del hijo, o `super::` para subir un nivel hacia el padre (como el `../` en rutas de terminal).

```rust
fn calentar_agua() {}

mod cocina {
    pub fn preparar_desayuno() {
        // Ruta absoluta desde la raíz del crate
        crate::calentar_agua();

        // Ruta relativa subiendo al padre (si hubiera algo arriba)
        // super::otra_funcion();

        // Ruta relativa usando self (mismo nivel)
        self::freir_huevos();
    }

    fn freir_huevos() {
        println!("Fritando huevos...");
    }
}
```

---

## 4. Reexportación Limpia con `pub use`

A veces, la estructura interna de tus carpetas es compleja y profunda, pero quieres ofrecer una interfaz simple y directa a quienes usen tu librería. Aquí es donde entra `pub use`.

Te permite exponer en la superficie de tu módulo funciones o structs que están enterrados tres niveles más abajo.

```rust
mod backend {
    pub mod auth {
        pub fn verificar_token(token: &str) -> bool {
            token == "secreto_valido"
        }
    }
}

// Reexportamos la función para que parezca que está directamente en el módulo raíz
pub use backend::auth::verificar_token;

fn main() {
    // El usuario final llama directamente a la función limpia
    let valido = verificar_token("secreto_valido");
    assert!(valido);
}
```

Veamos visualmente cómo `pub use` crea un atajo directo sin alterar tu orden interno:



![Diagrama 2](capitulos/15_modulos_y_visibilidad_img_2.svg)



---

## Resumen del Capítulo

- **Árbol de Módulos:** Organiza tu código lógicamente imitando la estructura de directorios o mediante bloques `mod`.
- **Privacidad:** Todo es privado por defecto. Usa `pub` para abrir visibilidad de forma consciente.
- **Rutas:** `crate::` para ir a la raíz absoluta, `super::` para subir un nivel en el árbol.
- **`pub use`:** La navaja suiza para aplanar APIs complejas y ofrecer accesos directos elegantes a tus usuarios.