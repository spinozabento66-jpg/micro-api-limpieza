from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import uvicorn

app = FastAPI(
    title="Micro-API de Limpieza y Estructuración de Texto",
    description="Limpia texto sucio, remueve etiquetas HTML, caracteres especiales y devuelve un JSON estructurado.",
    version="1.0.0"
)

# Estructura de entrada
class SolicitudLimpieza(BaseModel):
    texto_raw: str
    remover_numeros: bool = False

# Estructura de salida
class RespuestaLimpieza(BaseModel):
    estatus: str
    total_palabras: int
    caracteres_originales: int
    caracteres_limpios: int
    texto_procesado: str

@app.get("/")
def home():
    return {"mensaje": "API de Limpieza de Texto activa y lista para recibir solicitudes."}

@app.post("/api/v1/limpiar-texto", response_model=RespuestaLimpieza)
def limpiar_texto(datos: SolicitudLimpieza):
    try:
        texto = datos.texto_raw
        
        if not texto or not texto.strip():
            raise HTTPException(status_code=400, detail="El texto enviado está vacío.")

        # 1. Remover etiquetas HTML si existen
        texto_limpio = re.sub(r'<[^>]+>', '', texto)
        
        # 2. Remover caracteres especiales manteniendo acentos y espacios
        texto_limpio = re.sub(r'[^\w\s\dÁÉÍÓÚáéíóúÑñ,.!?]', '', texto_limpio)
        
        # 3. Remover números opcionalmente
        if datos.remover_numeros:
            texto_limpio = re.sub(r'\d+', '', texto_limpio)
            
        # 4. Normalizar espacios dobles o saltos de línea
        texto_limpio = ' '.join(texto_limpio.split())

        palabras = texto_limpio.split()

        return RespuestaLimpieza(
            estatus="exitoso",
            total_palabras=len(palabras),
            caracteres_originales=len(texto),
            caracteres_limpios=len(texto_limpio),
            texto_procesado=texto_limpio
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el texto: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)