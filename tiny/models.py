from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, List
from datetime import datetime

# Function arguments ==============================================
class ParamSearchProduct(BaseModel):
    token: str = Field(..., description="Chave gerada para identificar sua empresa")
    formato: str = Field('JSON', description="Formato do retorno (json)")
    pesquisa: str = Field(..., description="Nome ou código (ou parte) do produto que deseja consultar")
    idTag: Optional[int] = Field(None, description="Número de identificação da tag no Tiny")
    idListaPreco: Optional[int] = Field(None, description="Número de identificação da lista de preço no Tiny")
    pagina: Optional[int] = Field(None, description="Número da página")
    gtin: Optional[str] = Field(None, description="GTIN/EAN do produto")
    situacao: Optional[str] = Field(None, description='Situação dos produtos ("A" - Ativo, "I" - Inativo ou "E" - Excluído)')
    dataCriacao: Optional[datetime] = Field(None, description="Data de criação do produto. Formato dd/mm/aaaa hh:mm:ss")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "chave123",
                "formato": "json",
                "pesquisa": "produto123",
                "idTag": 123,
                "idListaPreco": 1,
                "pagina": 2,
                "gtin": "12345678901234",
                "situacao": "A",
                "dataCriacao": "01/01/2024 12:00:00"
            }
        }

class ParamGetSupply(BaseModel):
    token: str = Field(..., description="Chave gerada para identificar sua empresa")
    id: int = Field(..., description="Número de identificação do produto no Tiny")
    formato: str = Field('JSON', description="Formato do retorno (json)")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "chave123",
                "id": 101,
                "formato": "json"
            }
        }



# Function returns ==============================================

class Erro(BaseModel):
    erro: str = Field(..., description="Mensagem contendo a descrição do erro")

class Deposito(BaseModel):
    nome: str = Field(..., description="Nome do depósito", max_length=120)
    desconsiderar: Optional[str] = Field(None, description="Desconsidera o saldo do depósito (S/N)", max_length=1)
    saldo: Optional[Decimal] = Field(None, description="Saldo do estoque no depósito")
    empresa: Optional[str] = Field(None, description="Apelido da empresa", max_length=120)

class EstoqueProduto(BaseModel):
    id: Optional[int] = Field(None, description="Número de identificação do produto no Tiny")
    nome: Optional[str] = Field(None, description="Nome do produto", max_length=120)
    codigo: Optional[str] = Field(None, description="Código do produto", max_length=30)
    unidade: Optional[str] = Field(None, description="Unidade do produto", max_length=3)
    saldo: Optional[Decimal] = Field(None, description="Saldo em estoque")
    saldoReservado: Optional[Decimal] = Field(None, description="Saldo reservado em estoque")
    depositos: Optional[List[Deposito]] = Field(None, description="Lista de depósitos do produto")

class EstoqueRetorno(BaseModel):
    status_processamento: int = Field(..., description="Conforme tabela 'Status de Processamento'")
    status: str = Field(..., description="Contém o status do retorno 'OK' ou 'Erro'")
    codigo_erro: Optional[int] = Field(None, description="Conforme tabela 'Códigos de erro'")
    erros: Optional[List[Erro]] = Field(None, description="Contém a lista dos erros encontrados")
    produto: Optional[EstoqueProduto] = Field(None, description="Elemento utilizado para representar o produto")


class GetProductObject(BaseModel):
    id: int = Field(..., description="Número de identificação do produto no Tiny")
    nome: str = Field(..., description="Nome do produto", max_length=120)
    codigo: Optional[str] = Field(None, description="Código do produto", max_length=30)
    preco: Decimal = Field(..., description="Preço de venda do produto")
    preco_promocional: Decimal = Field(..., description="Preço promocional do produto")
    preco_custo: Optional[Decimal] = Field(None, description="Preço de custo do produto")
    preco_custo_medio: Optional[Decimal] = Field(None, description="Preço médio de custo do produto")
    unidade: Optional[str] = Field(None, description="Unidade do produto", max_length=3)
    gtin: Optional[str] = Field(None, description="GTIN/EAN do produto", max_length=14)
    tipoVariacao: str = Field(..., description="Tipo de variação 'N' - Normal, 'P' - Pai, 'V' - Variação", max_length=1)
    localizacao: Optional[str] = Field(None, description="Localização física no estoque", max_length=50)
    situacao: Optional[str] = Field(None, description="Situação dos produtos ('A' - Ativo, 'I' - Inativo, 'E' - Excluído)", max_length=1)
    data_criacao: Optional[datetime] = Field(None, description="Data de criação do produto. Formato dd/mm/aaaa hh:mm:ss")

class GetProductReturn(BaseModel):
    status_processamento: int = Field(..., description="Conforme tabela 'Status de Processamento'")
    status: str = Field(..., description="Contém o status do retorno 'OK' ou 'Erro'")
    codigo_erro: Optional[int] = Field(None, description="Conforme tabela 'Códigos de erro'")
    erros: Optional[List[Erro]] = Field(None, description="Contém a lista dos erros encontrados")
    pagina: int = Field(..., description="Número da página que está sendo retornada")
    numero_paginas: int = Field(..., description="Número de páginas do retorno")
    produtos: Optional[List[GetProductObject]] = Field(None, description="Lista de resultados da pesquisa")


# Classe principal -> RETORNO DE ESTOQUE
class SupplyReturnObject(BaseModel):
    retorno: EstoqueRetorno = Field(..., description="Elemento raiz do retorno")

    class Config:
        json_schema_extra = {
            "example": {
                "retorno": {
                    "status_processamento": 1,
                    "status": "OK",
                    "codigo_erro": None,
                    "erros": [],
                    "produto": {
                        "id": 123,
                        "nome": "Produto Exemplo",
                        "codigo": "PROD123",
                        "unidade": "UN",
                        "saldo": 100.50,
                        "saldoReservado": 20.0,
                        "depositos": [
                            {
                                "nome": "Depósito Central",
                                "desconsiderar": "N",
                                "saldo": 50.0,
                                "empresa": "Empresa X"
                            }
                        ]
                    }
                }
            }
        }

# Classe principal -> RETORNO DE CONSULTA DE PRODUTO
class GetProductReturnObject(BaseModel):
    retorno: GetProductReturn = Field(..., description="Elemento raiz do retorno")

    class Config:
        json_schema_extra = {
            "example": {
                "retorno": {
                    "status_processamento": 3,
                    "status": "OK",
                    "codigo_erro": None,
                    "erros": [],
                    "pagina": 1,
                    "numero_paginas": 5,
                    "produtos": [
                        {
                            "id": 123,
                            "nome": "Produto Exemplo",
                            "codigo": "PROD123",
                            "preco": 100.50,
                            "preco_promocional": 90.00,
                            "preco_custo": 70.00,
                            "preco_custo_medio": 72.50,
                            "unidade": "UN",
                            "gtin": "12345678901234",
                            "tipoVariacao": "N",
                            "localizacao": "Estoque Central",
                            "situacao": "A",
                            "data_criacao": "01/01/2024 12:00:00"
                        }
                    ]
                }
            }
        }