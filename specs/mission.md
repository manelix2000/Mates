# Misión

## Propósito
Aplicación web (SPA) de apoyo al estudio, diseñada para que un estudiante de **4º de ESO (España)**
practique ejercicios de matemáticas de forma autónoma. No es un producto profesional ni comercial:
es una herramienta personal, simple y directa, para reforzar la práctica en casa.

## Usuario objetivo
- Estudiante de 4º ESO (un único perfil, sin cuentas ni autenticación).
- Uso típico desde navegador de escritorio o tablet.

## Idioma
- **Documentación interna / specs:** español (este repositorio).
- **Interfaz de usuario y contenidos (preguntas, opciones, resoluciones):** **catalán**.
  Todo lo que ve el alumno debe estar en catalán.

## Experiencia del usuario
1. Al abrir la app, el estudiante ve un **selector de temas** (en catalán).
2. Selecciona un tema (ej. *Vectors*).
3. Aparece un ejercicio **que no haya hecho antes**, con:
   - Enunciado (texto y, si aplica, un **gráfico** — ej. vectores sobre una cuadrícula).
   - **4 opciones de respuesta**, solo una correcta.
4. El estudiante pulsa **"Comprova"**.
5. La app muestra:
   - Si la respuesta es correcta o incorrecta.
   - La **resolución paso a paso**, explicada de forma muy clara y sencilla, pensada
     para que se entienda sin ayuda externa.
6. Puede pasar al siguiente ejercicio (**"Següent"**).

## Persistencia de progreso
- La app **recuerda qué ejercicios ha hecho ya el alumno** entre sesiones y entre dispositivos.
- El progreso se guarda en el **servidor** (no en el navegador), por lo que es accesible desde
  cualquier navegador que apunte al mismo backend.
- **Modelo de datos compartido y único:** no hay cuentas ni autenticación. Todo el progreso es
  global; cualquier visitante ve y modifica el mismo estado. Es una decisión consciente para
  mantener la app trivial (un único alumno objetivo).
- **Backend:** servidor Node + Express minimalista que persiste en un único fichero JSON
  (`app/server/data/progress.json`) con escritura atómica (rename desde `.tmp`) y un lock
  serie en memoria para evitar carreras entre peticiones concurrentes.
- **API REST:**
  - `GET /api/progress` — devuelve todo el estado.
  - `GET /api/progress/:topicId` — devuelve el progreso de un tema (`{version, answered}`).
  - `POST /api/progress/:topicId/answer` — body `{questionId, correct}`; registra una respuesta.
  - `DELETE /api/progress/:topicId` — resetea el progreso del tema.
  - Validación estricta de `topicId` y `questionId` por regex para evitar inyección de claves.
- **Estructura por tema:** `{ version: 1, answered: { [questionId]: { correct: boolean, at: ISO } } }`.
  Se guarda si la respuesta fue acertada o fallada para poder mostrar estadísticas (bien/mal).
- **Cliente:** caché en memoria + actualización optimista en `markAnswered` (la UI no espera al
  servidor; si la red falla, se registra un `warn` y la sesión sigue funcionando con el caché).
- Al entrar en un tema, la app solo presenta preguntas **pendientes**.
- Cuando no queden preguntas por hacer en un tema:
  - Se muestra un mensaje claro ("Ja has fet tots els exercicis d'aquest tema").
  - Se ofrece un botón **"Tornar a començar"** que **resetea** el progreso del tema
    (pide confirmación para evitar reseteo accidental).
- El alumno puede resetear manualmente el progreso de un tema desde el selector
  (acción explícita, con confirmación).
- En la **home** (selector de temas) se muestra, por cada tema: ejercicios fets (X/25),
  cuántos correctos (✓) y cuántos errados (✗).

## Despliegue y ejecución
- **Desarrollo:** `npm run dev` lanza Vite (cliente) y el servidor Express en paralelo. Vite
  hace proxy de `/api` a `http://localhost:3001`.
- **Producción:** `npm run build && npm start`. El servidor Express sirve también el `dist/`
  estático, así que un único proceso atiende SPA + API en el mismo puerto.

