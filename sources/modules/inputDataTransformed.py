import sqlite3
from re import search


class inputsDB():
    '''
        Classe para salvar o resultado na Stage Area.

    '''

    def __init__(self):
         pass
    

    def conDatabase(self):
        con = sqlite3.connect("../../../ZZ/importacoes.db")
        cur = con.cursor()
        return con, cur

    # cria dicionário com atributos de cada tabela

    def totalAttributes(self, list_tables: list):
        con, cur = self.conDatabase()
        total_dict = list()
        for tabela in list_tables:
            dict_correspondence = dict()
            result = cur.execute(f"pragma table_info({tabela})").fetchall()
            #Eliminando o atributo id da tabela
            for atrr in result[1:]:
                dict_correspondence[atrr[1]] = ''
            total_dict.append(dict_correspondence)
        cur.close()
        con.close()
        return total_dict 
    

    def _insertData(self, tabela_zz: str, atributos_zz: list, atributos_staging_area: list, contracts: bool):

        '''
            Metodo para fazer input no DB dos valores novos.

        '''
        con, cur = self.conDatabase()
        atributos_sql = ', '.join(atributos_zz)
        atributos_staging_sql = ', '.join(atributos_staging_area)
        query_insert = f'''
                        INSERT INTO {tabela_zz} ({atributos_sql})
                        SELECT DISTINCT {atributos_staging_sql}
                        FROM staging_area
                        WHERE {atributos_staging_area[0]} IS NOT NULL  -- Filtra valores nulos
                            AND NOT EXISTS (
                                SELECT 1
                                FROM {tabela_zz}
                                WHERE {tabela_zz}.{atributos_zz[0]} = staging_area.{atributos_staging_area[0]}
                            );
                    '''
        

        query_insert_contracts = f'''
                        
                        INSERT INTO {tabela_zz} ({atributos_sql})
                        SELECT DISTINCT {atributos_staging_sql}
                        FROM staging_area
                        WHERE staging_area.numero_ade IS NOT NULL  -- Filtra valores nulos
                            AND NOT EXISTS (
                                SELECT 1
                                FROM contrato
                                WHERE contrato.numero_ade = staging_area.numero_ade
                            );
                    '''
    # fiz o join pra todos os atributos, e quando só tenho um campo dá erro, porque o outro não tem nada
        try:
            if contracts:
                cur.execute(query_insert_contracts)
            else:
                cur.execute(query_insert)

            con.commit()
            cur.close()
            con.close()
        except sqlite3.OperationalError:
            pass


    def loadInput(self, list_tables: list, total_dict: dict, contracts = False):
        for i, tabela_zz in enumerate(list_tables):
            # Filtra apenas atributos da tabela ZZ que contem seu correspondente no staging_area 
            atributos_zz = [key for key, value in total_dict[i].items() if value != ""]
            atributos_staging_area = [v for v in total_dict[i].values() if v != ""]
            
            if len(atributos_staging_area) > 0 and len(atributos_zz) > 0:
                inputsDB()._insertData(tabela_zz=tabela_zz,
                                    atributos_zz=atributos_zz,
                                    atributos_staging_area=atributos_staging_area,
                                    contracts=contracts)