import pandas as pd
import numpy as np
import json
from drive.MyDrive.Pulse.workspace.mateus_mais.parameters import parameters

#Extrai os dados do dataset original
class data_clear:
  def __init__(self, df):
    self.df = df
    self.parameters = parameters(df)
  
  # Extraí os dados em json, criando novas colunas
  def extract_and_create(self, transform=None):
    l = []
    self.return_list = []
    interlist = []
    all_df_list = []
    for i in self.parameters.slice_columns(12):
      time_list = self.df[i].iloc[:]
      for j in time_list:
        objeto = json.loads(j)
        interlist.append(objeto)
      self.return_list.append(interlist)
      interlist = []
    if transform == True:
      self.return_list, contador_df = self.extract_and_transform(self.return_list)
    df_lists = []
    new_df = pd.DataFrame()
    for c in self.return_list:
      mini_df = pd.DataFrame(c)
      all_df_list.append(mini_df)
    new_df = pd.concat(all_df_list, axis=1)
    new_df.columns = self.parameters.list_columns()
    columns_date = self.parameters.columns_date()
    for i in columns_date:
      new_df[i] = pd.to_datetime(new_df[i].astype(str), errors='coerce', utc=True)
    df_tratado = pd.concat([self.df[self.df.columns[:12]], new_df], axis=1)
    if transform == True:
      df_cont = pd.DataFrame(contador_df)
      df_tratado = [df_tratado, df_cont]
    return df_tratado

  def extract_and_transform(self, return_list):
    return_list = return_list
    return_list_contadores = []
    c = 0
    contNan = 0
    contOk = 0
    contNull = 0
    for i in range(len(return_list)):
      lista_interna = return_list[i]
      for j in range(len(lista_interna)):
        if list(lista_interna[j].values()).count(None) == 3:
          return_list[i][j] = {'data_inicio': 0, 'data_fim': 0,'diferenca_em_minutos': 0}
          contNull += 1
        elif list(lista_interna[j].values()).count(None) == 2 or list(lista_interna[j].values()).count(None) == 1:
          return_list[i][j] = {'data_inicio': np.nan, 'data_fim': np.nan,'diferenca_em_minutos': np.nan}
          contNan += 1
        else:
          contOk += 1
      return_list_contadores.append({'incompleto': contNan, 'completo': contOk, 'vazio': contNull})
      contNan = 0
      contOk = 0
      contNull = 0
    return return_list, return_list_contadores