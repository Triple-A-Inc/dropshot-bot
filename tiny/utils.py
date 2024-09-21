

def get_search_url(product_name: str) -> str:
    '''
    Essa função deve parsear um nome de produto para um link de pesquisa no site da dropshot

    Ex: 
    INPUT: Agasalho DROP SHOT AIRAM JMD
    OUTPUT: https://www.dropshot.com.br/produtos?q=Agasalho+DROP+SHOT+AIRAM+JMD
    '''

    base_url = 'https://www.dropshot.com.br/produtos?q='

    search_link = base_url + product_name.replace(' ', '+')

    return search_link

