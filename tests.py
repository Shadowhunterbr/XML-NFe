import requests
import logging
import zeep
from lxml import etree
from OpenSSL import crypto
from requests import Session
from zeep.transports import Transport


WS_URL = "https://nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx?wsdl"

CERTIFICADO = "certificado.pfx"
SENHA_CERTIFICADO = "sua_senha"


def testar_certificado(cert_path, senha):
    try:
        with open(cert_path, "rb") as f:
            #pfx = crypto.load_pkcs12(f.read(), senha.encode())
            crypto.load_pkcs12(f.read(), senha.encode())
        print(" Certificado carregado com sucesso")
    except Exception as e:
        print(f" Erro ao carregar certificado: {e}")

testar_certificado(CERTIFICADO, SENHA_CERTIFICADO)


URL_TESTE = "https://hom.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx?wsdl"

try:
    response = requests.get(URL_TESTE, verify=False)
    if response.status_code == 200:
        print(f"✅ Conectado à SEFAZ Status Code: {response.status_code}")
    else:
        print(f"⚠️ Resposta da SEFAZ: {response.status_code}")
except Exception as e:
    print(f"❌ Erro ao conectar à SEFAZ: {e}")


def criar_sessao(cert_path, senha):
    session = Session()
    session.verify = False
    session.cert = (cert_path, senha)
    return session

sessao = criar_sessao(CERTIFICADO, SENHA_CERTIFICADO)


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("zeep").setLevel(logging.DEBUG)

try:
    client = zeep.Client(wsdl=WS_URL, transport=Transport(session=sessao))
    print("Cliente SOAP criado com sucesso!")
except Exception as e:
    print(f" Erro ao criar cliente SOAP: {e}")
