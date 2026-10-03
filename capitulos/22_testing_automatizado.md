# Capítulo 22: Testing Automatizado: El Arnés Nativo sin Jest ni Mocha

> 🧠 **EN 10 SEGUNDOS (TDAH):** Rust trae un sistema de pruebas integrado en el propio compilador. No necesitas instalar Jest, Mocha, ni configurar librerías externas. Ejecutas `cargo test` y Rust se encarga de todo.

---

El desarrollo en Rust es rápido porque el compilador atrapa los bugs de tipos y memoria antes de ejecutar. Pero la lógica de negocio requiere validación humana. A diferencia de JavaScript o TypeScript, donde debes elegir entre Jest, Vitest, Mocha y configurar TypeScript con `ts-node`, Rust incluye un **arnés de pruebas nativo** desde el día uno.

---

## 1. Aserciones Básicas: Tus Nuevas Armas

El módulo estándar de Rust incluye macros potentes para validar resultados. No requieres importar librerías externas de aserciones.

```rust
pub fn sumar(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_suma() {
        let resultado = sumar(2, 2);
        
        // 1. Verifica booleans puros
        assert!(resultado == 4);
        
        // 2. Verifica igualdad (Equivalente a expect(a).toBe(b))
        assert_eq!(resultado, 4);
        
        // 3. Verifica desigualdad
        assert_ne!(resultado, 5);
    }
}
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En JS/TS haces `expect(resultado).toBe(4)`. En Rust, usas macros directas como `assert_eq!(resultado, 4);`. La macro imprime automáticamente los valores de ambos lados si la prueba falla, sin plugins adicionales.

---

## 2. Esperando el Caos: `#[should_panic]`

A veces, escribir código robusto significa asegurarte de que tu programa **falle a propósito** cuando recibe datos inválidos.

```rust
pub struct Rectangulo {
    ancho: u32,
    alto: u32,
}

impl Rectangulo {
    pub fn new(ancho: u32, alto: u32) -> Self {
        if ancho == 0 || alto == 0 {
            panic!("Las dimensiones deben ser mayores a cero.");
        }
        Rectangulo { ancho, alto }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "dimensiones deben ser mayores")]
    fn falla_con_cero() {
        // Esta línea hace un panic!, lo cual PASA la prueba 
        // porque esperamos ese panic exacto.
        let _r = Rectangulo::new(0, 10);
    }
}
```

---

## 3. Anatomía de los Tests Unitarios

Los tests unitarios viven en el mismo archivo que tu código productivo, protegidos por un condicional de compilación para que no aumenten el peso de tu binario final.



![Diagrama 1](capitulos/22_testing_automatizado_img_1.svg)



---

## 4. Pruebas de Integración: LaCarpeta `/tests`

Mientras los tests unitarios prueban funciones aisladas y privadas, los **tests de integración** se ubican en una carpeta raíz llamada `tests/`. Simulan ser un cliente externo usando tu crate como si fuera una librería instalada desde `crates.io`.

```
mi_proyecto/
├── Cargo.toml
├── src/
│   └── lib.rs
└── tests/
    └── integration_test.rs  <-- Cada archivo aquí es un crate independiente
```

Ejemplo dentro de `tests/integration_test.rs`:

```rust
// No necesitas #[cfg(test)] aquí, Cargo ya sabe que esta carpeta es para pruebas.
use mi_proyecto;

#[test]
fn test_conexion_externa() {
    let resultado = mi_proyecto::sumar(10, 20);
    assert_eq!(resultado, 30);
}
```

Para correr únicamente las pruebas de integración específicas de un archivo:
```bash
cargo test --test integration_test
```

---

> 🟥 **FRENAZO DEL COMPILADOR:** Intentar importar funciones privadas desde un test de integración externo.
> 
> ```text
> error[E0603]: function `funcion_secreta` is private
>  --> tests/integration_test.rs:3:22
>   |
> 3 | use mi_proyecto::funcion_secreta;
>   |                   ^^^^^^^^^^^^^^ private function
> ```
> 
> **Por qué ocurre:** Los tests de integración son **consumidores externos** (como cualquier usuario en internet). Solo pueden acceder a funciones marcadas con `pub`. Si quieres probar lógica interna privada, usa un test unitario dentro del mismo archivo `src/lib.rs`.

---

## Resumen del Comando `cargo test`

* `cargo test`: Ejecuta todas las pruebas unitarias e de integración en paralelo.
* `cargo test nombre_de_test`: Ejecuta únicamente las pruebas cuyo nombre coincida con el patrón.
* `cargo test -- --nocapture`: Muestra por consola los `println!` dentro de tus tests (útil para debug rápido).