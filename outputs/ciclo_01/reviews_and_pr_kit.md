# Kit de Reseñas Verificadas, Embudo Post-Lectura y Prensa — *Auto Sanación*

**Obra:** *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar*  
**Autora:** Francis Jaramillo (Francis Andrea Jaramillo Jacded)  
**Credenciales:** Psicóloga, terapeuta en medicina integrativa, consejera y especialista en teoterapia familiar  
**Editorial / ISBN-13 (Tapa blanda):** Independently published · `979-8403609579`  
**Formatos:** Kindle, Tapa blanda (Paperback) y Audiolibro (Audible)  
**Mercados prioritarios:** Amazon.com (US Hispanic), Amazon.es, Amazon.com.mx  

> [!IMPORTANT]
> **Variables pendientes de completar antes de maquetar o enviar:**  
> Según [`config/book_profile.json`](../../config/book_profile.json), sustituye los marcadores `[ASIN_KINDLE]`, `[ASIN_PAPERBACK]`, `[ASIN_AUDIBLE]`, `[URL_WEB]`, `[INSTAGRAM]`, `[TIKTOK]`, `[YOUTUBE]` y `[EMAIL_CONTACTO]` por los enlaces reales antes de publicar la versión final.

---

## 1. Flujo Post-Lectura (Final del Libro) + Diseño de Embudo QR (100% Conforme a Amazon)

### 1.1 Reglas de Cumplimiento Obligatorio (Amazon Customer Reviews Policy)
Para proteger la cuenta KDP de Francis Jaramillo y evitar la eliminación de reseñas o sanciones:
1. **Cero incentivos por reseñar:** Nunca se ofrece un regalo, PDF, meditación, descuento ni consulta a cambio de dejar una reseña. Si se ofrece un recurso gratuito de acompañamiento, debe entregarse **de forma incondicional** por suscribirse a la comunidad o como regalo abierto del libro, completamente separado de la petición de reseña.
2. **Cero *review gating* (reseñas condicionadas):** Nunca escribir *"si te gustó, déjanos una reseña; si no, escríbenos por privado"*. La invitación debe ser idéntica para todos los lectores.
3. **Cero solicitud de calificación específica:** Pedir siempre una **"reseña honesta"** o **"tu opinión genuina"**, nunca pedir "5 estrellas" ni "una reseña positiva".
4. **Reseñas de conocidos y familiares:** Amazon prohíbe las reseñas de familiares directos o personas con conflicto de interés financiero. Las invitaciones deben dirigirse a lectores reales que hayan adquirido o leído la obra de forma legítima.

---

### 1.2 Arquitectura del Embudo Post-Lectura con Código QR

El diseño separa **dos acciones independientes** para maximizar tanto la lista de correos como las reseñas verificadas sin violar las políticas de Amazon:

```text
[Última página del libro: Kindle (enlace) / Tapa blanda (QR)]
         │
         ├──► VÍA A (Reseña directa): Enlace/QR directo a Amazon Create Review
         │      └─ El lector deja su reseña honesta en su tienda (.com / .es / .com.mx)
         │
         └──► VÍA B (Captación de correo sin condiciones): QR / Enlace a Landing de Acompañamiento
                └─ Formulario simple (Nombre + Email) → Entrega inmediata del "Cuaderno / Audio de Calma"
                     │
                     ├─► Correo Día 0: Entrega del recurso prometido (0 mención a reseñas)
                     └─► Correo Día 7: Seguimiento de lectura + invitación separada y voluntaria a reseñar
```

#### Especificaciones Técnicas del Embudo QR
- **Destino del QR de Captación (Vía B):** Página limpia en `[URL_WEB]/acompanamiento` (o página de aterrizaje del proveedor de email `[EMAIL_PROVIDER]`).
  - **Título sugerido de la landing:** *"Recursos de acompañamiento para tu proceso de autosanación"*
  - **Lead magnet recomendado (coherente con el libro):** *Guía práctica de 7 días: Respiración, regulación emocional y oración/reflexión integrativa (PDF + Audio corto)* — **100% gratuito al suscribirse, sin pedir nada más**.
