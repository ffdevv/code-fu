import pandas as pd

def concat_join_fields_index2index(df1, df2, field_to, field_from, sep):
  """
  Effettua una join sugli index e concatena i valori del :param field_from: di :param df2: 
  dentro a un nuovo campo :param field_to: in :param df1:
  
  la join è effettuata comparando df1.index e df2.index
  """
  df1[field_to] = [
    sep.join(df2.loc[df2.index == k, :][field_from].apply(str))
    for k in df1.index
  ]

def concat_join_fields_index2col(df1, df2, df2_col, field_to, field_from, sep):
  """
  Effettua una join sugli index e concatena i valori del :param field_from: di :param df2: 
  dentro a un nuovo campo :param field_to: in :param df1:
  
  la join è effettuata comparando df1.index e df2[:param df2_col:]
  """
  df1[field_to] = [
    sep.join(df2.loc[df2[df2_col] == k, :][field_from].apply(str))
    for k in df1.index
  ]

def concat_join_fields_col2index(df1, df2, df1_col, field_to, field_from, sep):
  """
  Effettua una join sugli index e concatena i valori del :param field_from: di :param df2: 
  dentro a un nuovo campo :param field_to: in :param df1:
  
  la join è effettuata comparando df1[:param df1_col:] e df2.index 
  """
  df1[field_to] = [
    sep.join(df2.loc[df2.index == k, :][field_from].apply(str))
    for k in df1[df1_col]
  ]

def concat_join_fields_col2col(df1, df2, df1_col, df2_col, field_to, field_from, sep):
  """
  Effettua una join sugli index e concatena i valori del :param field_from: di :param df2: 
  dentro a un nuovo campo :param field_to: in :param df1:
  
  la join è effettuata comparando df1[:param df1_col:] e df2[:param df2_col:]
  """
  df1[field_to] = [
    sep.join(df2.loc[df2[df2_col] == k, :][field_from].apply(str))
    for k in df1[df1_col]
  ]
