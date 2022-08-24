import pandas as pd
from drive.MyDrive.Pulse.workspace.mateus_mais.parameters import *
from drive.MyDrive.Pulse.workspace.mateus_mais.data_clear import *

# Analisa a correlação que existe no dataset
class corr_analysis(data_clear):
  def __init__(self, df):
    super().__init__(df)
    self.columns_df_origin = df.columns
    self.df_corr_analysis = df
    self.corr_analysis = self.extract_and_create()
    self.columns_date = parameters(self.corr_analysis).columns_date(start=14, origin=False)[12:]
    self.corr = self.corr_analysis[self.columns_date].isnull().corr()
    self.corrm = self.corr[(self.corr.select_dtypes(include='number') >= 0.45) & (self.corr.select_dtypes(include='number') <= 1.00)]
    self.corrm.fillna(0, inplace=True)
  
  # Analisa a correlação das colunas retornando um dataset
  def analysis(self):
    self.corr = self.corr_analysis.isnull().corr()
    lista = []
    self.corrm.loc[self.corrm.columns[0]]
    for i in range(len(self.corrm.loc[self.corrm.columns])):
      lista.append(list(self.corrm.loc[self.corrm.columns[i]]))
    cont = soma = media = conta = 0
    medialist = []
    listaMaiorMedia = []
    for i in lista[::2]:
      cont = 0
      for j in i:
        soma += j
        if cont == 1:
          media = soma / 2
          soma = 0
          medialist.append(media)
        cont += 1
        if cont == 2:
          cont = 0
      listaMaiorMedia.append(medialist)
      medialist = []

    media_df = pd.DataFrame(listaMaiorMedia, columns=self.corrm.columns[0::2])
    media_df.columns = self.columns_df_origin[12:]
    media_df.index = self.columns_df_origin[12:]
    return media_df

  # Cria um texto a partir da correlação do dataset criado na função analysis
  def create_reports_corr(self):
    media_df = self.analysis()
    print("## **Nível de correlação entre as colunas**")
    print('-------')
    for i in media_df.index:
      print(f'Coluna `{i}`:')
      for j in media_df.index:
        if media_df[j].loc[i] > 0:
          print(f'* `{j}`: {(media_df[j].loc[i]):.2f}')
      print('-------')