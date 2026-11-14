# Playbook Estratégico — *Auto Sanación* (Francis Jaramillo)

## 1. Posicionamiento Único
- **Obra:** *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar* (ISBN-13 `979-8403609579`, Kindle, Tapa blanda, Audible).
- **Autora:** Francis Jaramillo — psicóloga, terapeuta en medicina integrativa, consejera y especialista en teoterapia familiar.
- **Gancho emocional + credibilidad clínica:** Combina formación psicológica y terapia integrativa con una historia real de superación frente a un diagnóstico de cáncer durante el embarazo.

## 2. Los 4 Motores de Crecimiento en Amazon
1. **Motor 1 — Conversión de Ficha (CRO):** Antes de pagar por tráfico, la página de Amazon debe convertir visitas en compras: descripción HTML estructurada (dolor → historia → beneficios → credibilidad → CTA), Contenido A+ visual (módulos de comparación, historia de la autora y ejercicios del libro), Amazon Author Central completo y alineación de precio entre Kindle / Paperback / Audible.
2. **Motor 2 — Visibilidad Orgánica (SEO KDP):** 7 casillas de backend keywords aprovechando el máximo de 50 bytes UTF-8 por casilla sin repetir palabras del título ni del autor, y selección de categorías con competencia alcanzable para sostener etiquetas *Best Seller* en nichos clave.
3. **Motor 3 — Amazon Ads Rentable (PPC):** Arquitectura de 4 campañas:
   - `SP_Auto_Discovery`: descubrimiento de términos y ASINs con puja conservadora.
   - `SP_Exact_Core`: palabras clave de alta intención en español (ej. *sanacion emocional*, *autosanacion libro*, *psiconeuroinmunologia*, *sanar cuerpo y mente*).
   - `SP_Broad_Research`: investigación controlada de frases largas.
   - `SP_ASIN_Competitors`: segmentación directa en páginas de libros complementarios de sanación emocional, bioneuroemoción, resiliencia y salud integrativa.
4. **Motor 4 — Tráfico Externo + Reseñas (Flywheel):** Videos cortos (Reels/TikTok/Shorts) desde la voz experta de psicóloga apuntando con **Amazon Attribution** (para recibir el *Brand Referral Bonus* y señal positiva al algoritmo A9/A10 de Amazon), más flujo ético de reseñas al final del libro y en listas de correo.

## 3. Cadencia Semanal del Sistema Orquestado
- **Lunes:** Descargar CSV de KDP y Search Term Report de Amazon Ads → ejecutar `ads_analyzer.py` y `kdp_sales_tracker.py`.
- **Martes:** Subir `bulk_negatives.csv` a Amazon Ads y promover términos ganadores a `SP_Exact_Core`.
- **Miércoles–Viernes:** Publicar 3–4 piezas de contenido corto (guiones de `content-funnel-agent`) + enviar 1 correo/historia con enlace Amazon Attribution.
- **Domingo:** `analytics-agent` consolida BSR, TACoS, unidades y define el experimento A/B de la siguiente semana.
