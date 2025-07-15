from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        if os.path.exists('media/logo_universidad.png'):
            self.image('media/logo_universidad.png', 10, 8, 33)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Reporte de Prueba de Integración', border=False, ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_metadata(self, test_name, date):
        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Nombre de la prueba:', 0, 0)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, test_name, ln=1)

        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Fecha:', 0, 0)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, date, ln=1)
        self.ln(10)

    def add_steps(self, steps):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Pasos realizados:', ln=1)
        self.set_font('Arial', '', 11)
        for i, step in enumerate(steps, start=1):
            self.multi_cell(0, 10, f'{i}. {step}')
        self.ln(5)

    def add_result_summary(self, success):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 100, 0) if success else self.set_text_color(180, 0, 0)
        resultado = 'Prueba exitosa' if success else 'Prueba fallida'
        self.cell(0, 10, f'Resultado: {resultado}', ln=1)
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def add_chart(self, steps):
        # Crear gráfico
        success = [1 for step in steps if not str(step).lower().startswith('error')]
        fails = len(steps) - len(success)

        labels = ['Exitosos', 'Fallidos']
        values = [len(success), fails]
        colors = ['#4caf50', '#f44336']

        plt.figure(figsize=(4, 3))
        plt.bar(labels, values, color=colors)
        plt.title('Resumen de pasos')
        plt.tight_layout()

        chart_path = 'media/chart.png'
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)  # ← agrega esto

        plt.savefig(chart_path)
        plt.close()

        # Agregar imagen al PDF
        self.image(chart_path, x=60, w=90)
        self.ln(10)

    

def generar_reporte(nombre_prueba, pasos, exitoso):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nombre_pdf = f'reports/reporte_{nombre_prueba.replace(" ", "_").lower()}.pdf'

    pdf = PDFReport()
    pdf.add_page()
    pdf.add_metadata(nombre_prueba, fecha_actual)
    pdf.add_steps(pasos)
    pdf.add_chart(pasos)
    pdf.add_result_summary(exitoso)

    os.makedirs(os.path.dirname(nombre_pdf), exist_ok=True)
    pdf.output(nombre_pdf)
    print(f'✅ Reporte generado en: {nombre_pdf}')
