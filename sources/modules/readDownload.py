import datetime
from pathlib import Path
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# classe para fazer a leitura dos download, na pasta de cada banco - esta pode ser uma classe geral, se for possível pensar em todos os formatos, e, pensar numa forma dinâmica de receber os atributos
class read_downaload():

    def __init__(self):
        pass

    # def read_data(self,
    #             bank: str,
    #             date: datetime.date,
    #             sep = None,
    #             decimal = None,
    #             header = None,
    #             thousands = None,
    #             sheet_name = None,
    #             type_transference: list = ['comission', 'production', 'importation', 'extra'],
    #             engine: list = ['csv', 'excel', 'html'],
    #             parse_dates = None,
    #             format_parse_dates = None,
    #             encoding = None,
    #             converters = None,
    #             skiprows = None,
    #             skipfooter = None,
    #             delimiter = None
    #             ):
    
    #     '''
    #         Método para carga dos dados.
    #         Preencha os argumentos de acordo com a documentação do pandas.
    #     '''

    #     dados = pd.DataFrame()
    #     engine = engine[0]
    #     file = None
    #     path_to_read = f'../../{bank}/download/{date.year}/{date.month}/{type_transference[0]}/'
        
    #     for file_Search in os.listdir(path_to_read):
    #         if file_Search.startswith(date.strftime("%Y-%m-%d")):
    #            files =  file_Search
    
    #     if len(files) > 0:
    #         for file in files:

    #             if file is not None:
    #                 if engine == 'csv':
    #                     dados = pd.read_csv(path_to_read + file,
    #                                         encoding = encoding,
    #                                         decimal=decimal,
    #                                         sep=sep,
    #                                         thousands=thousands,
    #                                         header=header,
    #                                         parse_dates = parse_dates,
    #                                         date_format = format_parse_dates,
    #                                         converters=converters,
    #                                         delimiter = delimiter)
                        
    #                 elif engine == 'excel':
    #                     dados = pd.read_excel(path_to_read + file,
    #                                         decimal=decimal,
    #                                         thousands=thousands,
    #                                         header=header,
    #                                         sheet_name=sheet_name,
    #                                         parse_dates=parse_dates,
    #                                         date_format=format_parse_dates,
    #                                         converters=converters,
    #                                         skiprows = skiprows
    #                                         #   skipfooter = skipfooter
    #                                         ) # type: ignore
                        
    #                 elif engine == 'html':
    #                     dados = pd.read_html(path_to_read + file,
    #                                         decimal = decimal,
    #                                         thousands=thousands,
    #                                         header=header,
    #                                         parse_dates=parse_dates,
    #                                         converters=converters)[0]



    #         if not dados.empty:
    #             dados = pd.concat([dados, dados])
    #             return dados
    #         else:
    #             return
        
    def read_data(self,
                bank: str,
                date: datetime.date,
                sep = None,
                decimal = None,
                header = None,
                thousands = None,
                sheet_name = None,
                type_transference: list = ['comission', 'production', 'importation', 'extra'],
                engine: list = ['csv', 'excel', 'html', 'parquet'],
                parse_dates = None,
                format_parse_dates = None,
                encoding = None,
                converters = None,
                skiprows = None,
                skipfooter = None,
                delimiter = None
                ):
    
        '''
            Método para carga dos dados.
            Preencha os argumentos de acordo com a documentação do pandas.
        '''

        dados = pd.DataFrame()
        engine = engine[0]
        file = None
        path_to_read = f'../../{bank}/download/{date.year}/{date.month}/{type_transference[0]}/'
        for file_Search in os.listdir(path_to_read):
            if file_Search.startswith(date.strftime("%Y-%m-%d")):
               file =  file_Search
               
        # print(os.path.getsize(path_to_read + file))
        
        if file is not None:
            if os.path.getsize(path_to_read + file) > 1:
                if engine == 'csv':
                    dados = pd.read_csv(path_to_read + file,
                                        encoding = encoding,
                                        decimal=decimal,
                                        sep=sep,
                                        thousands=thousands,
                                        header=header,
                                        parse_dates = parse_dates,
                                        date_format = format_parse_dates,
                                        converters=converters,
                                        delimiter = delimiter)
                    
                elif engine == 'excel':
                    dados = pd.read_excel(path_to_read + file,
                                        decimal=decimal,
                                        thousands=thousands,
                                        header=header,
                                        sheet_name=sheet_name,
                                        parse_dates=parse_dates,
                                        date_format=format_parse_dates,
                                        converters=converters,
                                        skiprows = skiprows
                                        #   skipfooter = skipfooter
                                        ) # type: ignore
                    
                elif engine == 'html':
                    dados = pd.read_html(path_to_read + file,
                                        decimal = decimal,
                                        thousands=thousands,
                                        header=header,
                                        parse_dates=parse_dates,
                                        converters=converters)[0]
                    
                elif engine == 'parquet':
                    dados = pd.read_parquet(path_to_read + file)



        if not dados.empty:
            return dados
        else:
            return
        
