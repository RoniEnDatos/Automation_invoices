import PyPDF2
import re
import os
from google_sheets import GoogleSheet
import uuid

def generate_uid():
    unique_id = uuid.uuid4()
    unique_id_str = str(unique_id)
    return unique_id_str

def extract_invoice_info(pdf_file_path):
    # Abrir el archivo PDF en modo lectura binaria
    with open(pdf_file_path, 'rb') as file:
        # Crear el lector de PDF
        pdf_reader = PyPDF2.PdfReader(file)

        # Variable para almacenar el texto extraído
        texto = ''

        # Recorrer cada página del PDF y extraer el texto
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto += page.extract_text()
         
        razon_social = re.search(r'^\s*(\S.+?)\s*$', texto, re.MULTILINE).group(1)

        # CLIENTE
        cliente = re.search(r'Señor\(es\)\s*:(.+)', texto).group(1).strip()

        # FECHA DE EMISIÓN
        fecha_emision = re.search(r'Fecha de Emisión\s*:(\d{2}/\d{2}/\d{4})', texto).group(1)

        # DESCRIPCIÓN DEL SERVICIO (línea después de código de producto)
        descripcion_match = re.search(
            r'Descripción\s*\n((?:.(?!\d+\.\d{2}\s+UNIDAD).)*?)\n',
            texto, re.DOTALL
        )
        descripcion_match = re.search(r"\d+\.\d{2}\s+UNIDAD\s+\S+\s+([\s\S]*?)\s+\d+\.\d{2}\s+\d+\.\d{2}", texto)
        descripcion = descripcion_match.group(1).strip().replace('\n', ' ') if descripcion_match else "No encontrado"
        # IMPORTE TOTAL
        importe_total = re.search(r'Importe Total\s*:\s*\$\s*([\d.,]+)', texto).group(1)

        # IMPORTE NETO = Importe Total * 0.1 (detracción)
        importe_total_valor = float(importe_total.replace(",", ""))
        importe_neto = round(importe_total_valor-importe_total_valor * 0.1, 2)

        
        return razon_social,cliente,fecha_emision,descripcion,importe_total,importe_neto


razon_social,cliente,fecha_emision,descripcion,importe_total,importe_neto= extract_invoice_info("invoices/PDF-DOC-E00122510107394112.pdf")  # Cambia esto por el nombre de tu archivo

def get_files_folder(folder_path):
    
    files =[]
    # Iterative over all files and subdirector
    for root,dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            #Append the full file path to the list of file
            files.append(os.path.join(root,filename))
    return files

if __name__== "__main__":

    folder_path ='invoices'
    files = get_files_folder(folder_path)
    # save info in google sheets
    uid=generate_uid()
    file_name_gs = 'credentials.json'
    google_sheet = 'Facturas'
    sheet_name = 'nombre'
    google = GoogleSheet(file_name_gs,google_sheet,sheet_name)


    for file in files:
        print('File',file)
        razon_social,cliente,fecha_emision,descripcion,importe_total,importe_neto= extract_invoice_info(file)

        # Print extracted information

        #Imprimir resultados
        print("RAZÓN SOCIAL:", razon_social)
        print("CLIENTE:", cliente)
        print("FECHA DE EMISIÓN:", fecha_emision)
        print("DESCRIPCIÓN DEL SERVICIO:", descripcion)
        print("IMPORTE TOTAL (S/):", importe_total)
        print("IMPORTE NETO (S/):", importe_neto)

        value = [[razon_social,cliente,fecha_emision,descripcion,importe_total,importe_neto,uid]]
        rango = google.get_last_row_range()
        google.write_data(rango,value)