import datetime

def MyQuery(date_work: datetime.date, date_limit: int):
    date_from = date_work
    date_to = date_from - datetime.timedelta(days = date_limit)

    query = f'''
    SELECT 
        payload->'ccb'->>'id' AS numero_proposta,
        payload->>'legacy_status' AS status,
        payload->'client'->>'name' AS nome,
        payload->'client'->>'email' AS email,
        payload->'client'->>'cell_phone' AS telefone,
        payload->'client'->>'document_number' AS cpf,
        (payload->'simulation'->'disbursement_options'->0->'issue_amount')::numeric AS valor_de_emissao,
        (payload->'simulation'->'disbursement_options'->0->'disbursed_issue_amount')::numeric AS valor_de_desembolso,
        jsonb_array_length(payload->'simulation'->'disbursement_options'->0->'installments') as prazo,
        TO_TIMESTAMP((payload->>'paid_at')::bigint) AS data_de_pagamento,
        TO_TIMESTAMP((payload->>'created_at')::bigint) AS data_de_criacao,
        (payload->'simulation'->'disbursement_options'->0->'iof_total')::numeric AS iof_total,
        (payload->'simulation'->'disbursement_options'->0->'tac'->>'Percentual') AS tac,
        (payload->'simulation'->'disbursement_options'->0->'tac_total')::numeric AS tac_total,
        payload->>'vendor_id' as id_vendedor,
        payload->'simulation'->'table'->'data'->>'id' as id_tabela
    FROM public.operations
    WHERE payload->>'legacy_status' = 'paid'
    AND TO_TIMESTAMP((payload->>'paid_at')::bigint) > '{date_to.strftime("%Y-%m-%d")}'
    AND TO_TIMESTAMP((payload->>'paid_at')::bigint) < '{date_from.strftime("%Y-%m-%d")}'
    '''
    return query
