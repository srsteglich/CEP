import streamlit as st
import requests
# Esse aplicativo digita o CEP e retorna o endereço completo.
def buscar():      
    st.subheader("Consultar CEP")
    cep = st.text_input("Digite o seu CEP:")
    
    if st.button("Buscar"):
        if cep:
            cep = cep.replace("-", "").replace(".", "").replace(" ", "")
            if not cep.isdigit():
                st.error("CEP inválido! Digite apenas números.")
                
            elif len(cep) != 8:
                st.error("CEP inválido! Digite com 8 números.")         

            else:
                link = f'https://viacep.com.br/ws/{cep}/json/'
                req = requests.get(link)
                dic_req = req.json()
                if 'erro' in dic_req:
                    st.error("CEP não encontrado.")               
                else:
                    rua = dic_req['logradouro']
                    comple = dic_req['complemento']
                    bairro = dic_req['bairro']
                    cidade = dic_req['localidade']
                    uf = dic_req['uf']
                    cep = dic_req['cep']
                    st.write(f"Endereço: {rua}  - {comple} ")
                    st.write(f"Bairro:  {bairro}")
                    st.write(f"Cidade: {cidade} / {uf}")
                    st.write(f"CEP: {cep}")

buscar()                