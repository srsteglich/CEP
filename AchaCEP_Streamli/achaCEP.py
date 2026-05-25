import streamlit as st
import pandas as pd
import requests
#Esse aplicativo é para achar o mostrar qual o CEP da cidade e endereço digitado pelo usuário.
def main():
    st.subheader("Consulta de CEP")
    st.markdown("""
    <style>
    .big-font {
        font-size:18px !important;
        color: #00FFFF;
    }
    </style>
    """, unsafe_allow_html=True)    
    st.markdown('<p class="big-font">Encontrar o seu CEP, digite pelo menos quatro letras para cidade e endereço</p>', unsafe_allow_html=True) 
    # Formulário de entrada
    with st.form(key='cep_form'):
        uf = st.text_input("Digite a UF (Estado):", max_chars=2).upper()
        cidade = st.text_input("Digite a Cidade:")
        endereco = st.text_input("Digite o Endereço:")
        submit_button = st.form_submit_button(label='Consultar')    
    if submit_button:
        if not uf.isalpha() or len(uf) != 2:
            st.error("UF deve conter exatamente 2 letras!")
        elif len(cidade) < 4 or len(endereco) < 4:
            st.warning("Cidade e Endereço devem ter pelo menos 4 caracteres!")
        else:
            try:
                link = f'https://viacep.com.br/ws/{uf}/{cidade}/{endereco}/json/'
                req = requests.get(link)
                dic_req = req.json()               
                if not dic_req:
                    st.error("Nenhum resultado encontrado para os dados informados!")
                else:
                    # Processa os dados
                    st.markdown('Encontramos os seguintes dados:')
                    tabela = pd.DataFrame(dic_req)        
                    tabela.rename(columns={
                        'cep':'CEP',
                        'logradouro':'Endereço',
                        'complemento':'Complemento',
                        'bairro':'Bairro',
                        'localidade':'Cidade',
                        'estado':'Estado',
                        'uf':'UF',
                        'regiao':'Região',
                        'ddd':'DDD',
                    }, inplace=True)                    
                    # Remove colunas não necessárias
                    cols_to_drop = ['unidade','ibge', 'gia', 'siafi']
                    for col in cols_to_drop:
                        if col in tabela.columns:
                            tabela.drop(col, axis=1, inplace=True)                  
                    # Exibe a tabela
                    st.dataframe(tabela)                   
            except Exception as e:
                st.error(f"Ocorreu um erro na consulta: {str(e)}")

if __name__ == '__main__':
    main()