import numpy as np

import numpy_financial as npf


class HomeLoan:
    def __init__(self):
        print('RunClass_HomeLoan')

    # ========================= คำนวณการผ่อนซื้อบ้าน ========================= #
    def DebtInstallment(self, Finance, Interest, Pay_Per_Month):
        Interest_All = []  # ดอกเบี้ย ทั้งหมด
        Balance_month = []  # ชำระเงินต้น ทั้งหมด
        Debt_start = Finance  # ยอดหนี้ เริ่มต้น
        DebtBalance_month = []  # ยอดหนี้เหลือ

        # if Debt_start >= 0:
        while Debt_start >= 0:
            # for i in range(Year*12):
            Interest_month = ((Debt_start * (Interest / 100)) / 365) * 30  # ชำระดอกเบี้ย
            # print('Interest_month: ', Interest_month)
            Interest_All.append(round(Interest_month, 2))

            balance = Pay_Per_Month - Interest_month  # ชำระเงินต้น
            Balance_month.append(round(balance, 2))

            Debt_start = Debt_start - balance  # ยอดหนี้คงเหลือ
            DebtBalance_month.append(round(Debt_start, 2))

        Number_Years = int(len(DebtBalance_month) - 1) // 12  # จำนวนงวด
        return Interest_All, Balance_month, DebtBalance_month, Number_Years

    def HomeLoanCalculation(self, LoanAmount, DownPrecent, Interest, Year):
        DownPayment = LoanAmount * (DownPrecent / 100)  # เงินดาวน์บาท
        DownPayment = round(DownPayment, 2)

        Finance = LoanAmount - DownPayment  # ยอดจัดไฟแนนซ์
        Finance = round(Finance, 2)

        # PMT(ดอกเบี้ยต่อปี /12, งวด(เดือน), ยอดเงินกู้)
        Pay_Per_Month = - (npf.pmt((Interest / 100) / 12, Year * 12, Finance, 000))  # ค่างวดในแต่ละเดือน (PMT)
        Pay_Per_Month = round(Pay_Per_Month, 2)

        # ชำระดอกเบี้ย , ชำระเงินต้น, ยอดหนี้คงเหลือ, จำนวนปีผ่อนชำระหมด
        Interest_All_list, Balance_month_list, DebtBalance_month_list, Number_Years = self.DebtInstallment(
            Finance=Finance,
            Interest=Interest, Pay_Per_Month=Pay_Per_Month)

        self.LoanAmount = LoanAmount
        self.Pay_Per_Month = Pay_Per_Month

        print('------------ CarLoanCalculation ------------')
        print('เงินดาวน์: ', DownPayment)
        print('ยอดจัดไฟแนนซ์: ', Finance)
        print('ดอกเบี้ย: ', Interest)
        print('จำนวนปีที่กู้: ', Year)
        print('ค่างวดในแต่ละเดือน: ', Pay_Per_Month)

        print('ดอกเบี้ยทั้งหมดที่ต้องจ่าย: ', Interest_All_list)
        print('ชำระเงินต้น: ', Balance_month_list)
        print('ยอดหนี้คงเหลือ: ', DebtBalance_month_list)
        print('จำนวนปีผ่อนชำระหมด: ', Number_Years)
        print('--------------------------------------------')

        return DownPayment, Finance, Pay_Per_Month, Interest_All_list, Balance_month_list, DebtBalance_month_list, Number_Years

    # ========================= คำนวณการผ่อนซื้อบ้าน ========================= #

    # ========================= คำนวณความสามารถผ่อนชำระ ========================= #
    # Debt Service Ratio ความสามารถผ่อนชำระหนี้ (มากก็ดี)
    def DebtServiceRatio(self, salary, DebtMonth):
        DSR = salary / DebtMonth
        DSR = round(DSR, 2)
        return DSR

    def SalaryLoan(self, salary, jobType='พนักงานประจำ', DebtCredit=10000, OtherMonthly_Debt=0):

        DebtCredit_Cal = DebtCredit * 0.1  #คิด 10%
        DebtCredit_Cal = round(DebtCredit_Cal, 2)

        career_type = {'พนักงานประจำ': 1, 'เจ้าของกิจการ(คนเดียว)': 0.1, 'เจ้าของกิจการ(หจก.)': 0.1, 'อาชีพอิสระ': 0.5}

        # ------- สูตร แบ่งประเภทรายได้ และ คิดลบค่าใช้จ่ายจริง ------- #
        salary_type = salary * career_type[jobType]  # คิด % รายได้ ตามประเภทงาน
        salary_expenses = salary_type * 0.7  # รายได้ ลบ ค่าใช้จ่ายในชีวิตประจำวัน 30% เหลือ 70% ของรายได้
        salary_Max_Month = salary_expenses - (
                    OtherMonthly_Debt + DebtCredit_Cal)  # รายได้ ลบภาระหนี้สินต่อเดือน = ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้
        LoanAmount_Max = salary_Max_Month * (1000 / 7)  # ล้านละ 7 พัน

        # ------- สูตร Sansiri (รายได้หักค่าใช้จ่าย * วงเงินกู้ / ขั้นต่ำต่องวดที่ต้องชำระ) ------- #
        LoanAmount_Sansiri = (salary_Max_Month * self.LoanAmount) / self.Pay_Per_Month

        # ------- สูตร คิดลบค่าใช้จ่ายทั่วไป โดยประมาณ ------- #
        salary_Min_Month = salary_type * 0.4  # ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้ - รายจ่าย 60% เหลือ 40% ของรายได้
        LoanAmount_Min = salary_Min_Month * (1000 / 7)  # ล้านละ 7 พัน

        print('------------ SalaryLoan ------------')
        print('รายรับ: ', salary)
        print('รายจ่าย: ', (OtherMonthly_Debt + DebtCredit_Cal))

        DSR = self.DebtServiceRatio(salary=salary, DebtMonth=float(DebtCredit + OtherMonthly_Debt))
        DSR = round(DSR, 2)
        print('DSR ความสามารถผ่อนชำระหนี้ (มากก็ดี ~3): ', DSR)

        salary_Max_Month = round(salary_Max_Month, 2)
        print('ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้ (หักค่าใช้จ่ายจริง): ', salary_Max_Month)

        LoanAmount_Max = round(LoanAmount_Max, 2)
        print('วงเงินที่กู้ได้ (หักค่าใช้จ่ายจริง): ', LoanAmount_Max)

        salary_Min_Month = round(salary_Min_Month, 2)
        print('ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้ (หักค่าใช้จ่าย 40% ของรายได้): ', salary_Min_Month)

        LoanAmount_Min = round(LoanAmount_Min, 2)
        print('วงเงินที่กู้ได้ (หักค่าใช้จ่าย 40% ของรายได้): ', LoanAmount_Min)

        LoanAmount_Sansiri = round(LoanAmount_Sansiri, 2)
        print('วงเงินที่กู้ได้ (หักค่าใช้จ่าย เทียบวงเงินกู้ที่ต้องชำระขั้นต่ำต่อเดือน): ', LoanAmount_Sansiri)
        print('------------------------------------')

        return DSR, salary_Max_Month, LoanAmount_Max, salary_Min_Month, LoanAmount_Min, LoanAmount_Sansiri

    # ========================= คำนวณความสามารถผ่อนชำระ ========================= #

    # ========================= คำนวณค่าใช้จ่ายขายบ้าน ========================= #
    # บัญชีอัตราภาษีเงินได้ สำหรับบุคคลธรรมดา
    def IncomeTaxRateAccount(self, Average_Netincome_year, YearHolding):
        # print('Average_Netincome_year: ', Average_Netincome_year)
        TaxRate_per = []
        price_list = [100000, 500000, 1000000, 4000000, 4000001]
        price_per = [0.05, 0.1, 0.2, 0.3, 0.37]
        balance = Average_Netincome_year

        for i, price in enumerate(price_list):
            # print('balance: ', balance)
            if (balance - price) > 0 and i < 4:
                TaxRate = price * price_per[i]
                TaxRate_per.append(TaxRate)
                balance = balance - price

            elif (balance - price) > 0 and i == 4:
                TaxRate = (balance - price) * price_per[i]
                TaxRate_per.append(TaxRate)
                balance = balance - (balance - price)

            else:
                # print('Else: ', balance)
                TaxRate = balance * price_per[i]
                TaxRate_per.append(TaxRate)
                balance = 0
            # print('price: ', price)
        TaxRate_all_year = YearHolding * sum(TaxRate_per)
        # print('TaxRate_all_year: ', TaxRate_all_year)
        # print('TaxRate_per: ', TaxRate_per)

        return TaxRate_per, TaxRate_all_year

    # ค่าลดหย่อนตามปีที่ถือครอง
    def DeductibleYear(self, YearHolding):
        Deductible_Year_tex_dic = {1: 0.92, 2: 0.84, 3: 0.77, 4: 0.71, 5: 0.65, 6: 0.60, 7: 0.55, 8: 0.50}
        if YearHolding >= 8:
            Deductible_Year_tex = Deductible_Year_tex_dic[8]
        else:
            Deductible_Year_tex = Deductible_Year_tex_dic[YearHolding]

        return Deductible_Year_tex

    def PurchaseCost(self, SellingPrice, PriceDepartment, YearHolding, YearNameHouse, Corporation):
        print('Corporation: ', Corporation)
        # อาจมีการเปลี่ยนแปลงตามนโยบายภาครัฐ

        # ค่าโอน 2% (ราคาประเมินกรมที่ดิน), อาจแบ่งจ่ายคนละครึ่ง
        Transfer_fee = PriceDepartment * 0.02

        # ค่าจดจำนอง 1% ของยอดเงินกู้จากธนาคาร(60%ราคาบ้าน)
        Mortgage = (SellingPrice * 0.6) * 0.01

        Stamp_duty = 0  # ค่าอากรแสตมป์
        BusinessTax = 0  # ค่าภาษีธุรกิจเฉพาะ

        # ค่าภาษีธุรกิจเฉพาะ 3.3% (นิติบุคลลเสียตลอด)
        if Corporation or YearHolding < 5 and YearNameHouse < 1:
            print('Corporation Fase')
            if SellingPrice < PriceDepartment:
                BusinessTax = SellingPrice * 0.033
            else:
                BusinessTax = PriceDepartment * 0.033

        # ค่าอากรแสตมป์ 0.5% (ราคาประเมินที่มากสุด) ถือครอง > 5 ปี หรือ ชื่อในโฉนด > 1
        # elif YearHolding >= 5 or YearNameHouse >= 1:
        else:
            print('Corporation else')
            # if Corporation == False:
            if SellingPrice < PriceDepartment:
                Stamp_duty = SellingPrice * 0.005
            else:
                Stamp_duty = PriceDepartment * 0.005




        # ค่าภาษีเงินได้
        # ค่าลดหย่อนตามปีที่ถือครอง
        Deductible_Year_tex = self.DeductibleYear(YearHolding=YearHolding)

        Discount_Year = PriceDepartment * Deductible_Year_tex  # ลดหย่อนตามปี (ราคาประเมิน)
        Netincome_Discount = PriceDepartment - Discount_Year  # เงินได้สุทธิ-ลดหย่อน (ราคาประเมิน)
        Average_Netincome_year = Netincome_Discount / YearHolding  # เงินได้สุทธิเฉลี่ยตามปี

        TaxRate_per, TaxRate_all_year = self.IncomeTaxRateAccount(Average_Netincome_year=Average_Netincome_year,
                                                                  YearHolding=YearHolding)

        print('------------ PurchaseCost ------------')
        print('ราคาขาย: ', SellingPrice)
        print('ราคาประเมินกรมที่ดิน: ', PriceDepartment)
        print('ถือครองมา(ปี) เจ้าของบ้าน: ', YearHolding)
        print('มีชื่อในโฉนด (ปี) เจ้าบ้าน: ', YearNameHouse)
        print('สถานะนิติบุคคล: ', Corporation)
        print('-----')

        Transfer_fee = round(Transfer_fee, 2)
        print('ค่าโอน 2% (ราคาประเมินกรมที่ดิน): ', Transfer_fee)

        Mortgage = round(Mortgage, 2)
        print('ค่าจดจำนอง 1% ของยอดเงินกู้จากธนาคาร(60%ราคาบ้าน): ', Mortgage)

        Stamp_duty = round(Stamp_duty, 2)
        print('ค่าอากรแสตมป์ 0.5% (ราคาประเมินที่มากสุด) ถือครอง > 5 ปี หรือ ชื่อในโฉนด > 1: ', Stamp_duty)

        BusinessTax = round(BusinessTax, 2)
        print('ค่าภาษีธุรกิจเฉพาะ 3.3% (นิติบุคลลเสียตลอด): ', BusinessTax)

        Deductible_Year_tex = round(Deductible_Year_tex, 2) # *
        print('% ลดหย่อนตามปีที่ถือครอง: ', Deductible_Year_tex)

        Discount_Year = round(Discount_Year, 2)
        print('ค่าลดหย่อนตามปีที่ถือครอง (ราคาประเมิน): ', Discount_Year) # *

        Netincome_Discount = round(Netincome_Discount, 2)
        print('เงินได้สุทธิ-ลดหย่อน คงเหลือ (ราคาประเมิน): ', Netincome_Discount) # *

        Average_Netincome_year = round(Average_Netincome_year, 2)
        print('ภาษีเงินได้เฉลี่ยต่อปี (ปีที่ถือครอง): ', Average_Netincome_year) # *

        TaxRate_per = TaxRate_per
        print('เทียบตาราง ภาษีเงินได้ที่ต้องชำระ (คูณปีที่ถือครอง): ', TaxRate_per)  # *

        TaxRate_all_year = round(TaxRate_all_year, 2)
        print('ภาษีเงินได้ที่ต้องชำระ (คูณปีที่ถือครอง): ', TaxRate_all_year)

        # if Corporation == False or YearHolding >= 5 or YearNameHouse >= 1:
        #     Sum = Transfer_fee + Mortgage + Stamp_duty + TaxRate_all_year
        # elif Corporation == True or YearHolding < 5 or YearNameHouse < 1:
        #     Sum = Transfer_fee + Mortgage + BusinessTax + TaxRate_all_year
        Sum_Price = Transfer_fee + Mortgage + Stamp_duty + BusinessTax + TaxRate_all_year
        print('ค่าใช้จ่ายรวม: ', Sum_Price)
        print('--------------------------------------')

        return Transfer_fee, Mortgage, Stamp_duty, BusinessTax, Deductible_Year_tex, Discount_Year, Netincome_Discount, \
               Average_Netincome_year, TaxRate_per, TaxRate_all_year, Sum_Price
    # ========================= คำนวณค่าใช้จ่ายขายบ้าน ========================= #


if __name__ == '__main__':
    HomeLoan_Class = HomeLoan()

    # คำนวณการผ่อนซื้อบ้าน
    DownPayment, Finance, Pay_Per_Month, Interest_All_list, Balance_month_list, DebtBalance_month_list, Number_Years = \
        HomeLoan_Class.HomeLoanCalculation(LoanAmount=5000000, DownPrecent=10, Interest=5.75, Year=30)

    # คำนวณความสามารถผ่อนชำระ
    DSR, salary_Max_Month, LoanAmount_Max, salary_Min_Month, LoanAmount_Min, LoanAmount_Sansiri = \
        HomeLoan_Class.SalaryLoan(salary=21000, jobType='พนักงานประจำ', DebtCredit=1000, OtherMonthly_Debt=6000)

    # คำนวณค่าใช้จ่ายขายบ้าน
    Transfer_fee, Mortgage, Stamp_duty, BusinessTax, Deductible_Year_tex, Discount_Year, Netincome_Discount, \
    Average_Netincome_year, TaxRate_per, TaxRate_all_year, Sum_Price = \
        HomeLoan_Class.PurchaseCost(SellingPrice=5000000, PriceDepartment=500000000,
                                    YearHolding=5, YearNameHouse=1, Corporation=False)
