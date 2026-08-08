"""
Generador de Informes Sociales Profesionales
Estructura completa según normativa de trabajo social
Colores: Blanco, Negro, Azul #0e98d6
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class DatosProfesional:
    """Datos del profesional e institución."""
    entidad_emisora: str = ""
    profesional_nombre: str = ""
    profesional_apellidos: str = ""
    numero_colegiatura: str = ""
    destinatario: str = ""
    fecha_emision: str = ""
    motivo: str = ""

    def to_dict(self) -> dict:
        return {
            "entidad_emisora": self.entidad_emisora,
            "profesional": f"{self.profesional_nombre} {self.profesional_apellidos}",
            "colegiatura": self.numero_colegiatura,
            "destinatario": self.destinatario,
            "fecha": self.fecha_emision,
            "motivo": self.motivo
        }


@dataclass
class DatosIdentificacion:
    """Datos de identificación del usuario."""
    nombres: str = ""
    apellidos: str = ""
    dni_nie: str = ""
    pasaporte: str = ""
    direccion: str = ""
    telefono: str = ""
    telefono_alt: str = ""
    email: str = ""
    fecha_nacimiento: str = ""
    edad: int = 0
    sexo: str = ""  # M/F/Otro
    nacionalidad: str = ""
    estado_civil: str = ""  # Soltero/Casado/Divorciado/Viudo/Unión libre

    def to_dict(self) -> dict:
        return {
            "nombre_completo": f"{self.nombres} {self.apellidos}",
            "dni_nie": self.dni_nie,
            "pasaporte": self.pasaporte,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "telefono_alt": self.telefono_alt,
            "email": self.email,
            "fecha_nacimiento": self.fecha_nacimiento,
            "edad": self.edad,
            "sexo": self.sexo,
            "nacionalidad": self.nacionalidad,
            "estado_civil": self.estado_civil
        }


@dataclass
class MiembroFamiliar:
    """Miembro de la unidad de convivencia."""
    nombre: str = ""
    parentesco: str = ""  # Padre/Madre/Hijo/Hija/Cónyuge/Abuelo/Otro
    edad: int = 0
    ocupacion: str = ""
    ingresos: float = 0.0
    situacion_laboral: str = ""  # Empleado/Desempleado/Jubilado/Estudiante/Discapacidad
    observaciones: str = ""


@dataclass
class UnidadConvivencia:
    """Composición de la unidad de convivencia."""
    miembros: List[MiembroFamiliar] = field(default_factory=list)
    genograma_data: str = ""  # JSON o descripción textual
    historia_familiar: str = ""
    dinamica_relaciones: str = ""  # Conflictivas/De apoyo/Neutras

    def to_dict(self) -> dict:
        return {
            "total_miembros": len(self.miembros),
            "miembros": [
                {
                    "nombre": m.nombre,
                    "parentesco": m.parentesco,
                    "edad": m.edad,
                    "ocupacion": m.ocupacion,
                    "ingresos": m.ingresos,
                    "situacion_laboral": m.situacion_laboral,
                    "observaciones": m.observaciones
                }
                for m in self.miembros
            ],
            "genograma": self.genograma_data,
            "historia_familiar": self.historia_familiar,
            "dinamica": self.dinamica_relaciones
        }


@dataclass
class SituacionSocioeconomica:
    """Situación socioeconómica y laboral."""
    ingresos_salarios: float = 0.0
    ingresos_pensiones: float = 0.0
    ingresos_subsidios: float = 0.0
    ingresos_otros: float = 0.0

    egresos_alquiler: float = 0.0
    egresos_hipoteca: float = 0.0
    egresos_servicios: float = 0.0
    egresos_alimentacion: float = 0.0
    egresos_otros: float = 0.0

    situacion_empleo_principal: str = ""  # Empleado/Desempleado/Informal
    duracion_desempleo: str = ""

    def ingresos_total(self) -> float:
        return self.ingresos_salarios + self.ingresos_pensiones + self.ingresos_subsidios + self.ingresos_otros

    def egresos_total(self) -> float:
        return (self.egresos_alquiler + self.egresos_hipoteca + self.egresos_servicios + 
                self.egresos_alimentacion + self.egresos_otros)

    def balance(self) -> float:
        return self.ingresos_total() - self.egresos_total()

    def to_dict(self) -> dict:
        return {
            "ingresos": {
                "salarios": self.ingresos_salarios,
                "pensiones": self.ingresos_pensiones,
                "subsidios": self.ingresos_subsidios,
                "otros": self.ingresos_otros,
                "total": self.ingresos_total()
            },
            "egresos": {
                "alquiler": self.egresos_alquiler,
                "hipoteca": self.egresos_hipoteca,
                "servicios": self.egresos_servicios,
                "alimentacion": self.egresos_alimentacion,
                "otros": self.egresos_otros,
                "total": self.egresos_total()
            },
            "balance": self.balance(),
            "situacion_empleo": self.situacion_empleo_principal,
            "duracion_desempleo": self.duracion_desempleo
        }


@dataclass
class Habitabilidad:
    """Habitabilidad y vivienda."""
    regimen_tenencia: str = ""  # Propia/Alquilada/Cedida/Precariedad/Situación de calle
    tipo_vivienda: str = ""  # Casa/Departamento/Cuarto/Choza/Refugio
    num_habitaciones: int = 0
    num_dormitorios: int = 0
    hacinamiento: str = ""  # Sí/No

    estado_infraestructura: str = ""  # Buena/Regular/Mala/Precaria
    materiales: str = ""  # Ladrillo/Madera/Cartón/Chapa

    agua_potable: bool = False
    electricidad: bool = False
    gas: bool = False
    cloacas: bool = False

    acceso_transporte: str = ""  # Bueno/Regular/Difícil
    equipamiento_barrio: str = ""  # Escuelas, hospitales, comercios cercanos

    def to_dict(self) -> dict:
        return {
            "regimen_tenencia": self.regimen_tenencia,
            "tipo_vivienda": self.tipo_vivienda,
            "habitaciones": self.num_habitaciones,
            "dormitorios": self.num_dormitorios,
            "hacinamiento": self.hacinamiento,
            "estado_infraestructura": self.estado_infraestructura,
            "materiales": self.materiales,
            "servicios": {
                "agua_potable": "Sí" if self.agua_potable else "No",
                "electricidad": "Sí" if self.electricidad else "No",
                "gas": "Sí" if self.gas else "No",
                "cloacas": "Sí" if self.cloacas else "No"
            },
            "transporte": self.acceso_transporte,
            "equipamiento_barrio": self.equipamiento_barrio
        }


@dataclass
class SaludEducacion:
    """Situación de salud y educación."""
    enfermedades_cronicas: str = ""
    discapacidades: str = ""
    situacion_dependencia: str = ""  # Grado I/II/III/Ninguna
    adicciones: str = ""

    medicamentos: str = ""
    cobertura_salud: str = ""  # Obra social/PAMI/Sin cobertura

    nivel_academico: str = ""  # Primario/Secundario/Terciario/Universitario
    asistencia_escolar: str = ""  # Regular/Irregular/Abandonó/Nunca asistió
    escolaridad_menores: str = ""  # Detalle de asistencia de menores

    def to_dict(self) -> dict:
        return {
            "salud": {
                "enfermedades_cronicas": self.enfermedades_cronicas,
                "discapacidades": self.discapacidades,
                "dependencia": self.situacion_dependencia,
                "adicciones": self.adicciones,
                "medicamentos": self.medicamentos,
                "cobertura": self.cobertura_salud
            },
            "educacion": {
                "nivel_academico": self.nivel_academico,
                "asistencia_escolar": self.asistencia_escolar,
                "escolaridad_menores": self.escolaridad_menores
            }
        }


@dataclass
class DiagnosticoSocial:
    """Diagnóstico, valoración social y propuesta."""
    juicio_tecnico: str = ""
    vulnerabilidades: str = ""
    fortalezas: str = ""

    propuesta_intervencion: str = ""
    recursos_solicitados: str = ""
    plazo_intervencion: str = ""
    seguimiento: str = ""

    def to_dict(self) -> dict:
        return {
            "diagnostico": self.juicio_tecnico,
            "vulnerabilidades": self.vulnerabilidades,
            "fortalezas": self.fortalezas,
            "propuesta_intervencion": self.propuesta_intervencion,
            "recursos_solicitados": self.recursos_solicitados,
            "plazo": self.plazo_intervencion,
            "seguimiento": self.seguimiento
        }


@dataclass
class InformeSocial:
    """Informe social completo."""
    id: str = ""
    fecha_creacion: str = ""

    datos_profesional: DatosProfesional = field(default_factory=DatosProfesional)
    datos_identificacion: DatosIdentificacion = field(default_factory=DatosIdentificacion)
    unidad_convivencia: UnidadConvivencia = field(default_factory=UnidadConvivencia)
    socioeconomica: SituacionSocioeconomica = field(default_factory=SituacionSocioeconomica)
    habitabilidad: Habitabilidad = field(default_factory=Habitabilidad)
    salud_educacion: SaludEducacion = field(default_factory=SaludEducacion)
    diagnostico: DiagnosticoSocial = field(default_factory=DiagnosticoSocial)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha_creacion": self.fecha_creacion,
            "datos_profesional": self.datos_profesional.to_dict(),
            "datos_identificacion": self.datos_identificacion.to_dict(),
            "unidad_convivencia": self.unidad_convivencia.to_dict(),
            "situacion_socioeconomica": self.socioeconomica.to_dict(),
            "habitabilidad": self.habitabilidad.to_dict(),
            "salud_educacion": self.salud_educacion.to_dict(),
            "diagnostico": self.diagnostico.to_dict()
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class InformeManager:
    """Gestor de informes sociales."""

    def __init__(self):
        self.informes: List[InformeSocial] = []
        self._load_from_db()

    def _load_from_db(self):
        """Carga informes desde la base de datos."""
        try:
            import sqlite3
            from ..database.schema import DB_PATH

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, data, created_at FROM social_reports ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                try:
                    data = json.loads(row[1])
                    informe = self._dict_to_informe(data)
                    informe.id = row[0]
                    informe.fecha_creacion = row[2]
                    self.informes.append(informe)
                except:
                    pass

            logger.info(f"✅ {len(self.informes)} informes cargados")
        except Exception as e:
            logger.error(f"Error cargando informes: {e}")

    def create_informe(self) -> InformeSocial:
        """Crea un nuevo informe vacío."""
        from datetime import datetime
        import uuid

        informe = InformeSocial(
            id=str(uuid.uuid4())[:8],
            fecha_creacion=datetime.now().isoformat()
        )

        # Pre-llenar fecha
        informe.datos_profesional.fecha_emision = datetime.now().strftime("%d/%m/%Y")

        return informe

    def save_informe(self, informe: InformeSocial) -> bool:
        """Guarda un informe en la base de datos."""
        try:
            import sqlite3
            from ..database.schema import DB_PATH

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS social_reports (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                INSERT OR REPLACE INTO social_reports (id, data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (informe.id, informe.to_json()))

            conn.commit()
            conn.close()

            logger.info(f"✅ Informe guardado: {informe.id}")
            return True
        except Exception as e:
            logger.error(f"Error guardando informe: {e}")
            return False

    def get_informe(self, informe_id: str) -> Optional[InformeSocial]:
        """Obtiene un informe por ID."""
        for informe in self.informes:
            if informe.id == informe_id:
                return informe
        return None

    def list_informes(self) -> List[InformeSocial]:
        """Lista todos los informes."""
        return self.informes

    def delete_informe(self, informe_id: str) -> bool:
        """Elimina un informe."""
        try:
            import sqlite3
            from ..database.schema import DB_PATH

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM social_reports WHERE id = ?", (informe_id,))
            conn.commit()
            conn.close()

            self.informes = [i for i in self.informes if i.id != informe_id]
            logger.info(f"🗑️ Informe eliminado: {informe_id}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando informe: {e}")
            return False

    def _dict_to_informe(self, data: dict) -> InformeSocial:
        """Convierte diccionario a InformeSocial."""
        informe = InformeSocial()

        # Datos profesional
        dp = data.get("datos_profesional", {})
        informe.datos_profesional.entidad_emisora = dp.get("entidad_emisora", "")
        informe.datos_profesional.profesional_nombre = dp.get("profesional", "").split()[0] if dp.get("profesional") else ""
        informe.datos_profesional.profesional_apellidos = " ".join(dp.get("profesional", "").split()[1:]) if dp.get("profesional") else ""
        informe.datos_profesional.numero_colegiatura = dp.get("colegiatura", "")
        informe.datos_profesional.destinatario = dp.get("destinatario", "")
        informe.datos_profesional.fecha_emision = dp.get("fecha", "")
        informe.datos_profesional.motivo = dp.get("motivo", "")

        # Datos identificación
        di = data.get("datos_identificacion", {})
        nombre_completo = di.get("nombre_completo", "")
        partes = nombre_completo.split()
        informe.datos_identificacion.nombres = partes[0] if partes else ""
        informe.datos_identificacion.apellidos = " ".join(partes[1:]) if len(partes) > 1 else ""
        informe.datos_identificacion.dni_nie = di.get("dni_nie", "")
        informe.datos_identificacion.direccion = di.get("direccion", "")
        informe.datos_identificacion.telefono = di.get("telefono", "")
        informe.datos_identificacion.email = di.get("email", "")
        informe.datos_identificacion.fecha_nacimiento = di.get("fecha_nacimiento", "")
        informe.datos_identificacion.edad = di.get("edad", 0)
        informe.datos_identificacion.sexo = di.get("sexo", "")
        informe.datos_identificacion.nacionalidad = di.get("nacionalidad", "")
        informe.datos_identificacion.estado_civil = di.get("estado_civil", "")

        # Socioeconómica
        se = data.get("situacion_socioeconomica", {})
        informe.socioeconomica.ingresos_salarios = se.get("ingresos", {}).get("salarios", 0)
        informe.socioeconomica.ingresos_pensiones = se.get("ingresos", {}).get("pensiones", 0)
        informe.socioeconomica.ingresos_subsidios = se.get("ingresos", {}).get("subsidios", 0)
        informe.socioeconomica.egresos_alquiler = se.get("egresos", {}).get("alquiler", 0)
        informe.socioeconomica.egresos_servicios = se.get("egresos", {}).get("servicios", 0)
        informe.socioeconomica.situacion_empleo_principal = se.get("situacion_empleo", "")

        # Habitabilidad
        hab = data.get("habitabilidad", {})
        informe.habitabilidad.regimen_tenencia = hab.get("regimen_tenencia", "")
        informe.habitabilidad.tipo_vivienda = hab.get("tipo_vivienda", "")
        informe.habitabilidad.num_habitaciones = hab.get("habitaciones", 0)
        informe.habitabilidad.hacinamiento = hab.get("hacinamiento", "")

        # Salud
        sal = data.get("salud_educacion", {}).get("salud", {})
        informe.salud_educacion.enfermedades_cronicas = sal.get("enfermedades_cronicas", "")
        informe.salud_educacion.discapacidades = sal.get("discapacidades", "")
        informe.salud_educacion.cobertura_salud = sal.get("cobertura", "")

        # Diagnóstico
        diag = data.get("diagnostico", {})
        informe.diagnostico.juicio_tecnico = diag.get("diagnostico", "")
        informe.diagnostico.propuesta_intervencion = diag.get("propuesta_intervencion", "")

        return informe
