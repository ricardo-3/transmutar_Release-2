# Transmutar

Transmutar es una pequeña web pensada para el celular: escribís un pensamiento o una emoción que te está pesando, presionás Transmutar emoción, y las palabras se disuelven en partículas de luz que se van con la noche. Al final, un mensaje te recuerda que nombrar el dolor es el primer paso para soltarlo.

## El origen

Este proyecto nació hace un año, en la sala de espera de un hospital, mientras esperaba que operaran a mi esposa. Para sostener esas horas tensas, se me ocurrió esta idea y armé la primera versión 100% con IA.

Desde entonces lo tomo como un proyecto vivo: a medida que la IA y las herramientas avanzan, voy creando nuevas versiones usando las tecnologías que voy descubriendo y que rinden mejor. Esta es una de esas iteraciones.

## Esta versión

El rediseño completo de la interfaz lo hice con IA dentro de Figma (UI + wireframe), y después le pasé ese wireframe a Claude para convertirlo en código. El objetivo fue lograr una estética moderna, calma y "viva", como un jardín mágico de noche.

### Cómo está hecho:

- **HTML + CSS puro** (sin frameworks de estilos): control total sobre la estética.
- **Liquid glass / glassmorphism** en la tarjeta de texto, con paleta tomada del propio fondo para que todo combine.
- **Three.js** para las luciérnagas y partículas que flotan sobre el jardín y le dan movimiento.
- **Tipografía Outfit** y un botón sólido para una lectura clara y un look limpio.
- **Efecto de disgregación**: el texto se convierte en luz que sube y se dispersa al transmutar.

### Optimización del fondo:

La imagen del jardín se convirtió a WebP (~78 KB) y va embebida en el HTML, con un fade-in de entrada desde un verde oscuro. Así carga al instante y sin parpadeo negro.

## Cómo usarlo

Es un único archivo autocontenido. Abrí `index.html` en el navegador, o publicalo con GitHub Pages y entrá desde el celular.

## La idea a futuro

Seguir evolucionando esta misma idea con cada salto de la tecnología. 

Cada versión es una foto del momento: de lo que la IA puede hacer y de lo que estoy aprendiendo. 🌱
