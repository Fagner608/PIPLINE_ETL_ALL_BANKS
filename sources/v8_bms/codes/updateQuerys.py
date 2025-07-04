updateClient = f'''
                                                
                        INSERT INTO cliente ("cpf_cliente", "nome_cliente", "email_cliente", "telefone_cliente")
                        SELECT "CPF" as cpf, 
                        "NOME" as nome, 
                        "USUARIO BANCO" as email, 
                        "TELEFONE" as telefone
                        FROM (
                        SELECT DISTINCT ON ("CPF") 
                                "CPF", 
                                "NOME", 
                                "USUARIO BANCO", 
                                "TELEFONE"
                        FROM public.temp_table
                        WHERE "CPF" IS NOT NULL
                        ORDER BY "CPF", "NOME" -- ou qualquer outra coluna que você queira garantir a única linha
                        ) as tmp
                        WHERE NOT EXISTS (
                        SELECT 1
                        FROM cliente
                        WHERE cpf_cliente = tmp."CPF"
                        );

            '''

# updateClient = f'''
                            
#             INSERT INTO cliente ("cpf_cliente", "nome_cliente", "email_cliente", "telefone_cliente")
#             SELECT DISTINCT 
#                 "CPF" as cpf, 
#                 "NOME" as nome, 
#                 "USUARIO BANCO" as email, 
#                 "TELEFONE" as telefone
#             FROM public.temp_table as tmp
#             where tmp."CPF" IS NOT NULL
#             AND NOT EXISTS (
#                     SELECT 1
#                     FROM cliente
#                     WHERE cpf_cliente = tmp."CPF"
#             )

#             '''




updateContrato = f'''
                            
INSERT INTO contrato (
                "numero_proposta",
                "cpf_cliente",
                "id_provider",
                "id_status_importacao",
                "table_grid", 
                "status",
                "valor_emissao",
                "valor_desembolsado",
                "prazo",
                "data_pagamento",
                "data_criacao",
                "iof_total",
                "tac",
                "tac_total",
                "id_vendedor",
                "TAXA",
                "TOMADA_DECISAO",
                "VALOR_COMISSAO_ESTIMADO",
                "SPREAD_ESTIMADO"
                )
SELECT DISTINCT 
                "NUMERO PROPOSTA", 
                "CPF", 
                cast("provedor" as integer), -- fazer update para retornar o id_provedor na etapa anterior 
                cast("status_importacao" as integer),
                "ID TABELA", -- fazer update para retornar o código da tabela na etapa anterior
                "STATUS",
                cast("VALOR OPERACAO" as float),
                cast("VALOR LIBERADO" as float),
                "NUMERO PARCELAS",
                "DATA DE PAGAMENTO",
                "DATA DE CRIACAO",
                cast("IOF TOTAL" as float),
                cast("TAXA TAC" as float),
                cast("TAX_INFORMADO" as float),
                "ID VENDEDOR",
                "taxa",
                "tomada_decisao",
                "valor_comissao_estimado",
                "spread_estimado"
            FROM public.temp_table as tmp
            where tmp."NUMERO PROPOSTA" IS NOT NULL
            AND NOT EXISTS (
                    SELECT 1
                    FROM contrato
                    WHERE "numero_proposta" = tmp."NUMERO PROPOSTA"
            )

                    '''
