# New Life Furniture — Rediseño web (entrega)

Sitio estático (HTML/CSS/JS, sin framework). Contenido en `build.py` → `python3 build.py` regenera todas las páginas, `sitemap.xml` y `robots.txt`.
Vista local: `python3 -m http.server 8765 -d new-life-furniture`.

## 1. Auditoría del sitio actual (Squarespace)
- **Dirección confirmada por el cliente (oct 2026):** 380 NE 56th St, Unit 380, Miami, FL 33137 — ya aplicada.
- **Datos inconsistentes (resuelto):** el home dice "380 NE 56th St … Miami, FL **34136**" (ZIP de Bonita Springs); el footer dice "382 N.E. 56th St, #380, Miami, FL 33137". Usé el del footer. **Confirmar con el cliente y con su Google Business Profile.**
- Copy de **Marine** describe "marine-inspired décor" (decoración), no tapicería náutica → mala coincidencia con búsquedas "marine upholstery".
- Booths & Banquettes, Refinishing y Fabrics solo existen como tarjetas del home; no hay página para anunciar booths.
- Títulos terminan en "— nlf"; `/services-comercial-residential` duplica `/upholstery-re-upholstery` (contenido duplicado).
- Página `/cart` indexable sin tienda. Testimonios sin nombre/fuente. Sin FAQ, sin proceso, sin schema LocalBusiness.
- Hero sin propuesta clara ni prueba de confianza; formulario solo en contacto.
- Ya existe GTM `GTM-NW3P7QNL` y Google Ads `AW-17105831863` (reutilizados, no inventados).
- **Los nombres de archivo de Squarespace no coinciden con lo que muestran las fotos** (p. ej. "draperies" mostraba cojines morados). Revisé cada foto visualmente; el dict `ALT` en `build.py` describe lo que realmente muestra cada una y define dónde se usa. Eliminé dos fotos sin relación (paneles rojos perforados, muestras de tela).
- **Imagen "AboutUs" es generada con IA**; el cliente la quiere y se usa solo en /about/ como imagen ilustrativa (alt genérico, no se presenta como proyecto real). No usarla en galerías ni anuncios.
- ~~Imagen "AboutUs" parece stock/IA~~ (artesano genérico) → la quité. Revisar con el cliente que **todas** las fotos sean proyectos reales suyos.

