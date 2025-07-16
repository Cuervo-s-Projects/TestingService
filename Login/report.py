from tests.test_login import test_login_invalid, test_login_success
from tests.test_jwt import test_valid_token, test_invalid_token
from tests.test_type_user import test_type_user
from tests.test_username import test_username_found, test_username_not_found
from tests.test_signup import test_signup_success, test_signup_password_mismatch, test_signup_password_least_characters, test_signup_password_lowercase_letter, test_signup_password_uppercase_letter, test_signup_password_number, test_signup_special_character
from tests.test_delete import test_delete_success, test_delete_invalid

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Reporte de Pruebas", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def add_test(self, test_results):
        for result in test_results:
            name = result['name']
            status = result['status']
            code = result['code']
            response = result['response']
            duration = result.get('duration', 0)

            color = {
                "PASSED": (0, 100, 0),
                "FAILED": (200, 0, 0)
            }.get(status, (0, 0, 0))

            self.set_text_color(*color)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, f"[{status}] {name} (Code: {code}, Tiempo:{duration}s)", ln=True)

            self.set_text_color(0, 0, 0)
            self.set_font("Arial", "", 10)
            preview = str(response)[:80]
            self.multi_cell(0, 5, f"Response: {preview}")
            self.ln(3)

    def add_summary(self, test_results):
        total = len(test_results)
        passed = sum(1 for r in test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in test_results if r['status'] == 'FAILED')

        self.set_font("Arial", "B", 12)
        self.ln(10)
        self.cell(0, 10, "Resumen Final:", ln=True)

        self.set_font("Arial", "", 11)
        self.set_text_color(0, 100, 0)
        self.cell(0, 8, f"PASSED: {passed}", ln=True)

        self.set_text_color(200, 0, 0)
        self.cell(0, 8, f"FAILED: {failed}", ln=True)

        self.set_text_color(0, 0, 0)
        self.cell(0, 8, f"TOTAL: {total}", ln=True)

pdf = PDF()
pdf.add_page()

results = []

test_signup_success(results)
test_signup_password_mismatch(results)
test_signup_password_least_characters(results)
test_signup_password_lowercase_letter(results)
test_signup_password_uppercase_letter(results)
test_signup_password_number(results)
test_signup_special_character(results)
test_login_success(results)
test_login_invalid(results)
test_valid_token(results)
test_invalid_token(results)
test_type_user(results)
test_username_found(results)
test_username_not_found(results)
test_delete_success(results)
test_delete_invalid(results)

pdf.add_test(results)
pdf.add_summary(results)

path = os.getcwd()
if "Login" in path:
    dr='\\'
    new_folder = 'reports'
    new_path = path + dr  + new_folder
else:
    dr='\\'
    folder = 'Login'
    new_folder = 'reports'
    new_path = path + dr + folder + dr  + new_folder

if not os.path.exists(new_path):
    os.makedirs(new_path)

dirs = os.listdir(new_path)
num = 0
for item in dirs:
    if os.path.isfile(new_path + dr + item):
        num+=1
        
pdf_filename = os.path.join(new_path, f"Report_{num}.pdf")

pdf.output(pdf_filename)
print("PDF generado")