from fastapi import FastAPI, File, UploadFile  # pip install fastapi
import uvicorn  # pip install
from starlette.middleware.cors import CORSMiddleware

from HomeLoan import HomeLoan
HomeLoan_Class = HomeLoan()

from CalCar import CalCar
CalCar_Class = CalCar()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
def index():
    return {"Hello": "World"}

# ========================= คำนวณการผ่อนซื้อบ้าน ========================= #
@app.post('/CalHomeLoan')
def CalHomeLoan(LoanAmount:str, DownPrecent:str, Interest:str, Year:str):
    print('LoanAmount: >> ' + str(LoanAmount))
    print('DownPrecent: >> ' + str(DownPrecent))
    print('Interest: >> ' + str(Interest))
    print('Year: >> ' + str(Year))
    DownPayment, Finance, Pay_Per_Month, Interest_All_list, Balance_month_list, DebtBalance_month_list, Number_Years = \
        HomeLoan_Class.HomeLoanCalculation(LoanAmount=float(LoanAmount), DownPrecent=float(DownPrecent),
                                           Interest=float(Interest), Year=float(Year))

    response = {'CalHomeLoan':
                    {
                        'DownPayment':DownPayment,
                        'Finance': Finance,
                        'Pay_Per_Month': Pay_Per_Month,
                        'Number_Years': Number_Years,
                        'Interest_All_list': Interest_All_list,
                        'Balance_month_list': Balance_month_list,
                        'DebtBalance_month_list': DebtBalance_month_list
                    }
                }

    print(response)
    return response
# ========================= คำนวณการผ่อนซื้อบ้าน ========================= #

# ========================= คำนวณความสามารถผ่อนชำระ ========================= #
@app.post('/PayInstallments') # salary, jobType='พนักงานประจำ', OtherMonthly_Debt=0, DebtCredit=10000
def PayInstallments(salary:str, jobType:str, DebtCredit:str, OtherMonthly_Debt:str):

    print('Salary: >> ' + str(salary))
    print('JobType: >> ' + str(jobType))
    print('DebtCredit: >> ' + str(DebtCredit))
    print('OtherMonthly_Debt: >> ' + str(OtherMonthly_Debt))


    DSR, salary_Max_Month, LoanAmount_Max, salary_Min_Month, LoanAmount_Min, LoanAmount_Sansiri = \
        HomeLoan_Class.SalaryLoan(salary=float(salary), jobType=jobType, DebtCredit=float(DebtCredit), OtherMonthly_Debt=float(OtherMonthly_Debt))

    response = {'PayInstallments':
                    {
                        'DSR_out':DSR,  # (มากก็ดี ~3)
                        'salary_Max_Month': salary_Max_Month,  # ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้ (หักค่าใช้จ่ายจริง)
                        'LoanAmount_Max': LoanAmount_Max,  # วงเงินที่กู้ได้ (หักค่าใช้จ่ายจริง)
                        'salary_Min_Month': salary_Min_Month,  # ภาระหนี้ที่สามารถผ่อนจ่ายต่อเดือนได้ (หักค่าใช้จ่าย 40% ของรายได้)
                        'LoanAmount_Min': LoanAmount_Min,  # วงเงินที่กู้ได้ (หักค่าใช้จ่าย 40% ของรายได้)
                        'LoanAmount_Sansiri': LoanAmount_Sansiri  # วงเงินที่กู้ได้ (หักค่าใช้จ่าย เทียบวงเงินกู้ที่ต้องชำระขั้นต่ำต่อเดือน)
                    }
                }

    print(response)
    return response
# ========================= คำนวณความสามารถผ่อนชำระ ========================= #

# ========================= คำนวณค่าใช้จ่ายขายบ้าน ========================= #
@app.post('/CostSellHouse') # SellingPrice, PriceDepartment, YearHolding, YearNameHouse, Corporation=False
def CostSellHouse(Corporation:str, SellingPrice:str, PriceDepartment:str, YearHolding:str, YearNameHouse:str):

    print('SellingPrice: >> ' + str(SellingPrice))
    print('PriceDepartment: >> ' + str(PriceDepartment))
    print('YearHolding: >> ' + str(YearHolding))
    print('YearNameHouse: >> ' + str(YearNameHouse))
    print('Corporation: >> ' + str(Corporation))

    if Corporation == 'false':
        Corporation = False
    else:
        Corporation = True

    Transfer_fee, Mortgage, Stamp_duty, BusinessTax, Deductible_Year_tex, Discount_Year, Netincome_Discount, \
    Average_Netincome_year, TaxRate_per, TaxRate_all_year, Sum_Price = \
        HomeLoan_Class.PurchaseCost(SellingPrice=float(SellingPrice), PriceDepartment=float(PriceDepartment),
                                    YearHolding=float(YearHolding), YearNameHouse=float(YearNameHouse), Corporation=Corporation)

    response = {'CostSellHouse':
        {
            'Transfer_fee': Transfer_fee,  # ค่าโอน 2% (ราคาประเมินกรมที่ดิน)
            'Mortgage': Mortgage,  # ค่าจดจำนอง 1% ของยอดเงินกู้จากธนาคาร(60%ราคาบ้าน)
            'Stamp_duty': Stamp_duty,  # ค่าอากรแสตมป์ 0.5% (ราคาประเมินที่มากสุด) ถือครอง > 5 ปี หรือ ชื่อในโฉนด > 1
            'BusinessTax': BusinessTax,  # ค่าภาษีธุรกิจเฉพาะ 3.3% (นิติบุคลลเสียตลอด)
            'Deductible_Year_tex': Deductible_Year_tex * 100,  # % หักค่าใช้จ่าย ตามปีที่ถือครอง
            'Discount_Year': Discount_Year,  # ค่าลดหย่อนตามปีที่ถือครอง (ราคาประเมิน)
            'Netincome_Discount': Netincome_Discount , # เงินได้สุทธิ-ลดหย่อน (ราคาประเมิน)
            'Average_Netincome_year': Average_Netincome_year,  # ภาษีเงินได้เฉลี่ยต่อปี (ปีที่ถือครอง)
            'TaxRate_per': TaxRate_per,  # เทียบตาราง ภาษีเงินได้ที่ต้องชำระ (คูณปีที่ถือครอง)
            'TaxRate_all_year': TaxRate_all_year,  # ภาษีเงินได้ที่ต้องชำระ (คูณปีที่ถือครอง)
            'Sum_Price': Sum_Price # ค่าใช้จ่ายรวม
        }
    }

    print(response)
    return response

