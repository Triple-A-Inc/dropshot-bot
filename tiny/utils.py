# Mapeamento de status de processamento
processing_status = {
    1: "Solicitação não processada",
    2: "Solicitação processada, mas possui erros de validação",
    3: "Solicitação processada corretamente",
    4: "Solicitação parcialmente processada"
}

error_codes = {
    1: "token não informado",
    2: "token inválido ou não encontrado",
    3: "XML mal formado ou com erros",
    4: "Erro de procesamento de XML",
    5: "API bloqueada ou sem acesso",
    6: "API bloqueada momentaneamente - muitos acessos no último minuto",
    7: "Espaço da empresa Esgotado",
    8: "Empresa Bloqueada",
    9: "Números de sequencia em duplicidade",
    10: "Parametro não informado",
    11: "API bloqueada momentaneamente - muitos acessos concorrentes",
    20: "A Consulta não retornou registros",
    21: "A Consulta retornou muitos registros",
    22: "O xml tem mais registros que o permitido por lote de envio",
    23: "A página que você está tentanto obter não existe",
    30: "Erro de Duplicidade de Registro",
    31: "Erros de Validação",
    32: "Registro não localizado",
    33: "Registro localizado em duplicidade",
    34: "Nota Fiscal não autorizada",
    35: "Ocorreu um erro inesperado, tente novamente mais tarde",
    99: "Sistema em manutenção"
}


def get_search_url(product_name: str) -> str:
    '''
    Essa função deve parsear um nome de produto para um link de pesquisa no site da dropshot

    Ex: 
    INPUT: Agasalho DROP SHOT AIRAM JMD
    OUTPUT: https://www.dropshot.com.br/produtos?q=Agasalho+DROP+SHOT+AIRAM+JMD
    '''

    base_url = 'https://www.dropshot.com.br/'


    search_link = base_url + product_name.replace(' ', '-')

    return search_link



