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
    filename = f"login_test_report_{timestamp}.pdf"
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
    story.append(Paragraph("REPORTE DE TEST - FLUJO DE LOGIN", title_style))
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
            if "password" in key.lower() or "contraseña" in key.lower():
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

def test_login_flow():
    """Test - flujo de login con generación de reporte PDF"""
    
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
        print("Iniciando test de login...")
        result.add_step("Inicialización del test", "SUCCESS", "Navegador Chrome iniciado correctamente")
        
        # 1. Abrir la página
        print("Abriendo http://localhost:3000/")
        driver.get("http://localhost:3000/")
        driver.maximize_window()
        time.sleep(2)
        result.add_step("Abrir página principal", "SUCCESS", "Página cargada: http://localhost:3000/")
        
        # 2. Buscar y clickear botón "Iniciar Sesión"
        print("Buscando botón 'Iniciar Sesión'...")
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']")))
            login_button.click()
            print("✅ Botón 'Iniciar Sesión' clickeado")
            result.add_step("Acceder a página de login", "SUCCESS", "Botón 'Iniciar Sesión' encontrado y clickeado")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")
            result.add_step("Acceder a página de login", "FAILED", f"Error: {str(e)}")
            raise
        
        # 3. Verificar que estamos en la página de login
        print("Verificando que estamos en la página de login...")
        try:
            time.sleep(2)
            current_url = driver.current_url
            expected_url = "http://localhost:3000/login"
            
            print(f"URL actual: {current_url}")
            print(f"URL esperada: {expected_url}")
            
            if current_url == expected_url:
                print("✅ Estamos en la página de login correcta")
                result.add_step("Verificar página de login", "SUCCESS", f"URL correcta: {current_url}")
            else:
                raise Exception(f"URL incorrecta. Esperada: {expected_url}, Actual: {current_url}")
                
        except Exception as e:
            print(f"❌ Error verificando página de login: {e}")
            result.add_step("Verificar página de login", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error verificando página de login: {str(e)}")
            raise

        # 4. Llenar formulario de login
        print("Llenando formulario de login...")

        # Datos mock para el login
        test_data = {
            "Correo": "juan.perez.1752721587@test.com",
            "Contraseña": "MiPassword123!"
        }

        result.test_data = test_data

        # Paso 1: Llenar campo "Correo"
        try:
            print(f"Llenando campo 'Correo' con: {test_data['Correo']}")
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Correo']")))
            email_field.clear()
            email_field.send_keys(test_data['Correo'])
            print("✅ Campo 'Correo' llenado correctamente")
            result.add_step("Llenar campo 'Correo'", "SUCCESS", f"Valor: {test_data['Correo']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error llenando campo 'Correo': {e}")
            result.add_step("Llenar campo 'Correo'", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error llenando campo 'Correo': {str(e)}")
            raise

        # Paso 2: Llenar campo "Contraseña"
        try:
            print(f"Llenando campo 'Contraseña'")
            password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Contraseña']")))
            password_field.clear()
            password_field.send_keys(test_data['Contraseña'])
            print("✅ Campo 'Contraseña' llenado correctamente")
            result.add_step("Llenar campo 'Contraseña'", "SUCCESS", "Contraseña ingresada")
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error llenando campo 'Contraseña': {e}")
            result.add_step("Llenar campo 'Contraseña'", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error llenando campo 'Contraseña': {str(e)}")
            raise

        print("✅ Formulario de login completado")
        
        # 5. Hacer clic en botón "Iniciar Sesión"
        print("Buscando y clickeando botón 'Iniciar Sesión'...")
        try:
            login_submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login-button")))
            login_submit_button.click()
            print("✅ Botón 'Iniciar Sesión' clickeado")
            result.add_step("Enviar formulario de login", "SUCCESS", "Botón 'Iniciar Sesión' clickeado")
        except Exception as e:
            print(f"❌ Error clickeando botón 'Iniciar Sesión': {e}")
            result.add_step("Enviar formulario de login", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Error enviando formulario de login: {str(e)}")
            raise
        
        # 6. Esperar respuesta del servidor
        print("Esperando respuesta del servidor...")
        time.sleep(3)

        # 7. Verificar login exitoso
        print("Verificando resultado del login...")
        try:
            # Verificar por cambio de URL (redirección después de login exitoso)
            current_url = driver.current_url
            result.final_url = current_url
            
            if "login" not in current_url:
                print(f"✅ LOGIN EXITOSO - Redirigido a: {current_url}")
                result.success_messages.append(f"Login exitoso - Redirigido a: {current_url}")
                result.set_final_status("SUCCESS")
                result.add_step("Verificar login exitoso", "SUCCESS", f"Redirigido a: {current_url}")
            else:
                # Si seguimos en la página de login, buscar mensajes de error
                try:
                    # Buscar posibles mensajes de error
                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error-message, .alert-danger, .login-error")
                    if error_elements:
                        error_text = error_elements[0].text
                        raise Exception(f"Error de login: {error_text}")
                    else:
                        raise Exception("Aún en página de login - posible error de autenticación")
                except Exception as inner_e:
                    raise Exception(f"Login falló - {str(inner_e)}")
        
        except Exception as e:
            print(f"❌ Login falló: {e}")
            result.set_final_status("FAILED")
            result.add_step("Verificar login exitoso", "FAILED", f"Error: {str(e)}")
            result.add_error(f"Login falló: {str(e)}")

        # Mostrar resumen
        print("\nResumen del test:")
        print(f"   - Estado: {result.status}")
        print(f"   - Datos utilizados: {test_data}")
        print(f"   - URL final: {result.final_url}")
        print(f"   - Duración: {result.get_duration()}")
        print(f"   - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if result.status == "SUCCESS":
            print("✅ TEST DE LOGIN COMPLETADO EXITOSAMENTE")
        else:
            print("❌ TEST DE LOGIN FALLÓ")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        result.set_final_status("ERROR")
        result.add_error(f"Error general: {str(e)}")
        
        # Tomar screenshot en caso de error
        screenshot_name = f"login_error_{int(time.time())}.png"
        screenshot_path = os.path.join("../reports/", screenshot_name)
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        result.screenshot_path = screenshot_path
        print(f"Screenshot guardado: {screenshot_path}")
        
    finally:
        # Generar reporte PDF
        try:
            pdf_path = create_pdf_report(result)
            print(f"📄 REPORTE PDF GENERADO: {pdf_path}")
        except Exception as e:
            print(f"❌ Error generando reporte PDF: {e}")
        
        # Mantener navegador abierto por 5 segundos para ver resultado
        print("Manteniendo navegador abierto 5 segundos...")
        time.sleep(5)
        driver.quit()
        print("Test de login completado")

if __name__ == "__main__":
    test_login_flow()