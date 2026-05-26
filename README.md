# 🍔 Kiosko Auto-Service - Sistema de Gestión de Pedidos

![Estado](https://img.shields.io/badge/Estado-Producci%C3%B3n-success)
![Arquitectura](https://img.shields.io/badge/Arquitectura-Full--Stack-blue)
![Despliegue](https://img.shields.io/badge/Despliegue-100%25_Cloud-orange)

Un sistema de autoservicio completo diseñado para automatizar el flujo de pedidos en restaurantes o kioskos. Permite a los clientes seleccionar productos, añadir modificadores (cremas, extras, tipo de leche), elegir métodos de pago y generar vouchers automáticamente. 

Este proyecto fue desarrollado desde cero con un enfoque en escalabilidad, separación de responsabilidades (API REST) e integración continua, demostrando habilidades sólidas en la construcción de soluciones modernas listas para el trabajo remoto.

---

## 🚀 Arquitectura y Tecnologías

El proyecto está construido con una arquitectura Full-Stack, desplegado de manera independiente en servicios en la nube:

* **Frontend:** HTML, CSS, JavaScript (Vanilla). Desplegado en **Vercel**.
* **Backend:** Python con **FastAPI** y Uvicorn. Desplegado en **Render**.
* **Base de Datos:** **MySQL 8.4** alojada en la nube mediante **Aiven**.
* **Integración:** `pymysql` para la conexión y lectura de datos mediante cursores de diccionario.

---

## ⚙️ Características Principales

1. **Catálogo Dinámico:** Gestión de productos base y sus categorías de modificadores asociadas.
2. **Motor de Precios:** Cálculo automático de subtotales integrando el precio base y el costo adicional de los extras seleccionados.
3. **Flujo de Operaciones:** Registro de clientes, boletas (Ventas) y métodos de pago (Yape, Plin, Efectivo).
4. **Reportes SQL en Tiempo Real:** Implementación de Vistas SQL (`VerVentasCompletas`) que unifican 4 tablas distintas, normalizando la zona horaria UTC a hora local para la emisión de reportes financieros precisos.

---

## 🗄️ Estructura de la Base de Datos

La base de datos relacional está dividida en 3 módulos principales para garantizar la normalización:

* **Catálogos Maestros:** `Productos_Base`, `Categorias_Modificador`, `Opciones_Modificador`, `Producto_Categoria` (Tabla puente), `Metodo_Pago`.
* **Operaciones:** `Cliente`, `Ventas`, `Comprobante_Voucher`.
* **Detalle Matemático:** `Detalle_Ventas`, `Seleccion_Modificadores`.

---

## 🔧 Instalación y Despliegue Local

Si deseas correr este proyecto en tu entorno local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
