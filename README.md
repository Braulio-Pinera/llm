# 📝 Asistente de Escritura Automática

Un asistente inteligente de escritura que utiliza la API de OpenAI para ayudarte a generar, corregir y mejorar textos de manera automática. Perfecto para escritores, estudiantes, profesionales y cualquier persona que necesite apoyo en sus tareas de redacción.

## ✨ Características Principales

- 🚀 **Generación de Texto Completo**: Crea artículos, correos, novelas y ensayos basados en un tema
- ✏️ **Corrección de Gramática**: Detecta y corrige errores ortográficos, gramaticales y de estilo
- 💡 **Sugerencias de Oraciones**: Proporciona múltiples opciones para continuar tu texto
- 📊 **Análisis de Estilo**: Evalúa y mejora la calidad de tu escritura
- 🏷️ **Generación de Títulos**: Crea títulos creativos y atractivos para tu contenido
- 📈 **Historial de Operaciones**: Mantiene un registro de todas las tareas realizadas

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+**
- **OpenAI API** (GPT-3.5-turbo)
- **Librerías estándar de Python**

## 📋 Requisitos Previos

1. **Python 3.7 o superior** instalado en tu sistema
2. **Cuenta de OpenAI** con acceso a la API
3. **API Key de OpenAI** válida

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/asistente-escritura.git
cd asistente-escritura
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar API Key
Tienes varias opciones para configurar tu API Key de OpenAI:

#### Opción A: Variable de entorno (Recomendado)
```bash
export OPENAI_API_KEY="tu-api-key-aquí"
```

#### Opción B: Archivo .env
Crea un archivo `.env` en el directorio raíz:
```
OPENAI_API_KEY=tu-api-key-aquí
```

#### Opción C: Directamente en el código
Modifica la variable `api_key` en el archivo principal.

## 🎯 Uso

### Modo Interactivo

Ejecuta el programa principal para acceder al menú interactivo:

```bash
python asistente_escritura.py
```

### Modo Programático

```python
from asistente_escritura import AsistenteEscritura

# Inicializar el asistente
asistente = AsistenteEscritura(api_key="tu-api-key")

# Generar un artículo
articulo = asistente.generar_texto(
    tema="Inteligencia Artificial", 
    tipo_texto="artículo",
    longitud="medio",
    tono="profesional"
)

# Corregir gramática
resultado = asistente.corregir_gramatica("Texto con errores")

# Sugerir oraciones
sugerencias = asistente.sugerir_oraciones("Contexto previo", 3)
```

## 📚 Funcionalidades Detalladas

### 1. Generación de Texto
```python
asistente.generar_texto(
    tema="Tu tema aquí",
    tipo_texto="artículo|correo|novela|ensayo",
    longitud="corto|medio|largo", 
    tono="profesional|casual|formal|creativo"
)
```

### 2. Corrección de Gramática
```python
resultado = asistente.corregir_gramatica("Tu texto aquí")
print(resultado["corregido"])  # Texto corregido
print(resultado["cambios"])    # Explicación de cambios
```

### 3. Sugerencias de Oraciones
```python
sugerencias = asistente.sugerir_oraciones("Contexto", num_sugerencias=3)
for sugerencia in sugerencias:
    print(f"- {sugerencia}")
```

### 4. Análisis de Estilo
```python
analisis = asistente.analizar_estilo("Tu texto aquí")
print(analisis["análisis"])      # Análisis detallado
print(analisis["fortalezas"])    # Puntos fuertes
print(analisis["sugerencias"])   # Recomendaciones
```

### 5. Generación de Títulos
```python
titulos = asistente.generar_titulo("Contenido del texto", num_opciones=5)
for i, titulo in enumerate(titulos, 1):
    print(f"{i}. {titulo}")
```

## 🔧 Configuración Avanzada

### Personalizar el Modelo
Puedes modificar el modelo de OpenAI utilizado editando la clase:

```python
# En el método que desees personalizar
response = self.client.chat.completions.create(
    model="gpt-4",  # Cambiar por gpt-4 para mejor calidad
    messages=[...],
    max_tokens=2000,
    temperature=0.7  # Ajustar creatividad (0.0-1.0)
)
```

### Parámetros de Temperature
- **0.0-0.3**: Respuestas más precisas y conservadoras
- **0.4-0.7**: Balance entre creatividad y precisión
- **0.8-1.0**: Respuestas más creativas y variadas

## 📊 Ejemplos de Uso

### Ejemplo 1: Generar un Correo Profesional
```python
correo = asistente.generar_texto(
    tema="Solicitud de reunión para proyecto",
    tipo_texto="correo",
    tono="profesional"
)
```

### Ejemplo 2: Corregir un Texto
```python
texto_original = "Hola, espero que esten bien. Queria comentarles sobre el projecto."
correccion = asistente.corregir_gramatica(texto_original)
print(correccion["corregido"])
# Output: "Hola, espero que estén bien. Quería comentarles sobre el proyecto."
```

### Ejemplo 3: Generar Ideas para Continuar
```python
contexto = "La inteligencia artificial está transformando la educación."
ideas = asistente.sugerir_oraciones(contexto, 3)
# Output: 
# - "Los estudiantes ahora pueden acceder a tutores virtuales personalizados."
# - "Esta tecnología permite adaptar el aprendizaje al ritmo de cada alumno."
# - "Sin embargo, es importante mantener el equilibrio con la interacción humana."
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] Interfaz gráfica con Tkinter o PyQt
- [ ] Soporte para múltiples idiomas
- [ ] Integración con Google Docs
- [ ] Exportación a diferentes formatos (PDF, DOCX)
- [ ] Sistema de plantillas personalizables
- [ ] API REST para integración web
- [ ] Modo colaborativo para equipos

## ❗ Limitaciones Conocidas

- Requiere conexión a internet para funcionar
- Está sujeto a los límites de rate de la API de OpenAI
- Los textos muy largos pueden ser truncados
- La calidad depende de la claridad de las instrucciones

## 🔒 Seguridad y Privacidad

- ⚠️ **No compartas tu API Key**: Manténla segura y nunca la subas a repositorios públicos
- 🔐 **Datos sensibles**: Ten cuidado al procesar información confidencial
- 📊 **Uso de datos**: OpenAI puede usar los datos enviados para mejorar sus modelos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.