# Cómo tener el Embudo, la Escuela y los QRs activos 24/7

## 1. En el Mac de Francis (Acceso directo de Escritorio)
- **Uso inmediato:** Haz doble clic en **`Auto Sanación.app`** en tu Escritorio. Esto inicia el servidor si estaba apagado y abre el **Panel de Francis (Modo Fácil)** en `http://127.0.0.1:8795/admin`.
- **Servicio permanente en este Mac (opcional):** Si quieres que el servidor arranque automáticamente al encender el Mac y se mantenga activo 24/7 mientras el computador esté prendido, ejecuta una sola vez en Terminal:
  ```bash
  bash scripts/install_24_7_service.sh
  ```

## 2. Para que los Códigos QR del libro impreso funcionen en todo el mundo 24/7
Los lectores que escanean un QR desde su celular necesitan acceder a una dirección pública de internet (no a `127.0.0.1`). El proyecto ya incluye un `Dockerfile` listo para desplegar en:
- **Render / Railway / Fly.io / Google Cloud Run** (escucha en `0.0.0.0:8080` con variable `AUTOSANACION_PORT` configurable y base de datos SQLite montable en volumen persistente `/app/data`).
- Una vez publicado en tu dominio (por ejemplo `https://escuela.francisjaramillo.com`), las rutas de los QR del libro quedan activas 24/7:
  - `/qr/contacto` -> Contacto directo por WhatsApp con Francis + acceso a la Escuela.
  - `/qr/cap-1` hasta `/qr/cap-6` -> Clase y ejercicio exacto de cada capítulo + seguimiento.
  - `/qr/resena` -> Invitación ética a dejar reseña verificada en Amazon.
