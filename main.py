import zeep
from requests import Session
from zeep.transports import Transport
from OpenSSL import crypto


CERTIFICADO = "certificado.pfx"
SENHA_CERTIFICADO = "sua_senha"

# Web Service da SEFAZ para consulta (URL de homologação ou produção)
WS_URL = "https://hom.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx?wsdl"

# CNPJ a ser consultado
CNPJ = "02.916.265/0001-60" #CPNJ JBS Exemplo.


def carregar_certificado(cert_path, senha):
    with open(cert_path, "rb") as f:
        pfx = crypto.load_pkcs12(f.read(), senha.encode())
    return pfx


def criar_sessao(cert_path, senha):
    cert = (cert_path, senha)  # Certificado digital
    session = Session()
    session.verify = False
    session.cert = cert
    return session


def consultar_nfe(cnpj):
    session = criar_sessao(CERTIFICADO, SENHA_CERTIFICADO)

    client = zeep.Client(wsdl=WS_URL, transport=Transport(session=session))


    xml_requisicao = f"""
    <distDFeInt xmlns="http://www.portalfiscal.inf.br/nfe" versao="1.00">
        <tpAmb>1</tpAmb>  <!-- 1 = Produção, 2 = Homologação -->
        <cUFAutor>35</cUFAutor>  <!-- Código do Estado (35 = SP, 41 = PR, etc.) -->
        <CNPJ>{cnpj}</CNPJ>
        <distNSU>
            <ultNSU>000000000000000</ultNSU>
        </distNSU>
    </distDFeInt>
    """

    # Enviar requisição
    response = client.service.nfeDistDFeInteresse(xml_requisicao)

    return response

# Chamada da função
xml_resposta = consultar_nfe(CNPJ)

# Salvar resposta XML em arquivo
with open("resposta_nfe.xml", "w", encoding="utf-8") as f:
    f.write(xml_resposta)

print("Consulta concluída! XML salvo.")