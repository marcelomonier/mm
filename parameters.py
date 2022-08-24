# Trabalha com a seleção dos nomes das colunas
class parameters:
  def __init__(self, df):
    self.columns_df = df.columns
    self.word1 = 'data_inicio_' 
    self.word2 = 'data_fim_'
    self.word3 = 'diferenca_em_minutos_'
    self.list_words = [self.word1, self.word2, self.word3]

  #Responsável por criar o nome das novas colunas criadas pela classe data_clear
  def list_columns(self, start=12, stop=None):
    name_columns = self.columns_df[start:stop]
    return_list = []
    for c in name_columns:
      for i in range(3):
        word = f'{self.list_words[i]}{c}'
        return_list.append(word)
    return return_list

  # Extraí o nome das colunas que possuiem dados do tipo datetime
  def columns_date(self, start=2, stop=None, step=3, origin=None):
    list_col = list(self.columns_df.copy())
    if origin == None:
      list_col = self.list_columns()
    for c in list_col[start:stop:step]:
      list_col.remove(c)
    return list_col

  # Fatia a lista de colunas
  def slice_columns(self, start=0, stop=None, step=None):
    return self.columns_df[start:stop:None]