## Formato estándar de temas
Toda la aplicación sigue un **formato uniforme** para cualquier tema existente o futuro:
- **Cada tema contiene exactamente 25 preguntas.** No más, no menos. Esto garantiza una
  carga de trabajo consistente por tema y simplifica la UI (no hay que mostrar progreso variable).
- **Cada pregunta tiene exactamente 4 opciones de respuesta**, con una única correcta.
  Las otras 3 son **distractores pedagógicos** (errores típicos documentados), nunca aleatorios.
- **Las opciones con contenido matemático (raíces, fracciones, exponentes, símbolos) deben
  envolverse en `$...$`** para que KaTeX las renderice correctamente. Texto plano sin notación
  matemática puede ir sin delimitadores. Ejemplo correcto: `"$\\sqrt{161}\\ \\text{cm}$"`.
- **Cada pregunta incluye una resolución paso a paso** en catalán, pensada para que el alumno
  la entienda sin ayuda externa.
- **Temas con contenido geométrico** (triángulos, vectores, figuras planas, etc.) deben incluir:
  - Un **gráfico en el enunciado** (campo `graphic`) que ilustre la figura con los datos conocidos
    y destaque visualmente la incógnita.
  - Un **gráfico final en la resolución** (paso de tipo `graphic`) que muestre la misma figura
    con **todos los valores resueltos**, para cerrar el razonamiento visualmente.
- **Tipos de gráfico soportados** (`graphic.kind`):
  - `vector-plot`: plano con ejes, cuadrícula, puntos y vectores (sumas/restas gráficas).
  - `right-triangle`: triángulo rectángulo con catetos `b`, `c`, altura `h` y proyecciones `m`, `n`
    (teoremas de Pitàgores y altura).
  - `applied-triangle`: triángulo rectángulo **aplicado** con un ángulo agudo α marcado y
    etiquetas libres en hipotenusa, cateto opuesto y cateto adyacente. Pensado para problemas
    de trigonometría (pals, escales, rampes, angles d'elevació/depressió). Acepta también
    etiquetas contextuales en los vértices (`vertexLabels`: terra / extrem / observador…).
  - `shape-plot`: lienzo genérico con `viewBox` lógico y una lista de primitivas
    (`polygon`, `circle`, `arc`, `line`) más etiquetas libres en posiciones absolutas.
    Permite dibujar cualquier figura plana (cuadrados, rectángulos, triángulos, trapecios,
    círculos) y **figuras compuestas** combinando varias primitivas, con soporte para
    líneas discontinuas que marquen la descomposición interna.
- Los nuevos temas añadidos al `index.json` deben cumplir estas reglas antes de publicarse.

### Convenciones trigonométricas
- **En la medida de lo posible, las resoluciones de trigonometría deben expresarse con
  `sin` y `cos` (y `arcsin`/`arccos` para ángulos), evitando `tan` y `arctan`.**
- Cuando se conocen dos catetos y falta la hipotenusa o el ángulo: calcular primero la
  hipotenusa por **Pitàgores** y después el ángulo con `arcsin` o `arccos`.
- Cuando se conoce un catete y el ángulo y se busca el otro catete: obtener primero la
  hipotenusa con `sin` o `cos` y después el catete restante con la razón complementaria.
- El razonamiento queda un poco más largo pero trabaja explícitamente Pitàgores + seno/coseno,
  que es el bloque central del temario de 4º ESO.

### Convenciones de triángulos rectángulos (teoremas)
- **Solo se usan Pitàgores y el teorema de l'altura** (`h² = m·n`, siendo `m` y `n` las
  proyecciones de los catetos sobre la hipotenusa). El **teorema del catete queda excluido**
  de forma explícita para no dispersar la enseñanza.
- Cada pregunta exige calcular **más de una magnitud** (p. ej. altura y un catete, o proyección
  y hipotenusa) para aumentar dificultad y obligar a encadenar dos teoremas.
- El **enunciado incluye una imagen** del triángulo con los datos conocidos y destacando la
  incógnita; la **resolución finaliza con una imagen** del triángulo con todos los valores
  ya resueltos.
