# Capítulo 27: Workspaces de Cargo: Monorrepositorios Profesionales

> 🧠 **EN 10 SEGUNDOS (TDAH):** Un **workspace** de Cargo une múltiples `crates` independientes en un solo directorio raíz. Comparten la misma carpeta `target/` y el archivo `Cargo.lock`, ahorrando gigabytes de disco y acelerando las compilaciones a lo loco.

Organizar código a medida que crece es un reto. Si creas proyectos separados para tu API, tu cliente CLI y tu librería compartida, terminarás copiando archivos o duplicando dependencias. 

Los **Cargo Workspaces** solucionan esto permitiéndote gestionar múltiples subproyectos bajo un mismo techo sin perder su independencia.

---

## Anatomía de un Workspace en Rust

Un workspace se define mediante un archivo `Cargo.toml` raíz que **no tiene código fuente propio**, sino que actúa como director de orquesta.

```toml
[workspace]
members = [
    "core_engine",
    "cli_tool",
    "api_server"
]
resolver = "2"
```

Cada miembro (`core_engine`, `cli_tool`, `api_server`) es un `crate` totalmente normal con su propia carpeta y su propio `Cargo.toml`.

<div align="center">


![Diagrama 1](capitulos/27_workspaces_cargo_img_1.svg)


</div>

---

## Dependencias Internas y Versiones Compartidas

Para que `cli_tool` use el `core_engine`, solo debes declararlo en su propio `Cargo.toml` usando rutas relativas:

```toml
# cli_tool/Cargo.toml
[dependencies]
core_engine = { path = "../core_engine" }
```

### El superpoder del `[workspace.dependencies]`
Desde Rust 1.64+, puedes centralizar las versiones de tus dependencias externas en la raíz. Así evitas que un crate use `tokio = "1.28"` y otro `tokio = "1.35"`.

```toml
# Cargo.toml (Raíz del Workspace)
[workspace]
members = ["core_engine", "cli_tool"]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1.38", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
```

Luego, en los miembros del workspace, las consumes sin especificar la versión:

```toml
# core_engine/Cargo.toml
[dependencies]
tokio.workspace = true
serde.workspace = true
```

> 🟦 **CONEXIÓN TYPESCRIPT/JAVASCRIPT:** En el ecosistema Node.js, esto equivale exactamente a los **pnpm workspaces** o **Turborepo** combinados con `workspace:*` en el `package.json`. La gran diferencia: Rust compila todo nativamente de forma incremental y maneja los binarios con un único `Cargo.lock` blindado contra el "dependency hell".

---

## Errores Comunes de Compilación

> 🟥 **FRENAZO DEL COMPILADOR:** Intentar compilar un crate de forma aislada (*fuera del workspace*) usando dependencias relativas rotas o versiones no sincronizadas.
>
> ```text
> error: no matching package found for `core_engine`
> location searched: fileложена dependency path
> ```
> **Por qué ocurre:** Si ejecutas `cargo build` dentro de la carpeta `cli_tool/` sin tener en cuenta el workspace raíz, Cargo buscará el crate en crates.io en lugar de mirar dos carpetas hacia arriba.
> **Solución:** Ejecuta siempre los comandos de Cargo desde la raíz del workspace, o usa la bandera `--manifest-path`. Cargo es inteligente y detectará automáticamente el workspace si estás dentro de cualquiera de sus subcarpetas.