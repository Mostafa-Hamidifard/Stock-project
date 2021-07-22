from fpdf import FPDF
from datetime import date


class PDF(FPDF):
    def __init__(self, initial_header_str="Stock-project Report"):
        self.header_str = initial_header_str
        FPDF.__init__(self)

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(self.header_str) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, self.header_str, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def print_company_title(self, comapny_name):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, f'Company name: {comapny_name}', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def print_firstpage(self, company_name_list):
        self.add_page()
        self.header_str = "Stock-project Report"
        self.set_font('Times', '', 12)
        self.cell(0, 7, f"Today: {date.today()}", ln=1)
        self.cell(0, 7, "This report conatins:", ln=1)
        txt = ''
        i = 1
        for name in company_name_list:
            txt = txt + "   {} {:<25}".format("*", name)
            if i % 4 == 0:
                txt += "\n"
            i += 1
        self.multi_cell(0, 7, txt,)

    def print_graphs(self, graphs):
        self.set_font('Times', '', 12)
        self.cell(0, 7, f"Today: {date.today()}", ln=1)
        pass

    def print_answers(self, filter, trend):
        pass

    def print_company(self, company):
        self.header_str = "Company Details"
        self.add_page()
        # a beautiful section which show company name
        self.print_company_title(company["name"])

        self.print_graphs(company["graphs"])  # this is remained

        self.print_answers(company['filter'], company["trend"])

    def print_lastpage(self, companies):
        pass


pdf = PDF()
pdf.set_auto_page_break(True, margin=10)
pdf.set_title("REPORT")
pdf.set_author('Stock project')

companies = ["babo" for i in range(0, 1000)]
pdf.print_firstpage(companies)

for company in companies:
    pdf.print_company(company)
pdf.print_lastpage(companies)
pdf.output('report.pdf', 'F')
