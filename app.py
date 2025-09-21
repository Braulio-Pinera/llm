import openai
import json
import re
from typing import Dict, List, Optional
from datetime import datetime

api_key= "INSERTA TU API KEY"

class AsistenteEscritura:
    """
    Asistente de escritura automática que utiliza la API de OpenAI
    para ayudar con corrección, sugerencias y generación de texto.
    """
    
    def __init__(self, api_key: str):
        """
        Inicializa el asistente con la API key de OpenAI
        
        Args:
            api_key (str): Clave de API de OpenAI
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.historial = []
        
    def generar_texto(self, tema: str, tipo_texto: str = "artículo", 
                     longitud: str = "medio", tono: str = "profesional") -> str:
        """
        Genera texto completo basado en un tema específico
        
        Args:
            tema (str): Tema o idea principal
            tipo_texto (str): Tipo de texto (artículo, correo, novela, ensayo)
            longitud (str): Longitud deseada (corto, medio, largo)
            tono (str): Tono del texto (profesional, casual, formal, creativo)
        
        Returns:
            str: Texto generado
        """
        longitud_palabras = {
            "corto": "200-300 palabras",
            "medio": "500-700 palabras", 
            "largo": "1000-1500 palabras"
        }
        
        prompt = f"""
        Escribe un {tipo_texto} sobre el tema: "{tema}"
        
        Requisitos:
        - Longitud: {longitud_palabras.get(longitud, "500-700 palabras")}
        - Tono: {tono}
        - Estructura clara y coherente
        - Contenido original y bien desarrollado
        
        Si es un correo electrónico, incluye saludo y despedida apropiados.
        Si es una novela, crea una narrativa envolvente con personajes.
        Si es un artículo, incluye introducción, desarrollo y conclusión.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en escritura creativa y profesional. Generas contenido de alta calidad adaptado a las necesidades del usuario."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            texto_generado = response.choices[0].message.content.strip()
            self._guardar_en_historial("generación", tema, texto_generado)
            return texto_generado
            
        except Exception as e:
            return f"Error al generar texto: {str(e)}"
    
    def corregir_gramatica(self, texto: str) -> Dict[str, str]:
        """
        Corrige gramática y estilo de un texto
        
        Args:
            texto (str): Texto a corregir
            
        Returns:
            Dict[str, str]: Diccionario con texto original, corregido y explicación
        """
        prompt = f"""
        Corrige la gramática, ortografía y estilo del siguiente texto.
        Proporciona el texto corregido y explica los cambios principales realizados.
        
        Texto original:
        {texto}
        
        Formato de respuesta:
        TEXTO_CORREGIDO: [texto corregido aquí]
        CAMBIOS_REALIZADOS: [explicación de los cambios principales]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un corrector experto en gramática española. Corriges errores ortográficos, gramaticales y de estilo manteniendo el sentido original del texto."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            respuesta = response.choices[0].message.content.strip()
            
            # Parsear la respuesta
            texto_corregido = ""
            cambios = ""
            
            if "TEXTO_CORREGIDO:" in respuesta:
                partes = respuesta.split("CAMBIOS_REALIZADOS:")
                texto_corregido = partes[0].replace("TEXTO_CORREGIDO:", "").strip()
                if len(partes) > 1:
                    cambios = partes[1].strip()
            else:
                texto_corregido = respuesta
                cambios = "Correcciones aplicadas automáticamente."
            
            resultado = {
                "original": texto,
                "corregido": texto_corregido,
                "cambios": cambios
            }
            
            self._guardar_en_historial("corrección", texto[:50] + "...", resultado)
            return resultado
            
        except Exception as e:
            return {
                "original": texto,
                "corregido": texto,
                "cambios": f"Error al corregir: {str(e)}"
            }
    
    def sugerir_oraciones(self, contexto: str, num_sugerencias: int = 3) -> List[str]:
        """
        Sugiere oraciones para continuar un texto
        
        Args:
            contexto (str): Texto previo para contexto
            num_sugerencias (int): Número de sugerencias a generar
            
        Returns:
            List[str]: Lista de oraciones sugeridas
        """
        prompt = f"""
        Basándote en el siguiente contexto, sugiere {num_sugerencias} oraciones diferentes 
        para continuar el texto de manera natural y coherente.
        
        Contexto:
        {contexto}
        
        Proporciona {num_sugerencias} sugerencias numeradas, cada una en una línea diferente.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente de escritura que ayuda a continuar textos de manera coherente y natural."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            respuesta = response.choices[0].message.content.strip()
            sugerencias = []
            
            # Parsear las sugerencias numeradas
            lineas = respuesta.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if re.match(r'^\d+\.', linea):
                    sugerencia = re.sub(r'^\d+\.\s*', '', linea)
                    sugerencias.append(sugerencia)
                elif linea and len(sugerencias) < num_sugerencias:
                    sugerencias.append(linea)
            
            # Si no se parsearon correctamente, dividir por líneas
            if not sugerencias:
                sugerencias = [linea.strip() for linea in lineas if linea.strip()][:num_sugerencias]
            
            self._guardar_en_historial("sugerencias", contexto[:50] + "...", sugerencias)
            return sugerencias[:num_sugerencias]
            
        except Exception as e:
            return [f"Error al generar sugerencias: {str(e)}"]
    
    def analizar_estilo(self, texto: str) -> Dict[str, str]:
        """
        Analiza el estilo del texto y proporciona sugerencias de mejora
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            Dict[str, str]: Análisis del estilo y sugerencias
        """
        prompt = f"""
        Analiza el estilo del siguiente texto y proporciona sugerencias de mejora.
        
        Evalúa:
        - Claridad y fluidez
        - Tono y registro
        - Estructura y coherencia
        - Vocabulario y variedad
        
        Texto:
        {texto}
        
        Formato de respuesta:
        ANÁLISIS: [análisis detallado del estilo]
        FORTALEZAS: [aspectos positivos]
        SUGERENCIAS: [recomendaciones específicas para mejorar]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de estilo literario y escritura. Proporcionas análisis constructivos y sugerencias específicas para mejorar la escritura."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.4
            )
            
            respuesta = response.choices[0].message.content.strip()
            
            # Parsear la respuesta
            resultado = {"texto_original": texto}
            secciones = ["ANÁLISIS:", "FORTALEZAS:", "SUGERENCIAS:"]
            
            for i, seccion in enumerate(secciones):
                if seccion in respuesta:
                    inicio = respuesta.find(seccion) + len(seccion)
                    if i < len(secciones) - 1:
                        siguiente_seccion = secciones[i + 1]
                        if siguiente_seccion in respuesta:
                            fin = respuesta.find(siguiente_seccion)
                            contenido = respuesta[inicio:fin].strip()
                        else:
                            contenido = respuesta[inicio:].strip()
                    else:
                        contenido = respuesta[inicio:].strip()
                    
                    clave = seccion.replace(":", "").lower()
                    resultado[clave] = contenido
            
            # Si no se parseó correctamente, usar la respuesta completa
            if len(resultado) == 1:
                resultado["análisis"] = respuesta
            
            self._guardar_en_historial("análisis", texto[:50] + "...", resultado)
            return resultado
            
        except Exception as e:
            return {
                "texto_original": texto,
                "análisis": f"Error al analizar estilo: {str(e)}"
            }
    
    def generar_titulo(self, contenido: str, num_opciones: int = 5) -> List[str]:
        """
        Genera títulos creativos para un contenido dado
        
        Args:
            contenido (str): Contenido para el cual generar títulos
            num_opciones (int): Número de opciones de títulos
            
        Returns:
            List[str]: Lista de títulos sugeridos
        """
        prompt = f"""
        Basándote en el siguiente contenido, genera {num_opciones} títulos creativos y atractivos.
        Los títulos deben ser relevantes, llamativos y capturar la esencia del contenido.
        
        Contenido:
        {contenido}
        
        Proporciona {num_opciones} títulos numerados, cada uno en una línea diferente.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing de contenidos y copywriting. Creas títulos atractivos y efectivos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            respuesta = response.choices[0].message.content.strip()
            titulos = []
            
            # Parsear los títulos numerados
            lineas = respuesta.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if re.match(r'^\d+\.', linea):
                    titulo = re.sub(r'^\d+\.\s*', '', linea)
                    titulos.append(titulo.strip('"'))
                elif linea and len(titulos) < num_opciones:
                    titulos.append(linea.strip('"'))
            
            self._guardar_en_historial("títulos", contenido[:50] + "...", titulos)
            return titulos[:num_opciones]
            
        except Exception as e:
            return [f"Error al generar títulos: {str(e)}"]
    
    def _guardar_en_historial(self, tipo: str, entrada: str, resultado):
        """
        Guarda la operación en el historial
        """
        self.historial.append({
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "entrada": entrada,
            "resultado": resultado
        })
    
    def obtener_historial(self) -> List[Dict]:
        """
        Obtiene el historial de operaciones
        
        Returns:
            List[Dict]: Lista con el historial de operaciones
        """
        return self.historial
    
    def limpiar_historial(self):
        """
        Limpia el historial de operaciones
        """
        self.historial = []