- Todas las respuestas con raíces, fracciones o unidades deben renderizarse con LaTeX
  (`$\\sqrt{161}\\ \\text{cm}$`, nunca texto plano).

## Principios de diseño
- **Simplicidad sobre todo.** Sin login, sin estado global complejo. El back-end es lo más
  pequeño posible: un solo fichero JSON detrás de una API REST minimalista.
- **Claridad pedagógica.** Las resoluciones son el activo más importante: redactadas paso a paso,
  con lenguaje accesible y en catalán, evitando saltos de razonamiento.
- **Extensibilidad por datos.** Los temas y preguntas se cargan desde archivos **JSON**, de modo que
  añadir un nuevo tema o ampliar uno existente **no requiere tocar código**.
- **UI suficientemente potente para gráficos.** Muchas preguntas incluirán elementos visuales
  (vectores, ejes, puntos, figuras). La capa gráfica debe permitir renderizar estos elementos con
  calidad y de forma declarativa desde el propio JSON.
- **Robustez frente a cambios en el JSON.** Si se añaden nuevas preguntas a un tema ya jugado,
  deben aparecer como pendientes (la persistencia se basa en IDs, no en posiciones).
  Si se elimina una pregunta del JSON, su ID en el progreso se ignora silenciosamente.

## Alcance actual
La app incluye 6 temas publicados, todos con el mismo formato (25 preguntas × 4 opciones):

1. **Vectors — construcció gràfica (suma i resta).** Dado un plano con AB y CD sobre una
   cuadrícula, el alumno aplica la regla del triángulo o del paralelogramo y determina a qué
   punto llega el vector resultante.
2. **Vectors — suma i resta (càlcul).** Suma y resta analítica de vectores dados por puntos o
   directamente por componentes.
3. **Vectors — coordenades d'un extrem (A o B).** Dado `AB = (x, y)` y un extremo, calcular
   el otro extremo aplicando `B = A + AB` o `A = B − AB`.
4. **Triangles rectangles — teoremes (Pitàgores i altura).** Aplicación del teorema de
   Pitàgores y del **teorema de l'altura** (`h² = m·n`). **No se usa el teorema del catete**
   para mantener consistencia pedagógica. Cada pregunta pide más de una magnitud
   (p. ej. altura + un catete, proyección + hipotenusa).
5. **Problemes de triangles rectangles (trigonometria aplicada).** Situaciones reales
   (pals, escales, rampes, angles d'elevació/depressió, ombres, fars, avions…) resueltas
   con `sin`/`cos` y Pitàgores. Evitan sistemáticamente `tan`/`arctan` en la resolución.
6. **Perímetres i àrees de figures planes.** Cálculo de perímetros y áreas de figuras
   básicas (cuadrado, rectángulo, triángulo rectángulo, trapecio, círculo) y de figuras
   **compuestas por dos figuras básicas** (rectángulo + semicírculo, cuadrado + triángulo,
   L formada por dos rectángulos, placa con agujero circular, trapecio sobre rectángulo,
   etc.). Cada pregunta muestra la figura con los datos en el enunciado y, al resolver,
   la misma figura con el resultado final marcado.

Distractores pedagógicos comunes:
- Vectores: confundir suma con resta, invertir el orden de la diferencia, olvidar trasladar
  el segundo vector, sumar coordenadas de puntos en lugar de componentes, errores de signo,
  invertir origen/destino.
- Triangles: aplicar `h² = m+n`, confundir Pitàgores con suma simple, intercambiar catete
  con hipotenusa, usar proyección como catete.
- Trigonometria aplicada: usar `sin` donde toca `cos` (y viceversa), confundir ángulo de
  elevación con el complementario, dividir en lugar de multiplicar.

## Fuera de alcance (por ahora)
- Autenticación, perfiles, sincronización por usuario (el progreso es global compartido).
- Estadísticas detalladas, gráficas de evolución, gamificación.
- Editor visual de preguntas.
- Internacionalización más allá del catalán.
- Modo examen, temporizador, puntuaciones globales.
