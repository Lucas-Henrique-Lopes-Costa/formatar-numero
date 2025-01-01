import pandas as pd
import re
import os

# Função para formatar os números de telefone
def format_phone(full_phone):
    full_phone = re.sub(r"\D", "", str(full_phone))  # Remove caracteres não numéricos

    # Assume DDI como 55 se não fornecido
    if len(full_phone) == 10:  # Apenas DDD + número (ex: 1198765432)
        ddi = "55"
        ddd = full_phone[:2]
        phone = full_phone[2:]
    elif len(full_phone) == 11:  # DDD + número com 9 dígitos (ex: 11998765432)
        ddi = "55"
        ddd = full_phone[:2]
        phone = full_phone[2:]
    elif len(full_phone) == 12:  # DDI + DDD + número (ex: 551198765432)
        ddi = full_phone[:2]
        ddd = full_phone[2:4]
        phone = full_phone[4:]
    else:
        return "Formato inválido"  # Retorna mensagem se o número não for válido

    # Lógica para formatação com base no DDD
    if int(ddd) > 28:
        if len(phone) == 9:
            phone = phone[1:]  # Remove o primeiro dígito se tiver 9 dígitos
    else:
        if len(phone) == 8:
            phone = '9' + phone  # Adiciona o '9' se tiver 8 dígitos

    # Retorna no formato E.164
    return f"+{ddi}{ddd}{phone}"

# Carrega os dados da planilha com verificacao de existencia do arquivo
file_path = "planilha.csv"  # Substitua pelo caminho do seu arquivo
output_path = "planilha_formatada.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado. Verifique o caminho e tente novamente.")

# Carrega a planilha CSV
df = pd.read_csv(file_path)

# Verifica se a coluna TELEFONE existe
if 'TELEFONE' not in df.columns:
    raise ValueError("A coluna 'TELEFONE' não foi encontrada na planilha. Verifique o arquivo CSV.")

# Aplica a formatação ao campo TELEFONE
df['formattedPhone'] = df['TELEFONE'].apply(format_phone)

# Salva os resultados em um novo arquivo CSV
df.to_csv(output_path, index=False)
print(f"Resultados salvos em {output_path}")