- **Destino del enlace/QR de Reseña (Vía A):** Enlace universal o selector por país que apunte directamente al formulario de reseña de Amazon:
  - **Amazon.com (EE. UU.):** `https://www.amazon.com/review/create-review?asin=[ASIN_KINDLE_O_PAPERBACK]`
  - **Amazon.es (España):** `https://www.amazon.es/review/create-review?asin=[ASIN_KINDLE_O_PAPERBACK]`
  - **Amazon.com.mx (México):** `https://www.amazon.com.mx/review/create-review?asin=[ASIN_KINDLE_O_PAPERBACK]`
  - *Tip técnico para Tapa blanda:* Si no deseas imprimir 3 URLs largas en papel, crea un enlace corto propio (ej. `[URL_WEB]/resena`) con botones para los 3 países (*Estados Unidos / Latinoamérica*, *España*, *México*) que redirijan a los enlaces oficiales `create-review`.

---

### 1.3 Texto Listo para Insertar al Final del Libro — Versión Kindle (eBook)

> **Instrucción de maquetación (Kindle):** Insertar en una página nueva inmediatamente después del capítulo final o epílogo. Convertir los textos entre corchetes en hipervínculos clicables.

```markdown
---
## Gracias por caminar estas páginas conmigo

Leer *Auto Sanación* no es solo terminar un libro; es abrir una conversación honesta con tu cuerpo, tu mente y tu espíritu. Cuando atravesé el diagnóstico de cáncer durante mi embarazo, comprendí que la sanación integral comienza cuando dejamos de luchar contra nosotros mismos y empezamos a activar los recursos que ya habitan en nuestro interior.

Si este libro te acompañó, te dio claridad o sembró esperanza en medio de un momento difícil, quiero pedirte dos cosas muy sencillas:

### 1. Comparte tu reseña honesta en Amazon
Las reseñas de lectores reales ayudan a que otras personas que hoy buscan respuestas, consuelo o herramientas prácticas encuentren este libro en el momento que más lo necesitan. No importa si tu comentario es breve: dos o tres líneas sinceras sobre lo que más te sirvió marcan una enorme diferencia.

👉 **[Dejar mi reseña honesta en Amazon.com (EE. UU. / Internacional)](https://www.amazon.com/review/create-review?asin=[ASIN_KINDLE])**  
👉 **[Dejar mi reseña honesta en Amazon.es (España)](https://www.amazon.es/review/create-review?asin=[ASIN_KINDLE])**  
👉 **[Dejar mi reseña honesta en Amazon.com.mx (México)](https://www.amazon.com.mx/review/create-review?asin=[ASIN_KINDLE])**

*(Tu opinión es completamente voluntaria y personal; valorar con sinceridad lo que viviste con estas páginas es el mayor aporte que puedes hacer a futuros lectores).*

---

### 2. Sigue profundizando: accede gratis a la comunidad y recursos de acompañamiento
Si deseas continuar integrando lo que leíste en tu día a día, he preparado un espacio gratuito para nuestra comunidad donde comparto herramientas prácticas de psicología integrativa, regulación emocional y bienestar integral.

👉 **[Quiero recibir mis recursos gratuitos de acompañamiento aquí]([URL_WEB]/acompanamiento)**

También podemos seguir en contacto en:
- Instagram: `[INSTAGRAM]`
- YouTube: `[YOUTUBE]`
- TikTok: `[TIKTOK]`
- Web oficial: `[URL_WEB]`

Con gratitud y esperanza,  
**Francis Jaramillo**  
*Psicóloga y terapeuta en medicina integrativa*
---
```

---

### 1.4 Texto Listo para Insertar al Final del Libro — Versión Tapa Blanda (Paperback)

