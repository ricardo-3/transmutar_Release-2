# Arbolito

Calculadora móvil de reales a pesos argentinos con cotización manual, estilo ticket y carrusel publicitario. Debajo del ticket muestra los primeros cinco precios de Compara Pix; tocar uno carga su cotización sin calcular automáticamente.

La tabla es una consulta periódica del HTML público, **no una ventana en vivo**. No usa API de cotizaciones ni claves. El workflow de GitHub Actions consulta aproximadamente cada 15 minutos, genera HTML estático y publica en Pages. La hora indica cuándo se leyó la fuente. Si falla la consulta, se conserva la última publicación y el navegador avisa al superar una hora.

## Activación

Leé **ACTIVAR-COTIZACIONES.txt** y **GUIA-GITHUB-Y-BANNERS.txt**. En Settings → Pages elegí **GitHub Actions** como Source. El workflow `.github/workflows/cotizaciones-pages.yml` debe estar en `main`; después ejecutalo desde Actions.

## Desarrollo local

Abrí `index.html` para probar la calculadora. Para consultar precios y generar la web: `python3 scripts/actualizar_pix.py`. El resultado queda en `_site/`. No se requieren paquetes Python externos.

Las imágenes van en `imagenes/`. Tamaño recomendado: **1200 × 400 px**, JPG, WebP o PNG, hasta 200 KB. Configuralas en `const banners` dentro de `index.html`. Conservá tus imágenes al actualizar el proyecto.

Fuente: [Compara Pix](https://comparapix.ar/). Cotizaciones orientativas; confirmá la tasa y condiciones en la billetera antes de pagar.
