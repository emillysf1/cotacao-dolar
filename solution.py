import datetime
import requests


def cotar():
    hoje = datetime.date.today()

    for i in range(365):
        dia = hoje - datetime.timedelta(days=i)
        data = dia.strftime("%m-%d-%Y")

        url = (
            "https://olinda.bcb.gov.br/olinda/servico/"
            "PTAX/versao/v1/odata/"
            "CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)"
        )

        parametros = {
            "@moeda": "'USD'",
            "@dataCotacao": f"'{data}'",
            "$format": "json"
        }

        try:
            resposta = requests.get(
                url,
                params=parametros,
                timeout=10
            )
            resposta.raise_for_status()

            dados = resposta.json()
            cotacoes = dados.get("value", [])

            if cotacoes:
                fechamentos = [
                    cotacao
                    for cotacao in cotacoes
                    if cotacao.get("tipoBoletim") == "Fechamento"
                ]

                cotacao = (
                    fechamentos[-1]
                    if fechamentos
                    else cotacoes[-1]
                )

                valor = cotacao.get("cotacaoCompra")

                if valor is not None:
                    print(f"{dia:%d/%m/%Y}: R$ {valor:.4f}")
                else:
                    print(f"{dia:%d/%m/%Y}: Cotação indisponível")
            else:
                print(f"{dia:%d/%m/%Y}: Sem cotação")

        except (requests.RequestException, ValueError) as erro:
            print(f"{dia:%d/%m/%Y}: Erro na consulta - {erro}")


if __name__ == "__main__":
    cotar()