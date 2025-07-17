from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import green, red, black, blue
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import time
import os

class TestResult:
    """Clase para almacenar los resultados del test"""
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None
        self.status = "PENDING"
        self.test_data = {}
        self.steps = []
        self.errors = []
        self.final_url = ""
        self.screenshot_path = ""
        self.success_messages = []
        self.error_messages = []
    
    def add_step(self, step_name, status, details=""):
        """Añadir un paso del test"""
        self.steps.append({
            "name": step_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now()
        })
    
    def add_error(self, error_msg):
        """Añadir un error"""
        self.errors.append({
            "message": error_msg,
            "timestamp": datetime.now()
        })
    
    def set_final_status(self, status):
        """Establecer el estado final del test"""
        self.status = status
        self.end_time = datetime.now()
    
    def get_duration(self):
        """Obtener la duración del test"""
        if self.end_time:
            return self.end_time - self.start_time
        return datetime.now() - self.start_time

def create_pdf_report(test_result, output_dir="../reports/"):
    """Crear reporte PDF con los resultados del test"""
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Nombre del archivo
    timestamp = test_result.start_time.strftime("%Y%m%d_%H%M%S")
    filename = f"signup_test_report_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Crear documento PDF
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Centrado
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    
    # Título del reporte
    story.append(Paragraph("REPORTE DE TEST - FLUJO DE REGISTRO", title_style))
    story.append(Spacer(1, 12))
    
    # Información general
    story.append(Paragraph("INFORMACIÓN GENERAL", subtitle_style))
    
    general_info = [
        ["Fecha de inicio:", test_result.start_time.strftime("%Y-%m-%d %H:%M:%S")],
        ["Fecha de fin:", test_result.end_time.strftime("%Y-%m-%d %H:%M:%S") if test_result.end_time else "N/A"],
        ["Duración:", str(test_result.get_duration())],
        ["Estado final:", test_result.status],
        ["URL final:", test_result.final_url]
    ]
    
    general_table = Table(general_info, colWidths=[2*inch, 4*inch])
    general_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(general_table)
    story.append(Spacer(1, 20))
    
    # Datos del test
    if test_result.test_data:
        story.append(Paragraph("DATOS UTILIZADOS EN EL TEST", subtitle_style))
        
        test_data_info = []
        for key, value in test_result.test_data.items():
            # Ocultar contraseñas en el reporte
            if "password" in key.lower():
                value = "***********"
            test_data_info.append([key.replace("_", " ").title() + ":", str(value)])
        
        test_data_table = Table(test_data_info, colWidths=[2*inch, 4*inch])
        test_data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(test_data_table)
        story.append(Spacer(1, 20))
    
    # Pasos del test
    story.append(Paragraph("PASOS EJECUTADOS", subtitle_style))
    
    steps_data = [["Paso", "Estado", "Detalles", "Tiempo"]]
    for i, step in enumerate(test_result.steps, 1):
        status_color = "✅" if step["status"] == "SUCCESS" else "❌" if step["status"] == "FAILED" else "⏳"
        steps_data.append([
            f"{i}. {step['name']}",
            f"{status_color} {step['status']}",
            step['details'][:50] + "..." if len(step['details']) > 50 else step['details'],
            step['timestamp'].strftime("%H:%M:%S")
        ])
    
    steps_table = Table(steps_data, colWidths=[2*inch, 1*inch, 2.5*inch, 0.8*inch])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(steps_table)
    story.append(Spacer(1, 20))
    
    # Mensajes de éxito
    if test_result.success_messages:
        story.append(Paragraph("MENSAJES DE ÉXITO", subtitle_style))
        for msg in test_result.success_messages:
            story.append(Paragraph(f"✅ {msg}", styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Errores encontrados
    if test_result.errors or test_result.error_messages:
        story.append(Paragraph("ERRORES ENCONTRADOS", subtitle_style))
        
        all_errors = []
        for error in test_result.errors:
            all_errors.append(f"❌ {error['message']}")
        for error_msg in test_result.error_messages:
            all_errors.append(f"❌ {error_msg}")
        
        for error in all_errors:
            story.append(Paragraph(error, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Resumen final
    story.append(Paragraph("RESUMEN", subtitle_style))
    
    total_steps = len(test_result.steps)
    successful_steps = len([s for s in test_result.steps if s["status"] == "SUCCESS"])
    failed_steps = len([s for s in test_result.steps if s["status"] == "FAILED"])
    
    summary_text = f"""
    <b>Total de pasos ejecutados:</b> {total_steps}<br/>
    <b>Pasos exitosos:</b> {successful_steps}<br/>
    <b>Pasos fallidos:</b> {failed_steps}<br/>
    <b>Tasa de éxito:</b> {(successful_steps/total_steps)*100:.1f}% (si total > 0)<br/>
    <b>Estado final del test:</b> {test_result.status}
    """
    
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Información adicional
    if test_result.screenshot_path:
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Screenshot guardado en:</b> {test_result.screenshot_path}", styles['Normal']))
    
    # Generar PDF
    doc.build(story)
    
    return filepath

def test_signup_flow():
    """Test - flujo de registro con generación de reporte PDF"""
    
    # Inicializar objeto de resultados
    result = TestResult()
    
    # Configurar navegador
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # para ejecutar sin ventana
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        print("Iniciando test de registro...")
        result.add_step("Inicialización del test", "SUCCESS", "Navegador Chrome iniciado correctamente")
        
        # 1. Abrir la página
        print("Abriendo http://localhost:3000/")
        driver.get("http://localhost:3000/")
        driver.maximize_window()
        time.sleep(2)
        result.add_step("Abrir página principal", "SUCCESS", "Página cargada: http://localhost:3000/")
        
        # 2. Buscar botón "Registrarse" (puede estar visible directamente o en menú móvil)
        print("Buscando botón de Registrarse...")
        try:
            signup_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/signup']")))
            signup_button.click()
            print("✅ Botón 'Registrarse' clickeado")
            result.add_step("Acceder a página de registro", "SUCCESS", "Botón encontrado y clickeado")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")
            result.add_step("Acceder a página de registro", "FAILED", f"Error: {str(e)}")
            raise
        
        # 3. Verificar que estamos en la página de signup
        print("Verificando que estamos en la página de signup...")
        try:
            # Esperar un momento para que la página cargue
            time.sleep(2)
    
            current_url = driver.current_url
            expected_url = "http://localhost:3000/signup"
    
            print(f"URL actual: {current_url}")
            print(f"URL esperada: {expected_url}")
    
            if current_url == expected_url:
                print("✅ Estamos en la página de signup correcta")
                result.add_step("Verificar página de signup", "SUCCESS", f"URL correcta: {current_url}")
            else:
                raise Exception(f"URL incorrecta. Esperada: {expected_url}, Actual: {current_url}")
        
        except Exception as e:
            print(f"❌ Error verificando página de signup: {e}")
            result.add_step("Verificar página de signup", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error verificando página de signup: {str(e)}")
            raise

        # 4. Llenar formulario de registro
        print("Llenando formulario de registro...")

        # Datos mock para el registro
        test_data = {
            "Nombre": "Juan",
            "Apellido": "Pérez", 
            "Edad": "25",
            "Fecha de nacimiento": "01-05-2000",
            "Correo electrónico": f"juan.perez.{int(time.time())}@test.com",
            "Nombre de usuario": f"juanperez_{int(time.time())}",
            "Contraseña": "MiPassword123!",
            "Repetir contraseña": "MiPassword123!"
        }

        result.test_data = test_data

        # Llenar cada campo usando el placeholder
        for placeholder, valor in test_data.items():
            try:
                print(f"Llenando campo '{placeholder}' con valor: {valor}")
                campo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")))
                campo.clear()
                campo.send_keys(valor)
                print(f"✅ Campo '{placeholder}' llenado correctamente")
                result.add_step(f"Llenar campo '{placeholder}'", "SUCCESS", f"Valor: {valor}")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Error llenando campo '{placeholder}': {e}")
                result.add_step(f"Llenar campo '{placeholder}'", "FAILED", f"Error: {str(e)}")
                result.add_error(f"Error llenando campo '{placeholder}': {str(e)}")

        print("✅ Formulario completado")
        # 5. Hacer clic en "Crear cuenta"
        try:
            # Hacer scroll hacia abajo
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)
            result.add_step("Scroll hacia abajo", "SUCCESS", "Scroll realizado correctamente")
            print("✅ Scroll realizado")
        except Exception as e:
            result.add_step("Scroll hacia abajo", "FAILED", f"Error: {str(e)}")
            print(f"⚠️ Error en scroll: {e}")
        print("Buscando y seleccionando 'Crear cuenta'...")
        try:
            create_account_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.signup-button")))
            create_account_button.click()
            print("✅ 'Crear cuenta' seleccionado")
            result.add_step("Enviar formulario", "SUCCESS", "Botón 'Crear cuenta' clickeado")
        except Exception as e:
            result.add_step("Enviar formulario", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error enviando formulario: {str(e)}")
            raise
        
        # 6. Esperar respuesta del servidor
        print("Esperando respuesta del servidor...")
        time.sleep(3)

        # Verificar registro exitoso
        print("Verificando resultado del registro...")
        try:
            # Buscar el mensaje de éxito específico
            success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.signup-message")))
    
            if success_message.is_displayed():
                message_text = success_message.text
                print(f"✅ REGISTRO EXITOSO: {message_text}")
                result.success_messages.append(message_text)
                result.set_final_status("SUCCESS")
                result.add_step("Verificar resultado", "SUCCESS", f"Mensaje: {message_text}")
            else:
                raise Exception("Mensaje de éxito no visible")
        
        except Exception as e:
            print(f"❌ No se encontró mensaje de éxito: {e}")
            result.set_final_status("FAILED")
            result.add_step("Verificar resultado", "FAILED", f"No se encontró mensaje de éxito: {str(e)}")
            result.add_error(f"No se encontró mensaje de éxito: {str(e)}")

        # Mostrar URL final para referencia
        current_url = driver.current_url
        result.final_url = current_url
        print(f"URL final: {current_url}")

        print("Resumen del test:")
        print(f"   - Estado: {result.status}")
        print(f"   - URL final: {current_url}")
        print(f"   - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if result.status == "SUCCESS":
            print("✅ TEST COMPLETADO EXITOSAMENTE")
        else:
            print("❌ TEST FALLÓ")
        
        
        # Verificar por cambio de URL
        if "signup" not in current_url:
            print("✅ Se redirigió fuera de la página de registro")
        elif "signup" in current_url:
            print("⚠️ Aún en página de registro - verificar errores")
        
        print("Resumen del test:")
        print(f"   - Datos utilizados: {test_data}")
        print(f"   - URL final: {current_url}")
        print(f"   - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        result.set_final_status("ERROR")
        result.add_error(f"Error general: {str(e)}")
        
        # Tomar screenshot en caso de error
        screenshot_name = f"signup_error_{int(time.time())}.png"
        screenshot_path = os.path.join("../reports/", screenshot_name)
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        result.screenshot_path = screenshot_path
        print(f"Screenshot guardado: {screenshot_path}")
        
    finally:
        # Generar reporte PDF
        try:
            pdf_path = create_pdf_report(result)
            print(f"REPORTE PDF GENERADO: {pdf_path}")
        except Exception as e:
            print(f"❌ Error generando reporte PDF: {e}")
        
        # Mantener navegador abierto por 5 segundos para ver resultado
        print("Manteniendo navegador abierto 5 segundos...")
        time.sleep(5)
        driver.quit()
        print("Test completado")

if __name__ == "__main__":
    test_signup_flow()