# ========================= คำนวณค่าใช้จ่ายขายบ้าน ========================= #

# ========================= คำนวณค่าใช้จ่ายซื้อรถ ========================= #
@app.post('/CalCar')
def CalCar(CarPrice:str, DownPrecent:str, Interest:str, Year:str, CarSizeCC:str, TypeCAR:str,
           SectionCAR:str, TypeInsurance:str, Km_Liter:str, Price_Liter:str, Km_Mont:str,
           rim:str, Parking:str, Expressway:str, WashCar:str, CarInspection:str,TrafficFine:str):  # Parameter

    print('CarPrice: >> ' + str(CarPrice))
    print('DownPrecent: >> ' + str(DownPrecent))
    print('Interest: >> ' + str(Interest))
    print('Year: >> ' + str(Year))
    print('CarSizeCC: >> ' + str(CarSizeCC))
    print('TypeCAR: >> ' + str(TypeCAR))
    print('SectionCAR: >> ' + str(SectionCAR))
    print('TypeInsurance: >> ' + str(TypeInsurance))
    print('Km_Liter: >> ' + str(Km_Liter))
    print('Price_Liter: >> ' + str(Price_Liter))
    print('Km_Mont: >> ' + str(Km_Mont))
    print('rim: >> ' + str(rim))
    print('Parking: >> ' + str(Parking))
    print('Expressway: >> ' + str(Expressway))
    print('WashCar: >> ' + str(WashCar))
    print('CarInspection: >> ' + str(CarInspection))
    print('TrafficFine: >> ' + str(TrafficFine))


    DownPayment, Finance, Interest_To_Year, Interest_All,\
    Price_All, Pay_Per_Month,Price_RegisFeeYear,\
    Price_RegisFee_Month,Price_RegisFeeDic, Price_RegisFeeDicSum,\
    Price_TyprCar, Price_CarInsurance,Price_Oli_Mont, Price_Oli_year,\
    rim_four_year, rim_year, rim_month, OtherExpensesSum, Total_expenses_per_month = CalCar_Class.getResults(
        CarPrice=float(CarPrice), DownPrecent=float(DownPrecent), Interest=float(Interest), Year=int(Year),
        CarSizeCC=float(CarSizeCC), TypeCAR=str(TypeCAR), SectionCAR=str(SectionCAR), TypeInsurance=str(TypeInsurance),
        Km_Liter=float(Km_Liter), Price_Liter=float(Price_Liter), Km_Mont=float(Km_Mont), rim=str(rim),
        Parking=float(Parking), Expressway=float(Expressway), WashCar=float(WashCar), CarInspection=float(CarInspection),
        TrafficFine=float(TrafficFine))

    response = {'CalCar':
                    {
                        'DownPayment': float(round(DownPayment, 2)),
                        'Finance': float(round(Finance, 2)),
                        'Interest_To_Year': float(round(Interest_To_Year, 2)),
                        'Interest_All': float(round(Interest_All, 2)),
                        'Price_All': float(round(Price_All, 2)),
                        'Pay_Per_Month': float(round(Pay_Per_Month, 2)),
                        'Price_RegisFeeYear': float(round(Price_RegisFeeYear, 2)),
                        'Price_RegisFee_Month': float(round(Price_RegisFee_Month, 2)),
                        'Price_RegisFeeDic': Price_RegisFeeDic,
                        'Price_RegisFeeDicSum': float(round(Price_RegisFeeDicSum, 2)),
                        'Price_TyprCar': float(round(Price_TyprCar, 2)),
                        'Price_CarInsurance': float(round(Price_CarInsurance, 2)),
                        'Price_Oli_Mont': float(round(Price_Oli_Mont, 2)),
                        'Price_Oli_year': float(round(Price_Oli_year, 2)),
                        'rim_four_year': float(round(rim_four_year, 2)),
                        'rim_year': float(round(rim_year, 2)),
                        'rim_month': float(round(rim_month, 2)),
                        'OtherExpensesSum': float(round(OtherExpensesSum, 2))
                    },
                'Total_per_month':float(round(Total_expenses_per_month, 2))
    }


    print(response)
    return response
# ========================= คำนวณค่าใช้จ่ายซื้อรถ ========================= #

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.11", port=5050)