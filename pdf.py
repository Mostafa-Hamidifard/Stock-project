from detection.filter_detection import StockFilter
from fpdf import FPDF
from datetime import date
import pandas as pd
import os
from detection.trend_detection import detect_trend
from Indicator.simple import Simple
from Indicator.normalize import Normalize
from Indicator.bbolinger import BBolinger
from Indicator.moving_average import MovingAverage
from Indicator.macd import MACD
from matplotlib import pyplot as plt


class PDF(FPDF):

    def __init__(self, company_data_list, store_path, filter_string=" ", trend_from=30, howmany=60, initial_header_str="Stock-project Report"):
        FPDF.__init__(self)
        print('start')
        self.header_str = initial_header_str
        self.store_path = store_path
        self.filter_string = filter_string
        self.trend_from = trend_from
        self.howmany = howmany
        self.set_auto_page_break(True, margin=10)
        self.set_title("REPORT")
        self.set_author('Stock project')

        companies_name = [company["<TICKER>"][0]
                          for company in company_data_list]

        self.print_firstpage(companies_name)

        for company_data in company_data_list:
            self.print_company(
                company_data)
        self.print_lastpage(company_data_list)
        self.output(os.path.join(store_path, 'report.pdf'), 'F')
        print('done')

    def print_lastpage(self, companies):
        self.header_str = 'Comparisons'
        self.add_page()

        self.set_font('Times', '', 12)
        true_filters = []
        false_filters = []
        ascends = []
        descends = []
        notrend = []
        for companydf in companies:
            name = companydf['<TICKER>'][0]
            tr, m, c = detect_trend(companydf, self.trend_from, end=True)
            filanswer = ''
            try:
                fil = StockFilter(companydf, self.filter_string)
                filanswer = fil.answer
            except:
                filanswer = "invalid"
            if(filanswer == 'invalid'):
                pass
            elif filanswer == True:
                true_filters.append(name)
            else:
                false_filters.append(name)
            if tr == 'Ascending':
                ascends.append(name)
            elif tr == 'Descending':
                descends.append(name)
            else:
                notrend.append(name)
        self.cell(w=0, h=7, txt='Ascending List:', ln=1)
        i = 1
        for name in ascends:
            start = self.get_x()
            self.cell(w=0, h=7, txt=name)
            self.cell(w=60+start-self.get_x(), h=7)
            if i % 3 == 0:
                self.ln(7)
            i += 1
        self.ln(12)

        self.cell(w=0, h=7, txt='descending List:', ln=1)
        i = 1
        for name in descends:
            start = self.get_x()
            self.cell(w=0, h=7, txt=name)
            self.cell(w=60+start-self.get_x(), h=7)
            if i % 3 == 0:
                self.ln(7)
            i += 1
        self.ln(12)

        self.cell(
            w=0, h=7, txt=f'Companies which satisfy the filter {self.filter_string} :', ln=1)
        i = 1
        for name in true_filters:
            start = self.get_x()
            self.cell(w=0, h=7, txt=name)
            self.cell(w=60+start-self.get_x(), h=7)
            if i % 3 == 0:
                self.ln(7)
            i += 1
        self.ln(12)
        self.cell(
            w=0, h=7, txt='Companies which don\'t satisfy the filter {self.filter_string} :', ln=1)
        i = 1
        for name in false_filters:
            start = self.get_x()
            self.cell(w=0, h=7, txt=name)
            self.cell(w=60+start-self.get_x(), h=7)
            if i % 3 == 0:
                self.ln(7)
            i += 1
        self.ln(12)

    def print_graphs(self, comdf, price_type="<LAST>"):
        self.set_font('Times', '', 12)
        graphs = {}
        graphs["MACD"] = MACD(comdf, price_type)
        graphs["Moving Average"] = MovingAverage(comdf, price_type=price_type)
        graphs["Bollinger Band"] = BBolinger(comdf, price_type=price_type)
        graphs["Normalized"] = Normalize(comdf, price_type)
        graphs["Simple"] = Simple(comdf, price_type)
        paths = {}
        for key, value in graphs.items():
            fig = plt.figure(1, figsize=(5, 3), dpi=150,
                             edgecolor='k')  # we should correct it
            ax1 = fig.add_axes([0.125, 0.125, 0.8, 0.8])
            value.plot(ax1)
            ax1.grid()
            name = comdf['<TICKER>'][0].replace('*', '_').replace(".", '_')
            p1 = os.path.join(self.store_path, 'images')
            if(os.path.exists(p1) == 0):
                os.makedirs(p1)
            p1 = os.path.join(p1, f"{name}__{key}.png")
            paths[key] = p1
            fig.savefig(p1, format='PNG')
            plt.cla()
            plt.clf()
            plt.close()
        for key, image_path in paths.items():
            self.ln(4)
            self.cell(w=0, h=10, txt=f'{key} Chart:', ln=1)
            self.image(image_path, w=185, type='PNG')
            self.ln(4)
        for i in range(0, 185):
            self.cell(w=1, h=7, txt='-')
        self.ln(10)

    def print_answers(self, comdf, filter, trend):
        self.set_font('Times', '', 12)
        tr, m, c = detect_trend(comdf, trend, end=True)
        filanswer = ''
        try:
            fil = StockFilter(comdf, filter)
            filanswer = fil.answer
        except:
            filanswer = "invalid"
        self.multi_cell(
            0, 7, f"Answer of Filter [{filter}] is {filanswer}")
        self.cell(w=0, h=7, txt=f"price graph in last {trend} days: {tr}")

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
        # tabular text
        i = 1
        for name in company_name_list:
            start = self.get_x()
            self.cell(w=0, h=7, txt=name)
            self.cell(w=60+start-self.get_x(), h=7)
            if i % 3 == 0:
                self.ln(7)
            i += 1

    def print_company(self, comdf, price_type='<LAST>'):
        self.header_str = "Company Details"
        self.add_page()
        # a beautiful section which show company name
        self.print_company_title(comdf["<TICKER>"][0])

        # this is remained

        self.print_graphs(comdf[-self.howmany:], price_type)
        self.print_answers(comdf, self.filter_string, self.trend_from)


if __name__ == '__main__':
    data_path_folder = "E:\\ap_final\\Stock-project\\resources\\CSV raw data"
    files = os.listdir(data_path_folder)
    all_companies_data = []
    for f in files:
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(data_path_folder, f))[::-1]
            all_companies_data.append(df)

    pdf = PDF(all_companies_data, os.getcwd(), "p[2]>p[1]")
