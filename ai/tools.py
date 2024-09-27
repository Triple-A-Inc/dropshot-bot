# Import things that are needed generically
from langchain.tools import tool


DROP_SHOT_ITEMS = [
    {
        "name": "Raquete DROP SHOT SPEKTRO 8.0 BT",
        "category": "Raquete",
        "price": "R$ 949,90",
        "description": "Raquete de beach tennis fabricada com Carbono 18K e EVA Tech, ideal para jogadores que buscam controle absoluto e potência em suas jogadas."
    },
    {
        "name": "Raquete DROP SHOT PREMIUM TECH BT",
        "category": "Raquete",
        "price": "R$ 1.567,41",
        "description": "Raquete de beach tennis com Carbono 18K e sistema anti-vibração, perfeita para jogadores avançados que buscam máxima performance."
    },
    {
        "name": "Raquete DROP SHOT CENTAURO 5.0 BT",
        "category": "Raquete",
        "price": "R$ 1.662,41",
        "description": "Raquete de beach tennis equipada com tecnologias de rigidez e controle, ideal para jogadores profissionais."
    },
    {
        "name": "Raquete DROP SHOT AMBITION PRO 2.0",
        "category": "Raquete",
        "price": "R$ 1.899,91",
        "description": "Raquete de alta performance com design inovador e máxima durabilidade, desenvolvida para jogadores que buscam controle e potência."
    },
    {
        "name": "Bola Oficial DROP SHOT Terno",
        "category": "Bola",
        "price": "R$ 75,91",
        "description": "Bola de Beach Tennis aprovada pela ITF, projetada para proporcionar o melhor desempenho nas quadras de areia."
    },
    {
        "name": "Bola de Beach Tennis DROP SHOT Pro",
        "category": "Bola",
        "price": "R$ 85,90",
        "description": "Bola de beach tennis com alta durabilidade e excelente controle, ideal para treinos e competições."
    },
    {
        "name": "Raqueteira DROP SHOT SIBI",
        "category": "Raqueteira",
        "price": "R$ 759,91",
        "description": "Raqueteira com compartimentos ventilados para calçados e raquetes, ideal para transportar seu equipamento com segurança e estilo."
    },
    {
        "name": "Raqueteira DROP SHOT BENTOR LIMA",
        "category": "Raqueteira",
        "price": "R$ 997,41",
        "description": "Projetada com materiais resistentes e compartimentos organizados, oferecendo espaço e proteção para os seus itens."
    },
    {
        "name": "Raqueteira DROP SHOT AIRAM JMD",
        "category": "Raqueteira",
        "price": "R$ 1.049,90",
        "description": "Raqueteira de alta capacidade, com design sofisticado e múltiplos compartimentos para máxima organização e proteção dos equipamentos."
    },
    {
        "name": "Tênis DROP SHOT CAYENNE",
        "category": "Vestuário",
        "price": "R$ 569,91",
        "description": "Tênis com tecnologia de amortecimento e aderência para movimentos ágeis nas quadras, perfeito para jogadores de beach tennis."
    },
    {
        "name": "Tênis DROP SHOT ABIAN CAMPA",
        "category": "Vestuário",
        "price": "R$ 999,90",
        "description": "Usado pelo jogador Lucas Campagnolo, oferece segurança, conforto e estabilidade para máxima performance no padel."
    },
    {
        "name": "Tênis DROP SHOT BENARA LIMA",
        "category": "Vestuário",
        "price": "R$ 949,91",
        "description": "Combina design moderno com tecnologias avançadas de suporte e amortecimento, ideal para intensos jogos de beach tennis."
    },
    {
        "name": "Camiseta DROP SHOT TECH DRY",
        "category": "Vestuário",
        "price": "R$ 159,90",
        "description": "Camiseta com tecnologia de secagem rápida e tecido respirável, proporcionando conforto em treinos e jogos."
    },
    {
        "name": "Shorts DROP SHOT PRO PLAYER",
        "category": "Vestuário",
        "price": "R$ 199,90",
        "description": "Shorts esportivo com ajuste perfeito e tecido leve, ideal para movimentos rápidos e precisos nas quadras."
    },
    {
        "name": "Boné DROP SHOT SUN PROTECT",
        "category": "Acessório",
        "price": "R$ 89,90",
        "description": "Boné com proteção UV e tecido respirável, ideal para proteger durante os treinos ao ar livre."
    },
    {
        "name": "Munhequeira DROP SHOT COMFORT",
        "category": "Acessório",
        "price": "R$ 49,90",
        "description": "Munhequeira com tecido absorvente e ajuste confortável, ideal para oferecer suporte extra durante o jogo."
    },
    {
        "name": "Corda DROP SHOT POWER STRIKE",
        "category": "Acessório",
        "price": "R$ 59,90",
        "description": "Corda de alta durabilidade para raquetes, proporcionando maior potência e controle nos golpes."
    },
    {
        "name": "Mochila DROP SHOT SPORT",
        "category": "Acessório",
        "price": "R$ 349,90",
        "description": "Mochila com múltiplos compartimentos, ideal para transporte de raquetes, roupas e acessórios de forma prática e segura."
    },
    {
        "name": "Bolsa DROP SHOT URBAN",
        "category": "Acessório",
        "price": "R$ 299,90",
        "description": "Bolsa esportiva estilosa com espaço para todos os seus pertences, perfeita para uso dentro e fora das quadras."
    },
    {
        "name": "Grip DROP SHOT TACKY FEEL",
        "category": "Acessório",
        "price": "R$ 29,90",
        "description": "Grip com aderência superior, proporcionando maior conforto e firmeza na pegada durante o jogo."
    }
]


@tool
def get_itens() -> str:
    """
        Busca os itens disponíveis para a venda no site da DropShot.   
    """
    return DROP_SHOT_ITEMS