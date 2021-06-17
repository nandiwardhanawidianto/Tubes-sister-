import pickle

case_1 = {'Microsoft Office Word': 'v0', 'Paint.NET': 'v2.1', 'Google Chrome': 'v0', 'Mozzile Firefox': 'v115.13'}
case_2 = {'Microsoft Office Word': 'v2020', 'Paint.NET': 'v2.2', 'Google Chrome': 'v24.36.20', 'Mozzile Firefox': 'v100.10'}

file_1 = open("./case_1.pkl", "wb")
pickle.dump(case_1, file_1)
file_1.close()

file_2 = open("./case_2.pkl", "wb")
pickle.dump(case_2, file_2)
file_2.close()
