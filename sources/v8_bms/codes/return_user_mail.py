import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import psycopg2


## bff engine

def retorna_conBFF():
    engine = psycopg2.connect(
        host = "v8-bff.postgres.database.azure.com",
        dbname = "bff",
        user = "financeiro_leitura",
        password = "S#rtUhu8dd^LB9V%Ri2UH8!NAbKeOfg!",
        port = "5432",
        sslmode = 'require'
    )
    return engine

def retorna_usermail(id_vender: list, engine):
    
    result_query = []
    search = dados['id_vendedor'].to_list()
    for idx, mail in enumerate(search):
        try:
            result = pd.read_sql(f"select email from public.users where id = '{mail}'", con=engine)
            result_query.append(result['email'][0])
        except Exception:
            result_query.append("NA")
            continue
    
    return result_query