> **Instrucción de maquetación (Papel — ISBN `979-8403609579`):** En libro impreso el lector no puede hacer clic. Usa **tipografía limpia**, márgenes amplios y **dos bloques visuales diferenciados** con códigos QR de alto contraste (mínimo 2,5 cm × 2,5 cm en negro sobre fondo blanco) y URL corta legible debajo de cada QR.

```markdown
---
## Una invitación antes de cerrar este libro

Gracias por permitir que *Auto Sanación* entre en tu vida y en tu hogar. Cuando enfrenté el cáncer durante mi embarazo, descubrí que el conocimiento profesional cobra sentido solo cuando se vuelve un puente de esperanza y acción cotidiana para el cuerpo, la mente y el alma.

### ¿Te gustaría ayudar a que este mensaje llegue a quien hoy lo necesita?
Las opiniones sinceras de los lectores son la mejor guía para quienes están buscando herramientas reales de sanación emocional y bienestar integral. Si deseas compartir tu experiencia honesta con el libro, solo toma un minuto:

┌───────────────────────────────────────────────┐
│  [ CÓDIGO QR #1: RESEÑA HONESTA EN AMAZON ]   │
│                                               │
│  Escanea con la cámara de tu teléfono o       │
│  visita: [URL_WEB]/resena                     │
│  (Elige tu tienda: Amazon.com / .es / .mx)    │
└───────────────────────────────────────────────┘

*Agradecemos cualquier opinión genuina y honesta sobre tu lectura.*

---

### Lleva la práctica a tu día a día (Recurso gratuito de la autora)
Como parte de mi compromiso con acompañarte más allá de estas páginas, puedes suscribirte gratis a mi boletín para recibir ejercicios prácticos de regulación mente-cuerpo, reflexiones de teoterapia familiar y novedades de próximos encuentros.

┌───────────────────────────────────────────────┐
│  [ CÓDIGO QR #2: RECURSOS Y COMUNIDAD ]       │
│                                               │
│  Escanea para recibir el material gratuito:   │
│  [URL_WEB]/acompanamiento                     │
└───────────────────────────────────────────────┘

Encuéntrame también en redes sociales:  
Instagram: `[INSTAGRAM]` · YouTube: `[YOUTUBE]` · Web: `[URL_WEB]`

Con todo mi cariño,  
**Francis Jaramillo**  
*Psicóloga, terapeuta en medicina integrativa y especialista en teoterapia familiar*
---
```

