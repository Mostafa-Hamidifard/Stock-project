import pandas as pd


class StockFilter:
    def __init__(self, raw_data, filter_str, price_type="<CLOSE>"):
        self.raw_data = raw_data[::-1]
        self.filter_str = filter_str
        self.price = self.raw_data[price_type].values
        self.volume = self.raw_data["<VOL>"].values
        try:
            self.answer = self.process_filter()
        except:
            self.answer = "invalid"
            raise ValueError

    def process_filter(self):
        txt = self.filter_str
        temp = self.filter_str
        temp = temp.lower().strip()
        self.PindexL = []
        self.PindexR = []
        self.VindexL = []
        self.VindexR = []

        ge = temp.find(">=")
        le = temp.find("<=")
        eq = temp.find("=")
        gt = temp.find(">")
        lt = temp.find("<")
        if ge != -1:
            self.tl = txt.split(">=")[0]
            self.ql = self.tl.split("]")
            self.tr = txt.split(">=")[1]
            self.qr = self.tr.split("]")
            return self.LHS() >= self.RHS()

        elif le != -1:
            self.tl = txt.split("<=")[0]
            self.ql = self.tl.split("]")
            self.tr = txt.split("<=")[1]
            self.qr = self.tr.split("]")
            return self.LHS() <= self.RHS()

        elif eq != -1:
            self.tl = txt.split("=")[0]
            self.ql = self.tl.split("]")
            self.tr = txt.split("=")[1]
            self.qr = self.tr.split("]")
            return self.LHS() == self.RHS()

        elif gt != -1:
            self.tl = txt.split(">")[0]
            self.ql = self.tl.split("]")
            self.tr = txt.split(">")[1]
            self.qr = self.tr.split("]")
            return self.LHS() > self.RHS()

        elif lt != -1:
            self.tl = txt.split("<")[0]
            self.ql = self.tl.split("]")
            self.tr = txt.split("<")[1]
            self.qr = self.tr.split("]")
            return self.LHS() < self.RHS()

    def LHS(self):

        for i in self.ql[:-1]:
            if i.find("p") != -1:
                self.PindexL.append(int((i[i.find("p") + 2:])))
            if i.find("v") != -1:
                self.VindexL.append(int((i[i.find("v") + 2:])))

        for i in self.PindexL:
            self.tl = self.tl.replace(f"p[{i}]", f"{self.price[i]}")
        for i in self.VindexL:
            self.tl = self.tl.replace(f"v[{i}]", f"{self.volume[i]}")

        return eval(self.tl)

    def RHS(self):

        for i in self.qr[:-1]:
            if i.find("p") != -1:
                self.PindexR.append(int((i[i.find("p") + 2:])))
            if i.find("v") != -1:
                self.VindexR.append(int((i[i.find("v") + 2:])))

        for i in self.PindexR:
            self.tr = self.tr.replace(f"p[{i}]", f"{self.price[i]}")
        for i in self.VindexR:
            self.tr = self.tr.replace(f"v[{i}]", f"{self.volume[i]}")

        return eval(self.tr)


if __name__ == "__main__":

    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")
    df = df[::-1]

    txt = "-p[2]+3*p[22]-v[5]<=-2*v[2]+p[21]-p[5]+v[5]"

    sf = StockFilter(df, txt)
    print(sf.answer)

    # print(sf.ql)
    # print(sf.qr)
    # print(sf.PindexL)
    # print(sf.VindexL)
    # print(sf.PindexR)
    # print(sf.VindexR)
