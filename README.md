# Asistente ONG

**Plataforma local para personas, casos, documentación, análisis contextual y seguimiento de organizaciones sociales.**

> El sistema es una herramienta de apoyo. No reemplaza la revisión profesional ni toma por sí solo decisiones legales, sanitarias o de protección.

## Estado

La suite actual tiene **71 tests automatizados pasando**. El proyecto incluye:

- Personas únicas con múltiples casos e historial longitudinal.
- Análisis contextual y explicable.
- Evidencia documental separada de decisiones.
- Biblioteca PDF con procedencia/página.
- Importación XLSX en modo revisión y confirmación explícita.
- Seguimientos, tareas, derivaciones y agenda.
- Roles, permisos, bloqueo de sesión y backup cifrado.
- Auditoría y exportación anonimizada.
- Tutorial interactivo de primer arranque.
- Configuración institucional para informes.
- Ejecutable Windows mediante PyInstaller.
- Instalador Windows mediante Inno Setup en CI.

## Principios

### Local first

Los expedientes, personas, casos y memoria se mantienen localmente como comportamiento base. Las consultas a fuentes externas son una función separada y explícita.

### Evidencia ≠ decisión

Los documentos, coincidencias históricas y señales del motor se presentan como evidencia o apoyo para revisión. El sistema no transforma automáticamente una coincidencia en una decisión.

### Una persona, muchos casos

El registro de persona se reutiliza. Si vuelve a consultar a la organización, se agrega un nuevo caso en lugar de duplicar a la persona.

## Inicio rápido para una ONG

1. Ejecutar `AsistenteONG.exe`.
2. Completar el tutorial inicial.
3. Ir a **Configuración** y cargar los datos institucionales necesarios.
4. Revisar **Seguridad** y establecer el procedimiento de backup.
5. Practicar con datos ficticios.
6. Crear una persona y dos casos de prueba.
7. Importar un PDF institucional en **Biblioteca**.
8. Revisar evidencia y fuentes.
9. Probar seguimiento y agenda.
10. Realizar un backup y comprobar su restauración.

## Desarrollo

```powershell
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
python -m pip install -r requirements.txt
python -m pytest
python -m src.main
```

El resultado esperado de la suite actual es:

```text
71 passed
```

## Generar EXE

En Windows:

```powershell
build_exe.bat
```

Resultado:

```text
dist\AsistenteONG.exe
```

También existe un workflow de GitHub Actions que ejecuta tests, smoke test, compila el EXE y genera un instalador Windows como artefactos.

## Documentación de producto

- [Guía de usuario final](docs/GUIA_USUARIO_FINAL.md)
- [Protocolo de piloto con usuarios](docs/PILOTO_USUARIOS.md)
- [Plan de distribución nacional](docs/DISTRIBUCION_NACIONAL.md)
- [Instalación](INSTALL.md)
- [Testing](docs/testing.md)
- [Herramientas gratuitas](docs/HERRAMIENTAS_GRATUITAS.md)
- [Comportamiento del producto](docs/PRODUCT_BEHAVIOR.md)
- [Roadmap](docs/ROADMAP_COMPLETA.md)

## Instalador

El archivo `installer/AsistenteONG.iss` permite construir un instalador Windows con Inno Setup. El workflow `Windows Build` también genera el instalador como artefacto.

## Piloto antes de producción

La parte técnica no sustituye una validación con una organización. El protocolo de piloto está en `docs/PILOTO_USUARIOS.md` y debe ejecutarse primero con datos ficticios o anonimizados.

Para una distribución amplia se debe aprobar el piloto, verificar backup/restauración, revisar permisos y publicar checksum y notas de versión.

## Licencia y uso

Consultar `LICENSE_SOCIAL.md` antes de redistribuir. Las organizaciones deben definir sus propios procedimientos de privacidad, conservación, acceso y respuesta profesional.

## Apoyo

El repositorio es mantenido por **Sarah Lee Olivera** con apoyo de **CCOMUSOC**.