# Función para usar el asistente de forma interactiva
def main():
    """
    Función principal para demostrar el uso del asistente
    """
    # Inicializar el asistente (asumiendo que api_key está definida)
    asistente = AsistenteEscritura(api_key)
    
    print("=== Asistente de Escritura Automática ===")
    print("¡Bienvenido! Este asistente te ayudará con tus tareas de escritura.")
    print()
    
    while True:
        print("\n--- Opciones disponibles ---")
        print("1. Generar texto completo")
        print("2. Corregir gramática y estilo")
        print("3. Sugerir oraciones para continuar")
        print("4. Analizar estilo del texto")
        print("5. Generar títulos")
        print("6. Ver historial")
        print("7. Limpiar historial")
        print("0. Salir")
        
        opcion = input("\nElige una opción (0-7): ").strip()
        
        if opcion == "0":
            print("¡Gracias por usar el Asistente de Escritura!")
            break
            
        elif opcion == "1":
            tema = input("Tema o idea principal: ")
            tipo = input("Tipo de texto (artículo/correo/novela/ensayo) [artículo]: ") or "artículo"
            longitud = input("Longitud (corto/medio/largo) [medio]: ") or "medio"
            tono = input("Tono (profesional/casual/formal/creativo) [profesional]: ") or "profesional"
            
            print("\nGenerando texto...")
            resultado = asistente.generar_texto(tema, tipo, longitud, tono)
            print("\n--- Texto Generado ---")
            print(resultado)
            
        elif opcion == "2":
            print("Ingresa el texto a corregir (escribe 'FIN' en una línea separada para terminar):")
            lineas = []
            while True:
                linea = input()
                if linea == "FIN":
                    break
                lineas.append(linea)
            texto = "\n".join(lineas)
            
            print("\nCorrigiendo texto...")
            resultado = asistente.corregir_gramatica(texto)
            print("\n--- Texto Corregido ---")
            print(resultado["corregido"])
            print("\n--- Cambios Realizados ---")
            print(resultado["cambios"])
            
        elif opcion == "3":
            print("Ingresa el contexto (escribe 'FIN' en una línea separada para terminar):")
            lineas = []
            while True:
                linea = input()
                if linea == "FIN":
                    break
                lineas.append(linea)
            contexto = "\n".join(lineas)
            
            num_sugerencias = input("¿Cuántas sugerencias quieres? [3]: ") or "3"
            try:
                num_sugerencias = int(num_sugerencias)
            except ValueError:
                num_sugerencias = 3
            
            print("\nGenerando sugerencias...")
            sugerencias = asistente.sugerir_oraciones(contexto, num_sugerencias)
            print("\n--- Sugerencias para continuar ---")
            for i, sugerencia in enumerate(sugerencias, 1):
                print(f"{i}. {sugerencia}")
                
        elif opcion == "4":
            print("Ingresa el texto a analizar (escribe 'FIN' en una línea separada para terminar):")
            lineas = []
            while True:
                linea = input()
                if linea == "FIN":
                    break
                lineas.append(linea)
            texto = "\n".join(lineas)
            
            print("\nAnalizando estilo...")
            resultado = asistente.analizar_estilo(texto)
            
            for clave, valor in resultado.items():
                if clave != "texto_original":
                    print(f"\n--- {clave.upper()} ---")
                    print(valor)
                    
        elif opcion == "5":
            print("Ingresa el contenido para generar títulos (escribe 'FIN' en una línea separada para terminar):")
            lineas = []
            while True:
                linea = input()
                if linea == "FIN":
                    break
                lineas.append(linea)
            contenido = "\n".join(lineas)
            
            num_opciones = input("¿Cuántos títulos quieres? [5]: ") or "5"
            try:
                num_opciones = int(num_opciones)
            except ValueError:
                num_opciones = 5
            
            print("\nGenerando títulos...")
            titulos = asistente.generar_titulo(contenido, num_opciones)
            print("\n--- Títulos Sugeridos ---")
            for i, titulo in enumerate(titulos, 1):
                print(f"{i}. {titulo}")
                
        elif opcion == "6":
            historial = asistente.obtener_historial()
            if historial:
                print("\n--- Historial de Operaciones ---")
                for i, entrada in enumerate(historial, 1):
                    print(f"{i}. {entrada['timestamp']} - {entrada['tipo']}: {entrada['entrada']}")
            else:
                print("\nEl historial está vacío.")
                
        elif opcion == "7":
            asistente.limpiar_historial()
            print("Historial limpiado.")
            
        else:
            print("Opción no válida. Por favor, elige una opción del 0 al 7.")
    
main()