## 2. Estructura (URLs antiguas conservadas para no perder SEO)
| URL | Propósito / keyword |
|---|---|
| `/` | Home: furniture reupholstery Miami |
| `/upholstery-re-upholstery/` | Reupholstery residencial + refinishing (#refinishing) |
| `/commercial/` | Commercial upholstery Miami |
| `/booths-banquettes/` | **Nueva** – restaurant booths / banquettes |
| `/marine/` | Marine upholstery Miami (copy reescrito) |
| `/outdoor-cushions/` | Custom outdoor / patio cushions |
| `/draperies/` | Custom draperies Miami |
| `/projects/` | Galería por categoría |
| `/about/` | Nueva |
| `/contact-new-life-furniture-miami/` | Estimado |
| `404.html` | noindex, con enlaces útiles |

Refinishing y Fabrics no tienen página propia (contenido insuficiente → evitar páginas delgadas). `_redirects` (formato Netlify/Cloudflare Pages) incluye 301 de `/services-comercial-residential` y `/cart`.

## 3. Qué incluye cada landing (Google Ads)
H1 alineado a la búsqueda · formulario corto arriba (con el servicio preseleccionado) · teléfono visible · fotos del servicio · proceso · FAQ · testimonios · servicios relacionados · CTA final. Barra fija "Call now / Free estimate" en móvil.

## 4. SEO técnico implementado
Title + meta description únicos, 1 H1 por página (verificado), canonical, OG, breadcrumbs, JSON-LD (`HomeAndConstructionBusiness`, `WebSite`, `BreadcrumbList`, `Service`, `FAQPage`) — sin ratings inventados. `sitemap.xml`, `robots.txt`. Imágenes WebP en 2 tamaños con `srcset`, `width/height` (sin CLS), lazy-load excepto hero (preload + `fetchpriority=high`).

## 5. Tracking (dataLayer → GTM)
| Evento | Cuándo | Estado |
|---|---|---|
| `click_call` (+`click_location`) | clic en cualquier `tel:` | implementado |
| `click_email` | clic en `mailto:` | implementado |
| `click_whatsapp` | clic en el botón flotante de WhatsApp ((954) 895-8504, confirmado) | implementado |
| `generate_lead` (`form_service`, `project_type`) | **solo** tras respuesta OK del backend; 1 por página | implementado, requiere backend |
- gclid/gbraid/wbraid se guardan 90 días y viajan como campos ocultos del formulario.
- No se envían datos personales a analytics.
- **Pendiente en GTM:** crear triggers de evento personalizado para estos 3 eventos → etiquetas GA4 y conversión de Google Ads (label existente `AW-17105831863/Vp8DCKfP5eEaELeP2dw_`; confirmar a qué acción corresponde). Call tracking de Ads: configurar en la cuenta. Nada de esto se probó en vivo.

## 6. Formulario — PENDIENTE para que funcione
Sin backend configurado, el formulario abre el correo del visitante (no cuenta como conversión). Para activarlo:
1. Crear form en formspree.io con destino **Ian@newlifefurniture.com** (confirmar con el cliente).
2. Poner el ID en `FORMSPREE_ID` en `build.py` → `python3 build.py`.
3. Enviar una prueba y verificar `generate_lead` en GTM Preview.
Incluye validación accesible, honeypot anti-spam, estados de carga/éxito/error. (Validación del lado servidor la hace Formspree.)

## 7. QA realizado
- ✅ 11 páginas, 37 enlaces internos e imágenes → 0 rotos. JSON-LD parsea en todas. 1 H1 por página.
- ✅ Desktop 1440 y móvil 375: sin scroll horizontal, menú móvil (abre/cierra, Escape), validación de formulario con foco y mensajes.
- ✅ Consola sin errores.
- ⚠️ **No medido:** Lighthouse / Core Web Vitals (correr PageSpeed Insights tras publicar), validación en Rich Results Test, prueba en Safari iOS real, envío real del formulario.
- Peso: HTML home 21 KB, CSS 13 KB, JS 5 KB, 1 fuente Google (2 familias).

## 8. Pendientes / dependencias
1. Confirmar dirección/ZIP, horario, área exacta de servicio, si hay pick-up/delivery y la promesa de "free estimate".
2. Confirmar autenticidad de fotos; pedir fotos reales antes/después y del taller/equipo.
3. Nombres (o iniciales) y fuente de los testimonios; enlace al perfil de Google.
4. Backend del formulario (sección 6) y configuración GTM (sección 5).
5. Hosting: el sitio actual es Squarespace. Publicar en Netlify/Cloudflare Pages (staging primero), luego apuntar DNS **solo con autorización**. Squarespace no permite subir HTML propio.
6. Tras el lanzamiento: enviar sitemap en Search Console y monitorear 404s.

## 9. Roadmap 90 días (orgánico)
- **Días 1–30:** lanzamiento, Search Console, GBP (categorías, fotos semanales, servicios con los mismos nombres de las landings), pedir reseñas a clientes recientes, citaciones NAP consistentes (Yelp, Houzz, BBB).
- **Días 31–60:** artículos: "Reupholster vs. replace: when it's worth it" → /upholstery-re-upholstery/; "Best fabrics for Florida outdoor cushions" → /outdoor-cushions/; "Restaurant booth reupholstery: what affects cost" → /booths-banquettes/. Casos de estudio con fotos antes/después.
- **Días 61–90:** analizar consultas en Search Console, ampliar páginas con impresiones altas y CTR bajo; landings por ciudad solo si hay demanda real y contenido único (p. ej. proyectos en Fort Lauderdale). Revisar términos de búsqueda de Ads y alinear headlines.

## 10. Angi (activo de confianza principal)
- Sello **Angi Super Service Award 2025** en: hero (grande en desktop, en la fila de confianza en móvil), cada landing, CTA final y footer. `award` en el schema.
- **Pendiente:** URL del perfil de Angi → `BIZ["angi"]` en `build.py`. Con eso, todos los sellos enlazan al perfil ("Read our Angi reviews") y se agrega a `sameAs` del schema.
- Pedir al cliente: rating y número de reseñas reales de Angi (para mostrarlos como texto, nunca como estrellas en schema), y 3–5 reseñas de Angi para reemplazar/ampliar testimonios con atribución "via Angi".
- No usar `AggregateRating` con reseñas de terceros (Google no lo muestra para negocios propios y puede considerarse marcado engañoso).
