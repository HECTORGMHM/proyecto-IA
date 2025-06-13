proyecto-IA
proyecto final de la materia Inteligencia Artificial
Teclado Virtual QWERTY con Control por Gestos  

Un teclado innovador que detecta tus gestos para escribir sin contacto físico, usando solo una cámara web y visión por computadora.

<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcW0yY2VqY2N6d2VjZGNjZ3BneHZ5Y2VtY2RlZ3BhdmJ6eGZ5eGZ5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7qE1YN7aBOFPRw8E/giphy.gif" width="400" alt="Demo">
  <p><em>¡Escribe con solo mover tus dedos!</em></p>
</div>

Características Principales  

- Reconocimiento preciso de gestos  
  Detecta dedos extendidos usando algoritmos de visión por computadora (OpenCV)  

- Diseño QWERTY optimizado  
  Teclas distribuidas ergonómicamente con retroalimentación visual  

- Bajo requerimiento de hardware  
  Funciona con cámaras web estándar (720p o superior recomendado)  

- Fácil integración  
  Opción para emular entrada de teclado físico (requiere `pyautogui`)  

Requisitos  

```bash
pip install opencv-python numpy  # Versión básica
pip install pyautogui keyboard   # Para emulación de teclado (opcional)
```

Cómo Usarlo  

1. Calibración inicial (5 segundos):  
   Mantén tu mano dentro del área roja hasta que aparezca el mensaje "LISTO"  

2. Modo escritura:  
   - Extiende 1 dedo para seleccionar teclas  
   - Mueve tu mano para navegar por el teclado  
   - La tecla presionada se iluminará en verde  

3. Teclas especiales:  
   - Barra espaciadora: Área inferior central  
   - Borrar (`<-`): Esquina inferior derecha  

```python
python teclado_virtual.py  # Ejecuta el modo básico
python teclado_emulador.py  # Versión con emulación de teclado real
```

Estructura del Código  

```
/project
├── main.py                  # Lógica principal de detección
├── teclado.py               # Renderizado del interfaz QWERTY
├── gestos.py                # Algoritmos de reconocimiento
└── utils/                   # Funciones auxiliares
    ├── calibracion.py       # Ajuste automático de iluminación  
    └── feedback.py          # Efectos visuales y sonoros
```

Casos de Uso  

- **Entornos médicos:** Quirófanos, laboratorios  
- **Accesibilidad:** Personas con movilidad reducida  
- **Kioskos interactivos:** Museos, exposiciones  
- **Control por gestos:** Presentaciones, realidad aumentada  

Limitaciones y Mejoras Futuras  

| Limitación Actual          | Solución Propuesta          |
|----------------------------|-----------------------------|
| Sensibilidad a luz variable| Usar filtro de histograma   |
| Latencia (~200ms)          | Optimizar con C++/CUDA      |
| Sin soporte multitouch     | Integrar MediaPipe Hands    |

Cómo Contribuir  

1. Haz fork del proyecto  
2. Crea una rama (`git checkout -b feature/nueva-funcion`)  
3. Haz commit de tus cambios (`git commit -m 'Add some feature'`)  
4. Haz push a la rama (`git push origin feature/nueva-funcion`)  
5. Abre un Pull Request  

Licencia  

MIT © [HECTOR GAEL MORALES MORENO] - ¡Usa, modifica y comparte libremente!  

---

<div align="center">
  <a href="https://youtu.be/demo-link">🎥 Video Demo</a> • 
  <a href="https://github.com/tuusuario/teclado-virtual/issues">🐛 Reportar Bug</a> • 
  <a href="mailto:tu@email.com">✉️ Contacto</a>
</div>

---

Ejemplo de Uso en Código  

```python
from teclado import VirtualKeyboard
from gestos import HandDetector

# Inicializa componentes
detector = HandDetector()
teclado = VirtualKeyboard(layout="QWERTY")

while True:
    frame = camara.obtener_frame()
    dedos = detector.contar_dedos(frame)
    tecla = teclado.detectar_presion(dedos)
    
    if tecla == "<-":
        texto = texto[:-1]  # Borrar
    else:
        texto += tecla     # Escribir
```

¡Convierte cualquier superficie en un teclado con solo tu mano!
