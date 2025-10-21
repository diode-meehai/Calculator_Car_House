class CalCar:
    def __init__(self):
        print('RunClass_CalCar')


    def CarLoanCalculation(self, CarPrice, DownPrecent, Interest, Year):
        DownPayment = CarPrice * (DownPrecent / 100)  # เงินดาวน์บาท
        Finance = CarPrice - DownPayment  # ยอดจัดไฟแนนซ์
        Interest_To_Year = Finance * (Interest / 100)  # จำนวนดอกเบี้ยรายปี
        Interest_All = Interest_To_Year * Year  # ดอกเบี้ยทั้งหมดที่ต้องจ่าย
        Price_All = Finance + Interest_All  # ยอดทั้งหมดที่ต้องจ่ายจริง
        Pay_Per_Month = Price_All / (Year * 12)  # ค่างวดในแต่ละเดือน

        print('------------ CarLoanCalculation ------------')
        print('เงินดาวน์: ', DownPayment)
        print('ยอดจัดไฟแนนซ์: ', Finance)
        print('จำนวนดอกเบี้ยรายปี: ', Interest_To_Year)
        print('ดอกเบี้ยทั้งหมดที่ต้องจ่าย: ', Interest_All)
        print('ยอดทั้งหมดที่ต้องจ่ายจริง: ', Price_All)
        print('ค่างวดในแต่ละเดือน: ', Pay_Per_Month)
        print('--------------------------------------------')

        return DownPayment, Finance, Interest_To_Year, Interest_All, Price_All, Pay_Per_Month

    def RegisFeeYear(self, CarSizeCC):

        # 1-600 CC = 0.5 สตางค์
        if CarSizeCC > 600:
            CC_SixHundred = 600 * 0.5
        elif CarSizeCC <= 600:
            CC_SixHundred = CarSizeCC * 0.5

        # 601-1800 CC = 1.5 บาท
        if (CarSizeCC-600) > 0:
            CC_ThousandEight = (CarSizeCC - 600) * 1.5
        elif (CarSizeCC-600) <= 0:
            CC_ThousandEight = 0

        # 1800 CC (Up) = 4 บาท
        if (CarSizeCC-(600+1800)) > 0:
            CC_ThousandEightUP = (CarSizeCC -(600+1800)) * 4
        elif (CarSizeCC-(600+1800)) <= 0:
            CC_ThousandEightUP = 0

        Price_RegisFeeYear = CC_SixHundred + CC_ThousandEight + CC_ThousandEightUP

        print('-------------- RegisFeeYear ----------------')
        print('ขนาดรถ (CC): ', CarSizeCC)
        print('รวมภาษีทะเบียนรถ(ต่อทุกปี):' , Price_RegisFeeYear)

        Price_RegisFee_Month = Price_RegisFeeYear/12
        print('รวมภาษีทะเบียนรถ(เฉลี่ยต่อเดือน):', Price_RegisFee_Month)


        # ------ ตารางปี ---- #
        # ปีที่ 1-5 จะคงที่ตามที่คำนวณได้
        # เกิน 6 ปีขึ้นไปจะลดภาษีลง 10%
        Price_RegisFeeYearSix = Price_RegisFeeYear - (Price_RegisFeeYear * (10/100))
        # ในปีที่ 10 ลดลงถึง 50% และคงที่ที่ 50% ในปีต่อไปเรื่อยๆ (ไม่แน่ใจ 50% ของปีแรก หรือ ของ 6ปี เลยใช้มากสุดที่ของปีแรก)
        Price_RegisFeeYearTen = Price_RegisFeeYear - (Price_RegisFeeYear * (50 / 100))
        Price_RegisFeeDic = {"1":Price_RegisFeeYear, "2":Price_RegisFeeYear, "3":Price_RegisFeeYear,
                             "4":Price_RegisFeeYear, "5":Price_RegisFeeYear,"6":Price_RegisFeeYearSix,
                             "7":Price_RegisFeeYearSix, "8":Price_RegisFeeYearSix, "9":Price_RegisFeeYearSix,
                             "10":Price_RegisFeeYearTen,"11":Price_RegisFeeYearTen,"12":Price_RegisFeeYearTen}

        Price_RegisFeeDicSum = round(sum(Price_RegisFeeDic.values()), 2)
        Price_RegisFeeDic['SUM'] = Price_RegisFeeDicSum

        print('ตารางจ่ายภาษีทะเบียนรถรายปี: ', Price_RegisFeeDic)
        print('รวมจ่ายภาษีทะเบียนรถ 12 ปี: ', Price_RegisFeeDicSum)
        print('--------------------------------------------')

        return Price_RegisFeeYear, Price_RegisFee_Month, Price_RegisFeeDic, Price_RegisFeeDicSum

    def PLB_Protection(self, TypeCAR='', SectionCAR=''):

        Dic_TyprCar = {
            'รถยนต์โดยสาร': {
                'ที่นั่งไม่เกิน 7 รถเก๋ง':600, 'ที่นั่งไม่เกิน 15 รถตู้':1100, 'ที่นั่งไม่เกิน 20': 2050, 'ที่นั่งไม่เกิน 40': 3200, 'ที่นั่งเกิน 40': 3740
            },

            'รถกระบะ/รถบรรทุก': {
                'ไม่เกิน 3 ตัน(รถกระบะ)': 900, 'ไม่เกิน 6 ตัน': 1220, 'ไม่เกิน 12 ตัน': 1310,
                'ไม่เกิน 12 ตัน(บรรทุกเชื้อเพลิง)': 1680, 'เกิน 12 ตัน(บรรทุกเชื้อเพลิง)': 2320
            },

            'รถประเภทอื่นๆ': {
                'หัวรถลากจูง': 2370, 'รถพ่วง': 600, 'รถยนต์ที่ใช้ในการเกษตร': 90
            }
        }

        print('--------------------------------------------')
        print(TypeCAR)
        print(SectionCAR)

        Price_TyprCar = Dic_TyprCar[TypeCAR][SectionCAR]
        print('ค่า พ.ร.บ. รายปี' + '(' + TypeCAR + SectionCAR + '): ', Price_TyprCar)
        print('--------------------------------------------')

        return Price_TyprCar

    def CarInsurance(self, TypeInsurance):
        Dic_Insurance = {'ประกันชั้น 1': 12000, 'ประกันชั้น 2': 6000, 'ประกันชั้น 3': 5000}

        print('-------------- CarInsuranc------------------')
        Price_CarInsurance = Dic_Insurance[TypeInsurance]
        print('ค่าประกันภัยรถยนต์ ' + TypeInsurance + ' รายปี: ', str(Price_CarInsurance))
        print('--------------------------------------------')

        return Price_CarInsurance

    def OilCost(self, Km_Liter, Price_Liter, Km_Mont):
        Price_Oli_Mont = (Km_Mont/Km_Liter) * Price_Liter

        print('--------------- OilCost --------------------')
        print('รถใช้น้ำมัน กม./ลิตร: ', Km_Liter)
        print('Km_Mont: ', Price_Liter)
        print('ระยะทาง กม. ที่ใช้ ต่อ เดือน: ', Km_Mont)

        print('ค่าน้ำมันรายเดือน: ', Price_Oli_Mont)

        Price_Oli_year = Price_Oli_Mont*12
        print('ค่าน้ำมันรายปี: ', Price_Oli_year)
        print('--------------------------------------------')
        return Price_Oli_Mont, Price_Oli_year

    def TirePrice(self, rim):
        dic_rim = {'ขอบยาง 13"':2100, 'ขอบยาง 14"':2200,'ขอบยาง 15"':2300,'ขอบยาง 16"':4000,'ขอบยาง 17"':6000,
                   'ขอบยาง 18"':8000,'ขอบยาง 19"':10000,'ขอบยาง 20"':11000,'ขอบยาง 21"':15000, 'โดยประมาณ':2500}

        print('---------------- TirePrice -----------------')
        print(rim)
        rim_four_year = dic_rim[rim] * 4
        print('ค่าเปลี่ยนยาง 4 เส้น (4ปีครั้ง โดยประมาณ): ', rim_four_year)

        rim_year = (dic_rim[rim]*4)/4
        print('ค่าเปลี่ยนยาง 4 เส้น (เฉลี่ยต่อปี): ', rim_year)

        rim_month = (dic_rim[rim]*4)/(4*12)
        print('ค่าเปลี่ยนยาง 4 เส้น (เฉลี่ยต่อเดือน): ', rim_month)
        print('--------------------------------------------')
        return rim_four_year, rim_year, rim_month

    def OtherExpenses(self, Parking, Expressway, WashCar, CarInspection, TrafficFine):

        print('------------- OtherExpenses ---------------')
        print('ค่าที่จอดรถ (รายเดือน): ', Parking)
        print('ค่าทางด่วน (รายเดือน): ', Expressway)
        print('ค่าล้างรถ (รายเดือน): ', WashCar)

        print('ตรวจสภาพรถยนต์/ค่าตกแต่งรถ (รายปี): ', CarInspection)
        print('ตรวจสภาพรถยนต์/ค่าตกแต่งรถ (เฉลี่ยต่อเดือน): ', CarInspection/12)

        print('ค่าปรับที่ทำผิดกฎจราจร (รายปี): ', TrafficFine)
        print('ค่าปรับที่ทำผิดกฎจราจร (เฉลี่ยต่อเดือน): ', TrafficFine/12)

        OtherExpensesSum = Parking + Expressway + WashCar + (CarInspection/12) + (TrafficFine/12)
        print('รวมค่าใช้จ่ายอื่นๆ (รายเดือน): ', str(OtherExpensesSum))
        print('--------------------------------------------')

        return OtherExpensesSum

    def getResults(self, CarPrice, DownPrecent, Interest, Year, CarSizeCC,
                 TypeCAR, SectionCAR, TypeInsurance,
                 Km_Liter, Price_Liter, Km_Mont, rim,
                 Parking, Expressway, WashCar,
                 CarInspection, TrafficFine):

        self.DownPayment, self.Finance, self.Interest_To_Year, self.Interest_All, self.Price_All, self.Pay_Per_Month = \
            self.CarLoanCalculation(CarPrice, DownPrecent, Interest, Year)

        self.Price_RegisFeeYear, self.Price_RegisFee_Month, self.Price_RegisFeeDic, self.Price_RegisFeeDicSum = \
            self.RegisFeeYear(CarSizeCC=CarSizeCC)

        self.Price_TyprCar = self.PLB_Protection(TypeCAR=TypeCAR, SectionCAR=SectionCAR)

        self.Price_CarInsurance = self.CarInsurance(TypeInsurance=TypeInsurance)

        self.Price_Oli_Mont, self.Price_Oli_year = self.OilCost(Km_Liter=Km_Liter, Price_Liter=Price_Liter,
                                                                Km_Mont=Km_Mont)

        self.rim_four_year, self.rim_year, self.rim_month = self.TirePrice(rim=rim)

        self.OtherExpensesSum = self.OtherExpenses(Parking=Parking, Expressway=Expressway, WashCar=WashCar,
                                                   CarInspection=CarInspection, TrafficFine=TrafficFine)

        Total_expenses_per_month = self.Pay_Per_Month + self.Price_RegisFee_Month + \
                                   (self.Price_TyprCar/12) + (self.Price_CarInsurance/12) + \
                                   self.Price_Oli_Mont + self.rim_month + self.OtherExpensesSum

        return self.DownPayment, self.Finance, self.Interest_To_Year, self.Interest_All,\
               self.Price_All, self.Pay_Per_Month, self.Price_RegisFeeYear, self.Price_RegisFee_Month,\
               self.Price_RegisFeeDic, self.Price_RegisFeeDicSum, self.Price_TyprCar, self.Price_CarInsurance,\
               self.Price_Oli_Mont, self.Price_Oli_year, self.rim_four_year, self.rim_year, self.rim_month,\
               self.OtherExpensesSum, Total_expenses_per_month


if __name__ == '__main__':
    CalCar_Class = CalCar(CarPrice=824000, DownPrecent=30, Interest=3, Year=5,
                          CarSizeCC=2393, TypeCAR='รถกระบะ/รถบรรทุก', SectionCAR='ไม่เกิน 3 ตัน(รถกระบะ)',
                          TypeInsurance='ประกันชั้น 1', Km_Liter=13, Price_Liter=25, Km_Mont=1000,
                          rim='ขอบยาง 15"', Parking=1000, Expressway=1000, WashCar=300,
                          CarInspection=10000, TrafficFine=1000)
