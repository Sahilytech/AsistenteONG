# Informe Social Profesional

La aplicación incorpora un formulario local para estructurar informes sociales en siete bloques:

1. Datos del profesional e institución.
2. Identificación de la persona de referencia.
3. Unidad de convivencia y dinámica familiar.
4. Situación socioeconómica y laboral.
5. Habitabilidad y vivienda.
6. Salud y educación.
7. Diagnóstico, valoración social y propuesta de intervención.

## Datos institucionales fijables

Los campos de entidad emisora, profesional, matrícula/colegiatura y destinatario se guardan en `data/institution_defaults.json` y se precargan en futuros informes.

## PDF

El botón **Generar PDF** crea un documento A4 institucional con encabezado, las siete secciones, tabla de datos y espacio para firma/sello. El contenido debe ser revisado por el profesional responsable antes de emitirlo.

## Privacidad

El proyecto está diseñado para trabajar localmente. No se envían los datos del informe a servicios externos.

## Identidad visual

- Fondo: `#FFFFFF`
- Texto: `#000000`
- Azul institucional: `#0e98d6`
- Modo: claro únicamente

## EXE

En Windows ejecutar `build_exe.bat`. El proceso instala dependencias, limpia compilaciones anteriores y genera `dist/AsistenteONG.exe` con PyInstaller.

La carpeta `data` se incluye para la ejecución inicial; para datos sensibles de producción se recomienda conservarlos en una ubicación local de trabajo y establecer una política de respaldo definida por la organización.
