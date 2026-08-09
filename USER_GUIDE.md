# Guía de uso — Asistente ONG

Herramienta local para organizaciones sociales que necesitan ordenar casos, analizar información y preparar documentación profesional sin enviar automáticamente los datos a Internet.

## 1. Inicio

Al abrir la aplicación se muestra el panel principal y una navegación lateral. La lista de casos debe comenzar vacía en una instalación nueva.

No se incluyen expedientes, relatos, personas ni situaciones ficticias precargadas.

## 2. Nuevo caso

Desde **Nuevo caso** se puede registrar:

- Nombre o alias, cuando corresponda.
- Contacto, si resulta necesario y está autorizado.
- Tipo de caso.
- Localidad o zona.
- Relato o información recibida.

El operador carga solamente la información necesaria para la atención. Después puede ejecutar el análisis local.

## 3. Análisis

El sistema puede señalar indicadores de prioridad, palabras o patrones relevantes, información faltante y aspectos que requieren revisión.

Los resultados son apoyo operativo. No constituyen diagnóstico, peritaje ni decisión profesional.

## 4. Informe Social Profesional

El módulo **Informe Social** recopila siete bloques:

### 1. Datos del profesional e institución

- Entidad emisora.
- Profesional de referencia.
- Número de colegiatura o matrícula.
- Destinatario.
- Fecha de emisión.
- Motivo de la solicitud.

Los cuatro primeros datos institucionales/profesionales pueden fijarse para reutilizarlos en nuevos informes.

### 2. Identificación de la persona de referencia

- Nombres y apellidos.
- DNI/NIE/pasaporte.
- Domicilio.
- Teléfono y correo.
- Fecha de nacimiento y edad.
- Sexo, nacionalidad y estado civil.

### 3. Unidad de convivencia y dinámica familiar

- Personas que viven en el hogar.
- Parentesco, edad y ocupación.
- Antecedentes familiares.
- Dinámica, vínculos, apoyos y conflictos.
- Genograma u observaciones visuales opcionales.

### 4. Situación socioeconómica y laboral

- Fuentes de ingresos y sustento.
- Situación laboral de los integrantes.
- Gastos esenciales y otros egresos relevantes.

### 5. Habitabilidad y vivienda

- Régimen de tenencia.
- Condiciones materiales.
- Habitaciones y hacinamiento.
- Agua, electricidad, transporte y servicios del entorno.

### 6. Salud y educación

- Situación sanitaria relevante.
- Discapacidad o dependencia.
- Tratamientos o apoyos.
- Nivel educativo.
- Asistencia escolar de niños, niñas y adolescentes.

### 7. Diagnóstico, valoración y propuesta

- Juicio técnico.
- Fortalezas y factores protectores.
- Vulnerabilidades y factores de riesgo.
- Propuesta de intervención.
- Recursos a activar.
- Observaciones finales.

## 5. Análisis del informe social

El botón **Analizar información** revisa:

- Completitud de los campos principales.
- Indicadores sociales relevantes.
- Posibles inconsistencias.
- Edad calculada a partir de la fecha de nacimiento.
- Relación entre convivientes y habitaciones cuando los datos permiten calcularla.
- Balance entre ingresos y egresos cuando se declaran montos.
- Fortalezas y factores protectores declarados.
- Recomendaciones de revisión.

El análisis no sustituye la valoración del profesional.

## 6. Guardado y exportación

### Guardar borrador

Guarda el informe localmente sin modificar los datos institucionales fijados.

### Fijar datos institucionales

Guarda únicamente los datos seleccionados para reutilizarlos en futuros informes.

### Exportar JSON

Genera una copia estructurada del informe y, si fue ejecutado, de su análisis orientativo.

### Generar PDF

Genera un documento profesional con los siete bloques y el análisis orientativo.

## 7. Casos

Los casos se crean únicamente mediante la carga realizada por el operador.

No hay casos de ejemplo, números de caso ficticios ni mensajes predeterminados dentro de la aplicación.

Los casos reales se almacenan localmente en SQLite.

## 8. Privacidad

El procesamiento del caso y del informe se realiza localmente. La aplicación no envía automáticamente los datos sensibles a servicios externos.

Antes de compartir un documento, verificá destinatario, contenido y datos personales incluidos.

## 9. Ejecutar

### Opción rápida

```bat
run_app.bat
```

### Manual

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m src.main
```

### Crear EXE

```bat
build_exe.bat
```

El ejecutable queda en `dist\AsistenteONG.exe`.

## 10. Principio de funcionamiento

**Recopilar → analizar → revisar profesionalmente → intervenir/derivar → documentar → hacer seguimiento.**

La herramienta asiste al trabajo; la decisión profesional permanece en manos del equipo responsable.
