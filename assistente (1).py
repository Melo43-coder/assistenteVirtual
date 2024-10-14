from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
import sys
from datetime import datetime
import webbrowser as browser
from bs4 import BeautifulSoup
from requests import get
import requests
from requests.structures import CaseInsensitiveDict
import json
import urllib.request

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer live_c01c5b77b6240e3b815bab2e327964"
url = "https://api.api-futebol.com.br/v1/campeonatos/10/tabela"

def cria_audio(audio,mensagem, lang="pt-br"):
	tts = gTTS(mensagem, lang=lang)
	tts.save(audio)
	playsound(audio)
	os.remove(audio)

cria_audio("audios/welcome.mp3", "Olá. Sou a Maria. Em que posso ajudá-lo?")

def monitora_audio():
	recon = sr.Recognizer()
	with sr.Microphone() as source:
		while True:
			print("Diga algo")
			audio = recon.listen(source)
			try:
				mensagem = recon.recognize_google(audio, language='pt-br')
				mensagem = mensagem.lower()
				print("Você disse", mensagem)
				executa_comandos(mensagem)
				break
			except sr.UnknownValueError:
				pass
			except sr.RequestError:
				pass
		return mensagem

def executa_comandos(mensagem):
	if 'fechar assistente' in mensagem:
		sys.exit()
	elif 'horas' in mensagem:
		hora = datetime.now().strftime("%H:%M")
		frase = f"Agora são{hora}"
		cria_audio("audios/mensagem.mp3",frase)
	elif 'desligar computador' in mensagem and 'uma hora' in mensagem:
		os.system("shutdown -s -t 3600")
	elif 'desligar computador' in mensagem  and 'meia hora' in mensagem:
		os.system("shutdown -s -t 1800")
	elif 'cancelar desligamento' in mensagem:
		os.system("shutdown -a")
	elif 'toca' in mensagem  and 'libertadores' in mensagem:
		playlists('libertadores')
	elif 'toca' in mensagem  and 'instrumental' in mensagem:
		playlists('instrumental')
	elif 'toca' in mensagem and 'jogo' in mensagem:
		playlists('jogo')
	elif 'toca' in mensagem and 'série' in mensagem:
		playlists('serie')
	elif 'notícias' in mensagem:
		ultimas_noticias()
	elif 'cotação' in mensagem  and 'dólar' in mensagem:
		cotacao_moeda("Dólar")
	elif 'cotação' in mensagem  and 'euro' in mensagem:
		cotacao_moeda("Euro")
	elif 'cotação' in mensagem  and 'bitcoin' in mensagem:
		cotacao_moeda("Bitcoin")
	elif 'times' in mensagem and 'primeiras colocações' in mensagem:
		lista_g6()
	elif 'times' in mensagem and 'zona de rebaixamento' in mensagem:
		lista_rebaixamento()
	elif 'filmes' in mensagem  and 'populares' in mensagem:
		lista_filmes('popular')
	elif 'filmes' in mensagem and 'kids' in mensagem:
		lista_filmes('kids')
	elif 'filmes' in mensagem  and '2010' in mensagem:
		lista_filmes('2010')
	elif 'filmes' in mensagem  and 'drama' in mensagem:
		lista_filmes('drama')
	elif 'listar' in mensagem and 'cursos' in mensagem:
		lista_cursos()


def ultimas_noticias():
	site = get("https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt")
	noticias = BeautifulSoup(site.text, 'html.parser')
	for item in noticias.findAll('item')[:7]:
		mensagem = item.title.text
		cria_audio("audios/mensagem.mp3",mensagem)

def cotacao_moeda(moeda):
	if moeda == "Dólar":
		requisicao = get('https://economia.awesomeapi.com.br/all/USD-BRL')
		cotacao = requisicao.json()
		nome = cotacao['USD']['name']
		data = cotacao['USD']['create_date']
		valor = cotacao['USD']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio("audios/mensagem.mp3",mensagem)
	elif moeda == "Euro":
		requisicao = get('https://economia.awesomeapi.com.br/all/EUR-BRL')
		cotacao = requisicao.json()
		nome = cotacao['EUR']['name']
		data = cotacao['EUR']['create_date']
		valor = cotacao['EUR']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio("audios/mensagem.mp3",mensagem)
	elif moeda == "Bitcoin":
		requisicao = get('https://economia.awesomeapi.com.br/all/BTC-BRL')
		cotacao = requisicao.json()
		nome = cotacao['BTC']['name']
		data = cotacao['BTC']['create_date']
		valor = cotacao['BTC']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio("audios/mensagem.mp3",mensagem)



def playlists(musica):
	if musica == 'libertadores':
		browser.open('https://open.spotify.com/track/5OWl1Xzj3bL07Gj5LBDMuP?si=178d49aef76b4d6c')
	elif musica == 'instrumental':
		browser.open('https://open.spotify.com/track/0enLtCNBPxgqHQJ68Uk1H8?si=c95097c06d344136')
	elif musica == 'jogo':
		browser.open('https://open.spotify.com/track/00jNnMfEuG861HUy37Mo6Q?si=028f0d1ca36d436e')
	elif musica == 'filme':
		browser.open('https://open.spotify.com/track/1FL7eUG80aeUeyMO2N4btN?si=0d4490e925904e92')
	elif musica == 'serie':
		browser.open('https://open.spotify.com/track/2hsLpiKNkWpd4e9QuVdhar?si=ffb498c00b1548ce')

def lista_g6():
	response = requests.get(url, headers=headers)
	classificacao = json.loads(response.text)
	for g6 in classificacao[:6]:
		times = g6["time"]["nome_popular"]
		cria_audio("audios/mensagem.mp3", times)

def lista_rebaixamento():
	response = requests.get(url, headers=headers)
	classificacao = json.loads(response.text)
	for z4 in classificacao[-4:]:
		times = z4["time"]["nome_popular"]
		s = times.encode()
		cria_audio("audios/mensagem.mp3", times)

def lista_filmes(recurso):
	if recurso == 'popular':
		url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13"
	elif recurso == 'kids':
		url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13"
	elif recurso == '2010':
		url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13"
	elif recurso == 'drama':
		url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=3ddc9b92db4de6c6559569c67bd88a13"
	
	resposta = urllib.request.urlopen(url)
	dados = resposta.read()
	jsondata = json.loads(dados)
	filmes = jsondata['results']
	for filme in filmes[:5]:
		cria_audio("audios/mensagem.mp3",filme['title'],"en")

def lista_cursos():
	URL = "http://localhost:5000/cursos"
	API_KEY = "cb1a7f93-001b-4b86-b0b3-95f30bcfabde"
	PARAMS = {'api_key':API_KEY}
	response = requests.get(url=URL, params=PARAMS)
	cursos = json.loads(response.text)
	cursos = cursos['results']
	for curso in cursos:
		nome = curso['nome']
		descricao = curso['descricao']
		data = curso['data_publicacao']
		texto = f'Curso {nome} tem descrição {descricao} e foi criado em {data}'
		cria_audio("audios/mensagem.mp3", texto)
	

def main():
	while True:
		monitora_audio()

main()