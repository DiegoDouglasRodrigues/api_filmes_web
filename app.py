import streamlit as st
import requests
import urllib.request
import os
import glob

# Funções auxiliares
def limpar_imagens_filmes():
    if os.path.exists('imagens'):
        files = glob.glob('imagens/*.jpg')
        for f in files:
            os.remove(f)
    else:
        os.makedirs('imagens')

def download_imagens():
    api_key = '3adbb5856e462f0378b57334a2d07412'
    link = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1"
    link_imagem = "https://image.tmdb.org/t/p/w500"

    limpar_imagens_filmes()

    response = requests.get(link)
    if response.status_code != 200:
        st.error(f"Erro na requisição: {response.status_code}")
        return []

    informacoes = response.json()
    if 'results' not in informacoes:
        st.error("A chave 'results' não foi encontrada na resposta da API.")
        return []

    lista_filmes = informacoes['results']
    filmes = []

    for filme in lista_filmes:
        titulo = filme.get('original_title', 'Título indisponível')
        nota = filme.get('vote_average', 'Nota indisponível')
        descricao = filme.get('overview', 'Descrição indisponível')
        foto_path = filme.get('backdrop_path', None)

        if foto_path:
            link_capa = f"{link_imagem}{foto_path}"
            img_path = f"imagens/{os.path.basename(foto_path)}"
            try:
                resource = urllib.request.urlopen(link_capa)
                with open(img_path, "wb") as f:
                    f.write(resource.read())
                imagem_local = img_path
            except Exception as e:
                st.error(f"Erro ao baixar a imagem: {e}")
                imagem_local = None
        else:
            imagem_local = None

        filmes.append({
            'titulo': titulo,
            'nota': nota,
            'descricao': descricao,
            'imagem': imagem_local
        })

    return filmes

api_key = '3adbb5856e462f0378b57334a2d07412'

token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYWRiYjU4NTZlNDYyZjAzNzhiNTczMzRhMmQwNzQxMiIsIm5iZiI6MTY3NjgzODkzNS40MDMsInN1YiI6IjYzZjI4ODE3YTI0YzUwMDA3OGM5NDJiNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KG7Dr4pkY1Ji8C4qXU3E0atD-C6CYl9kHof7y42BiuQ'


def download_imagens_series():
    base_url = "https://api.themoviedb.org/3"
    link_series = f"{base_url}/tv/popular?language=en-US&page=1"
    imagem_base_url = "https://image.tmdb.org/t/p/w500"

    limpar_imagens_filmes()

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(link_series, headers=headers)
    if response.status_code != 200:
        st.error(f"Erro na requisição: {response.status_code}")
        return []

    informacoes = response.json()
    if 'results' not in informacoes:
        st.error("A chave 'results' não foi encontrada na resposta da API.")
        return []

    lista_series = informacoes['results']
    series_processadas = []

    for serie in lista_series:
        titulo = serie.get('original_name', 'Título indisponível')
        nota = serie.get('vote_average', 'Nota indisponível')
        descricao = serie.get('overview', 'Descrição indisponível')
        foto_path = serie.get('backdrop_path', None)

        if foto_path:
            link_capa = f"{imagem_base_url}{foto_path}"
            img_path = f"imagens/{os.path.basename(foto_path)}"
            try:
                resource = urllib.request.urlopen(link_capa)
                with open(img_path, "wb") as f:
                    f.write(resource.read())
                imagem_local = img_path
            except Exception as e:
                st.error(f"Erro ao baixar a imagem: {e}")
                imagem_local = None
        else:
            imagem_local = None

        series_processadas.append({
            'titulo': titulo,
            'nota': nota,
            'descricao': descricao,
            'imagem': imagem_local
        })

    return series_processadas

# Configuração inicial do Streamlit
st.set_page_config(page_title="Sistema de Filmes", layout="wide")
st.title("Sistema de Acompanhamento de Filmes e Séries")

# Criação de pastas para imagens, se não existir
if not os.path.exists('imagens'):
    os.makedirs('imagens')

# Menu lateral
menu = st.sidebar.selectbox("Selecione uma opção", ["Filmes Populares", "Series Populares"])

if menu == "Filmes Populares":
    st.subheader("Filmes Populares")
    if st.button("Atualizar Lista de Filmes"):
        st.info("Carregando filmes populares...")
        filmes = download_imagens()
        if filmes:
            st.success("Filmes atualizados com sucesso!")
            for filme in filmes:
                st.subheader(filme['titulo'])
                st.write(f"**Nota**: {filme['nota']}")
                st.write(f"**Descrição**: {filme['descricao']}")
                if filme['imagem']:
                    st.image(filme['imagem'], width=300)
        else:
            st.warning("Nenhum filme encontrado.")

if menu == "Series Populares":
    st.subheader("Séries Populares")
    if st.button("Atualizar Lista de Séries"):
        st.info("Carregando séries populares...")
        series = download_imagens_series()
        if series:
            st.success("Séries atualizadas com sucesso!")
            for serie in series:
                st.subheader(serie['titulo'])
                st.write(f"**Nota**: {serie['nota']}")
                st.write(f"**Descrição**: {serie['descricao']}")
                if serie['imagem']:
                    st.image(serie['imagem'], width=300)
        else:
            st.warning("Nenhuma série encontrada.")


# ok funcionando 07/01