### 1.5 Secuencia Breve de Correo Post-Opt-In (Embudo QR — Vía B)
Para mantener la separación ética entre el regalo de bienvenida y la reseña:
- **Email 1 (Inmediato al registrarse vía QR #2):** Asunto: *"Aquí tienes tu guía de acompañamiento — Auto Sanación"*. Entrega el enlace al recurso descargable, da la bienvenida a la comunidad de Francis Jaramillo y presenta un ejercicio corto aplicable hoy. **No pide reseña.**
- **Email 2 (Día +7 tras el registro):** Asunto: *"¿Cómo vas con tu proceso? + Un pequeño favor"*. Pregunta cómo le fue con el recurso de acompañamiento y, al final, incluye una invitación separada y sin incentivos: *"Si ya terminaste de leer Auto Sanación y quieres dejar tu opinión honesta en Amazon para ayudar a otros lectores a descubrirlo, puedes hacerlo aquí: [Enlaces Amazon .com / .es / .com.mx]"*.

---

## 2. Secuencia de 2 Mensajes (WhatsApp y Correo) para Lectores Actuales, Pacientes y Comunidad

> [!WARNING]
> **Nota importante sobre reseñas verificadas y conflicto de interés:**  
> 1. **Compra Verificada (*Verified Purchase*):** Envíalo priorizando a quienes sabes que **compraron el libro en Amazon** (Kindle, Tapa blanda o Audible). Las reseñas de compradores reales tienen mayor peso algorítmico y muestran la insignia de *Compra verificada*.  
> 2. **Ética clínica y políticas de Amazon:** En el caso de **pacientes actuales**, evita cualquier tono de obligación terapéutica o intercambio de favores. Aclara explícitamente que es una invitación voluntaria, que no tiene relación con su proceso terapéutico y que **no deben participar familiares directos ni personas vinculadas comercialmente al libro**, ya que Amazon puede bloquear esas reseñas.  
> 3. **Personaliza** los campos entre corchetes `[Nombre]`, `[ASIN]` y enlaces antes de enviar.

---

### Mensaje 1 (Día 1): Invitación Cercana y Honesta

#### Versión A — WhatsApp (Lectores / Comunidad / Ex-pacientes o Pacientes)
> Hola `[Nombre]`, ¿cómo estás? Te saluda Francis Jaramillo 🌿
>
> Te escribo con mucha ilusión porque *Auto Sanación* está llegando a nuevas personas que están atravesando momentos difíciles de salud o búsqueda emocional, y quiero pedirte un apoyo muy puntual si ya tuviste oportunidad de leerlo (o de avanzar en sus capítulos).
>
> En Amazon, las **reseñas honestas de lectores reales** son lo que permite que el algoritmo recomiende el libro a quienes buscan herramientas de sanación mente-cuerpo y esperanza. Si compraste tu ejemplar en Amazon y el libro te aportó algo valioso (o tienes una reflexión sincera sobre tu lectura), ¿me apoyarías dejando una reseña breve de 2 o 3 líneas?
>
> Puedes hacerlo directo aquí según tu tienda:
> - EE. UU. / Internacional: https://www.amazon.com/review/create-review?asin=[ASIN_DEL_FORMATO]
> - España: https://www.amazon.es/review/create-review?asin=[ASIN_DEL_FORMATO]
> - México: https://www.amazon.com.mx/review/create-review?asin=[ASIN_DEL_FORMATO]
>
> *(Por supuesto, es 100 % voluntario y sin ningún compromiso; solo tu opinión genuina).*
>
> ¡Muchas gracias por ser parte de este camino! Un abrazo enorme.

#### Versión B — Correo Electrónico (Comunidad / Lista de Lectores)
- **Asunto:** Un pequeño favor si ya leíste *Auto Sanación* 🌿
- **Preheader:** Tu experiencia honesta puede ayudar a otra persona a encontrar esperanza hoy.

```text
Hola [Nombre],

Espero que estés teniendo una semana serena y con bienestar.

Quiero agradecerte de corazón por haber adquirido o leído "AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar". Escribir este libro nació de una convicción profunda tras superar un cáncer durante mi embarazo y ver, día a día en consulta, la capacidad de transformación que existe cuando integramos cuerpo, mente y espíritu.

Hoy te escribo con una petición sencilla y completamente voluntaria:

Si adquiriste el libro en Amazon y ya pudiste leerlo (o al menos sus primeros capítulos), ¿considerarías dedicar 2 minutos a dejar una reseña honesta en Amazon?

¿Por qué es tan importante?
En Amazon, las opiniones genuinas de lectores con compra verificada ayudan a que el libro sea visible para personas y familias que hoy están buscando respuestas, contención emocional y herramientas prácticas para su proceso de sanación.

No hace falta escribir algo largo; unas pocas líneas sinceras sobre lo que más te resonó o te resultó útil marcan una gran diferencia.

Elige tu tienda de Amazon para dejar tu reseña:
• Amazon.com (EE. UU. / Internacional): https://www.amazon.com/review/create-review?asin=[ASIN_DEL_FORMATO]
• Amazon.es (España): https://www.amazon.es/review/create-review?asin=[ASIN_DEL_FORMATO]
• Amazon.com.mx (México): https://www.amazon.com.mx/review/create-review?asin=[ASIN_DEL_FORMATO]

(Nota: Si aún no lo terminas, guárdate este correo para cuando sientas que es tu momento. Tu opinión es totalmente libre y no existe ningún tipo de incentivo asociado, únicamente el deseo de llegar a más vidas).

Gracias por caminar conmigo y por ayudar a que este mensaje siga creciendo.

Con gratitud,
Francis Jaramillo
Psicóloga | Terapeuta en Medicina Integrativa | Especialista en Teoterapia Familiar
[URL_WEB] | [INSTAGRAM]
```

---

### Mensaje 2 (Día 5–7): Recordatorio Breve de Seguimiento (Solo a Quienes No Han Respondido)

#### Versión A — WhatsApp (Seguimiento corto y respetuoso)
> Hola `[Nombre]`, espero que estés muy bien ✨
>
> Te paso un mensajito breve de seguimiento por si se te quedó abajo mi mensaje anterior. Si llegaste a tener un par de minutos esta semana y quieres compartir tu **reseña honesta** de *Auto Sanación* en Amazon, aquí te dejo nuevamente el enlace directo para ahorrar tiempo:
>
> 👉 `[ENLACE_CORTO_O_AMAZON_CREATE_REVIEW]`
>
> Y si aún no lo terminas o estás muy ocupado/a estos días, no te preocupes en absoluto, tómate tu tiempo. ¡Te mando un abrazo grande y gracias siempre por tu apoyo!

#### Versión B — Correo Electrónico (Seguimiento)
- **Asunto:** Solo 2 minutos: ¿me ayudas con tu opinión de *Auto Sanación*?
- **Preheader:** Un recordatorio breve (sin presión) por si se te pasó el correo anterior.

```text
Hola [Nombre],

Te escribo rápidamente para hacer un breve seguimiento de mi mensaje de hace unos días, porque sé lo rápido que pasan las semanas.

Si ya terminaste (o estás leyendo) "AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar" y te nace compartir tu opinión sincera en Amazon, tu reseña ayuda muchísimo a que el libro llegue a más mujeres, madres, pacientes y familias que buscan un enfoque integral para recuperar su bienestar.

Solo toma un par de minutos y puedes hacerla desde el enlace de tu país:
• Amazon.com: https://www.amazon.com/review/create-review?asin=[ASIN_DEL_FORMATO]
• Amazon.es: https://www.amazon.es/review/create-review?asin=[ASIN_DEL_FORMATO]
• Amazon.com.mx: https://www.amazon.com.mx/review/create-review?asin=[ASIN_DEL_FORMATO]

¿No sabes qué escribir? Basta con responder brevemente una de estas ideas:
1. ¿Qué capítulo o herramienta práctica te ayudó más?
2. ¿A quién le recomendarías este libro?

Si en este momento no puedes hacerlo o aún estás leyendo el libro, por favor no sientas ninguna presión. Agradezco muchísimo que formes parte de esta comunidad.

Un abrazo con cariño,
Francis Jaramillo
[URL_WEB]
```

---

## 3. Media Kit / One-Pager de Prensa — Francis Jaramillo

*(Diseñado como hoja informativa lista para exportar a PDF de 1–2 páginas o pegar en Notion/Google Docs para enviar a periodistas, productores y anfitriones de podcasts).*

---

### MEDIA KIT OFICIAL | FRANCIS JARAMILLO
**Autora · Psicóloga · Terapeuta en Medicina Integrativa · Sobreviviente de Cáncer en el Embarazo**

#### Ficha Técnica del Libro
- **Título:** *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar*
- **Autora:** Francis Jaramillo (Francis Andrea Jaramillo Jacded)
- **Formatos disponibles:** Kindle, Tapa blanda (ISBN-13: `979-8403609579`) y Audiolibro (Audible)
- **Editorial:** Independently published
- **Temática:** Psicología integrativa, bienestar emocional, conexión mente-cuerpo, psiconeuroinmunología práctica, espiritualidad y resiliencia ante la adversidad.
- **Dónde conseguirlo:** Amazon.com, Amazon.es y Amazon.com.mx (`[ENLACE_UNIVERSAL_LIBRO]`)

#### Contacto de Prensa y Entrevistas
- **Correo para prensa / podcasts:** `[EMAIL_CONTACTO]`
- **Sitio web:** `[URL_WEB]`
- **Redes sociales:** Instagram `[INSTAGRAM]` · YouTube `[YOUTUBE]` · TikTok `[TIKTOK]`
- **Disponibilidad:** Entrevistas en vivo o grabadas (audio/video), colaboraciones editoriales y charlas en español.

---

### Biografías Listas para Publicar (Copiar y Pegar)

#### Biografía Corta (para intros de podcast y notas breves — ~70 palabras)
> **Francis Jaramillo** es psicóloga, terapeuta en medicina integrativa, consejera y especialista en teoterapia familiar. Tras recibir un diagnóstico de cáncer durante su embarazo, eligió transitar un camino integrativo de sanación física, mental y espiritual que transformó su práctica clínica y su vida. Es autora del libro *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar*, una guía práctica y testimonial sobre cómo activar los recursos biológicos, emocionales y espirituales para recuperar el bienestar integral.

#### Biografía Larga (para dosieres de prensa y páginas de eventos — ~185 palabras)
> **Francis Andrea Jaramillo Jacded** (conocida como **Francis Jaramillo**) es psicóloga, terapeuta en medicina integrativa, consejera y especialista en teoterapia familiar. Su trabajo se centra en acompañar a personas, mujeres y familias a comprender el diálogo profundo entre la salud emocional, la biología del cuerpo y la dimensión espiritual.
>
> Su enfoque clínico dio un giro decisivo cuando enfrentó una de las pruebas más extremas que puede vivir una mujer: recibir un diagnóstico de cáncer durante el embarazo. Lejos de limitarse a la teoría, Francis tuvo que poner a prueba en carne propia sus herramientas profesionales, eligiendo un proceso de sanación integrativo que unió el acompañamiento médico con la regulación emocional, la resiliencia mental y la fe.
>
> Fruto de esa vivencia y de su experiencia terapéutica nace su libro *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar* (disponible en Amazon en formato Kindle, tapa blanda y audiolibro). En él, Francis ofrece una hoja de ruta accesible y compasiva para que cualquier lector —atraviese o no una crisis de salud— descubra los recursos intrínsecos que posee para sanar su cuerpo, su mente y su alma.

---

### 5 Temas de Entrevista (Ángulos de Alto Valor para Medios y Podcasts)

1. **Cáncer durante el embarazo: cómo sostener la mente cuando el diagnóstico llega en el momento más vulnerable**
   - *Enfoque:* El impacto psicológico de recibir una noticia extrema mientras se gesta vida; cómo gestionar el miedo, evitar el colapso emocional y tomar decisiones desde la calma y no desde el pánico.
2. **Tu cuerpo no es tu enemigo: qué es la autosanación integrativa (y qué NO es)**
   - *Enfoque:* Desmitificar la "positividad tóxica". Explicar desde la psicología y la medicina integrativa cómo el sistema nervioso, las emociones reprimidas y los pensamientos influyen en los procesos de recuperación física, complementando el cuidado médico.
3. **La tríada cuerpo–mente–alma: recursos biológicos, emocionales y espirituales que ya llevamos dentro**
   - *Enfoque:* Herramientas prácticas del libro para pasar de la supervivencia al equilibrio: regulación emocional cotidiana, manejo del estrés crónico y el papel de la espiritualidad/teoterapia en la salud familiar.
4. **Sanar en familia cuando uno de sus miembros enferma o atraviesa una crisis**
   - *Enfoque:* Desde su especialidad en teoterapia familiar y consejería: cómo acompañar a un ser querido sin anularlo, cómo pedir ayuda y cómo transformar una crisis de salud en un vínculo familiar más sano.
5. **De paciente a terapeuta transformada: lecciones de resiliencia para mujeres y madres que sienten que "no pueden con todo"**
   - *Enfoque:* Conversación íntima sobre maternidad, culpa, sobrecarga mental y reconstrucción personal tras una tormenta vital.

---

### Preguntas Sugeridas para el/la Anfitrión/a

1. *Francis, eres psicóloga y terapeuta en medicina integrativa, pero tu libro nace también de una historia muy personal. ¿Cómo fue el momento en que recibiste el diagnóstico de cáncer estando embarazada y qué pasó por tu mente en esas primeras horas?*
2. *Como profesional de la salud mental, ¿qué herramientas clínicas te sirvieron en ese momento y cuáles sentiste que la teoría por sí sola no alcanzaba a cubrir?*
3. *El título de tu libro habla de que "tu cuerpo tiene los recursos para sanar". A veces en redes sociales se banaliza este tema con frases vacías: desde tu enfoque integrativo, ¿qué significa realmente la autosanación?*
4. *¿Cómo se conectan nuestras heridas emocionales o el estrés sostenido con la respuesta biológica del cuerpo?*
5. *En tu práctica combinas psicología, medicina integrativa y teoterapia familiar. ¿Qué papel juega la dimensión espiritual o de fe en la recuperación emocional y física?*
6. *Muchas personas que escuchan este episodio quizá están acompañando a un familiar enfermo o atravesando un duelo de salud. ¿Qué error cometemos al intentar "animar" a alguien en crisis y qué sí funciona para acompañarlo?*
7. *Para una mujer o madre que hoy siente agotamiento físico y emocional, ¿cuál es un primer paso práctico de tu libro que pueda aplicar hoy mismo en 10 minutos?*
8. *Si alguien pudiera quedarse con una sola idea después de escuchar esta charla y leer "Auto Sanación", ¿cuál te gustaría que fuera?*

---

## 4. Plantilla de Pitch para Podcasts de Psicología, Bienestar y Maternidad en Español

### 4.1 Plantilla Base (Lista para Copiar, Personalizar y Enviar por Email o DM)

**Asunto (elegir 1 según el tono del programa):**
- Opción A (Historia + Autoridad): `Propuesta de entrevista: Psicóloga sobreviviente de cáncer en el embarazo | Libro "Auto Sanación"`
- Opción B (Beneficio para la audiencia): `Idea de episodio para [Nombre del Podcast]: Qué ocurre en la mente y el cuerpo cuando sanamos desde adentro`
- Opción C (Directa): `Invitada experta en psicología integrativa y resiliencia — Francis Jaramillo`

**Cuerpo del correo:**

```text
Hola [Nombre del/de la anfitrión/a],

Te saludo con mucho cariño. Sigo [Nombre del Podcast] desde hace tiempo y disfruté muchísimo el episodio sobre [mencionar tema o episodio reciente real, ej. "cómo gestionar la ansiedad en la maternidad" / "salud integral"] —especialmente cuando mencionaste [detalle breve de 1 línea que demuestre que escuchaste el programa].

Te escribo porque creo que tu audiencia conectaría profundamente con Francis Jaramillo: es psicóloga, terapeuta en medicina integrativa y especialista en teoterapia familiar, además de autora del libro "AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar".

Su historia tiene un puente muy poderoso entre la clínica y la vida real: recibió un diagnóstico de cáncer durante su embarazo y tuvo que aplicar —en carne propia y junto a su familia— un camino integrativo de sanación física, mental y espiritual.

Si te encaja para una próxima temporada, podríamos conversar sobre uno de estos ángulos pensados para tu audiencia:
1. [Elegir 1 de los 3 ganchos adaptados abajo según el nicho del podcast]
2. [Elegir 1 segundo ángulo complementario]

La entrevista sería 100 % práctica, cercana y sin tecnicismos vacíos, para que tus oyentes se lleven herramientas concretas de regulación emocional y esperanza aplicable.

Adjunto su Media Kit / One-Pager con bio, temas y preguntas sugeridas (sin compromiso). Si te resuena, estaré encantada de coordinar fecha según tu calendario.

Un abrazo y felicidades por el trabajo que haces en [Nombre del Podcast],

[Tu Nombre / Equipo de Francis Jaramillo]
En representación de Francis Jaramillo
[EMAIL_CONTACTO] | [URL_WEB] | [INSTAGRAM]
```

---

### 4.2 Bloques Adaptables por Nicho de Podcast (Sustituir en los puntos 1 y 2 del Pitch)

- **Para Podcasts de Psicología y Salud Mental:**
  - *Ángulo 1:* Cómo distinguir entre positivismo tóxico y verdadera regulación emocional basada en el vínculo mente-cuerpo.
  - *Ángulo 2:* Herramientas de consejería y teoterapia familiar para sostener la salud mental cuando llega una crisis médica inesperada.
- **Para Podcasts de Bienestar, Salud Holística y Medicina Integrativa:**
  - *Ángulo 1:* El cuerpo como aliado: cómo activar los recursos biológicos, emocionales y espirituales de autosanación sin abandonar el rigor clínico.
  - *Ángulo 2:* Psiconeuroinmunología aplicada a la vida diaria: hábitos mentales y emocionales que desactivan la respuesta crónica de amenaza.
- **Para Podcasts de Maternidad, Mujeres y Fe/Resiliencia:**
  - *Ángulo 1:* Enfrentar un diagnóstico de cáncer durante el embarazo: cómo transformar el miedo en fuerza interior y esperanza activa.
  - *Ángulo 2:* Cómo sanar como mujer y madre cuando sientes que debes sostener a todos mientras tú también estás rota.

---

### 4.3 Mensaje Corto de Seguimiento (Follow-up a los 5–7 días si no responde)

**Asunto:** `Re: Propuesta de entrevista — Francis Jaramillo ("Auto Sanación")`

```text
Hola [Nombre del/de la anfitrión/a],

¿Cómo va tu semana? Retomo brevemente mi correo anterior por si quedó enterrado entre tus mensajes.

Seguimos con agenda abierta este mes por si te gustaría conversar con Francis Jaramillo (psicóloga integrativa y sobreviviente de cáncer en el embarazo) para [Nombre del Podcast]. Si prefieres un tema distinto al propuesto para ajustarlo a tu próxima serie de episodios, con gusto lo adaptamos.

Gracias por tu tiempo y por el espacio que creas para tu comunidad.

Un saludo cálido,
[Tu Nombre / Francis Jaramillo]
[EMAIL_CONTACTO]
```

---

### 4.4 Checklist Operativo de Envío (Ciclo 01)
- [ ] Completar `asin_kindle`, `asin_paperback`, `asin_audible`, `website` y redes en [`config/book_profile.json`](../../config/book_profile.json).
- [ ] Generar los dos códigos QR de alta resolución (300 DPI, SVG/PNG) para la edición de Tapa blanda (`979-8403609579`) y verificar en móvil antes de subir el PDF interior a KDP.
- [ ] Configurar la landing `[URL_WEB]/acompanamiento` y los dos correos automáticos (Día 0 entrega del recurso; Día +7 invitación separada a reseñar).
- [ ] Enviar Mensaje 1 (WhatsApp y Correo) a primeros lectores con compra verificada; programar Mensaje 2 a los 5–7 días solo para quienes no hayan interactuado.
- [ ] Seleccionar una lista inicial de 15–20 podcasts en español (psicología, bienestar integrativo, maternidad) y enviar el pitch personalizado usando los bloques de la Sección 4.2.
