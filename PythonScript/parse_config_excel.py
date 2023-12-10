import pandas as pd

class Config:
    def __init__(self, initialPeopleCount, initialValue, peopleCountStep, mealsKindsStep):
        self.initialPeopleCount = initialPeopleCount
        self.initialValue = initialValue
        self.peopleCountStep = peopleCountStep
        self.mealsKindsStep = mealsKindsStep
        
    def print(self):
        print("self.initialValue:", self.initialValue)
        print("self.peopleCountStep:", self.peopleCountStep)
        print("self.mealsKindsStep:", self.mealsKindsStep)
        
def read_config_from_excel(file_path: str, sheet_name: str, row: int) -> Config:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    return Config(df.iat[row, 1], df.iat[row, 3], df.iat[row, 6], df.iat[row, 8])

if __name__ == "__main__":
    config = read_config_from_excel("采购单.xlsx", "参数设置")