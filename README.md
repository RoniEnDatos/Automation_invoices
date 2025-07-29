# 📊 Automatización de Facturas con Python y Google Sheets

Este proyecto permite subir automáticamente facturas a una base de datos en Google Sheets.

🔧 **Tecnologías utilizadas**:
- Python
- Google Sheets API
- Librerías como `gspread`, `pandas`, entre otras

📁 **Estructura de carpetas**:
- `invoices/`: aquí colocarás las facturas nuevas (en formato `.pdf` o `.xml`)
- `processed_invoices/`: las facturas ya procesadas se moverán aquí automáticamente

📌 **Requisitos previos**:
- Crear un archivo `credentials.json` con tus credenciales de Google Service Account
- Activar la API de Google Sheets en tu proyecto de Google Cloud
- Instalar las dependencias con `pip install -r requirements.txt`

📚 **Lo que aprenderás**:
- Manejo de archivos y carpetas con Python
- Automatización de procesos con scripts
- Uso avanzado de APIs con autenticación
