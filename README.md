# Problema de negócio

A empresa No Hunger é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da No Hunger, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
O CEO também foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a No Hunger, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises.
O objetivo desse projeto é criar um conjunto de gráficos e tabelas que exibam métricas da melhor forma possível para o CEO.

# Premissas

1.	As análises foram realizadas com os dados da empresa disponíveis até a dia 02-04-2024, não sendo atualizado na posterioridade.
2.	Marketplace foi o modelo de negócio assumido.
3.	As 4 principais visões de negócio foram: Visão Geral, Visão dos Países, Visão das Cidades e Visão dos Tipos de Culinária.
4.	O valor de conversão da moeda moeda local de cada país para dólar foi baseado na cotação da data de 03-04-2024.
   
# Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as princpais visões do modelo de negócio da empresa:
1.	Visão Geral
2.	Visão de Crescimento dos Países
3.	Visão de Crescimento das Cidades
4.	Visão Tipos de Culinária
   
## Visão Geral (Main Page)
a.	Número de restaurantes cadastrados 

b.	Número de países em que No Hunger está presente

c.	Número de Cidades em que a No Hunger está presente

d.	Número total de avaliações de restaurantes já realizadas na plataforma

e.	Quantidade de tipos de culinária servidas pelos restaurantes cadastrados na No Hunger

f.	Mapa com a localização exata de cada restaurante cadastrado na No Hunger

## Visão de Crescimentos dos Países (Country View)

### Overview:
a.	Número e porcentagem de restaurantes cadastrados em cada país

b.	Número  e porcentagem de cidades atendidas em cada país 

### Price/Rating Analyses:

a.	Comparação entre preço médio, avaliação média e número de avaliações realizadas em cada país

b.	Ranking de notas média dos restaurantes de cada país

c.	Ranking com a média do número de avaliações realizadas nos restaurantes de cada país

d.	Ranking de países baseado no preço médio de uma refeição para duas pessoas

## Visão de Crescimento das Cidades (City View)
### Overview:
a.	Ranking das dez cidades com o maior número de restaurantes cadastrados

b.	Ranking das dez cidades com a maior diversidade de tipos de culinárias 

### Price/Rating Analyses:
a.	Ranking das sete cidades com o maior preço de refeição

b.	Ranking com as sete cidades mais baratas 

c.	Ranking com as sete cidades com o maior número de restaurantes bem avaliados (rating de 4.0 ou mais)

d.	Ranking das sete cidades com o maior número de restaurantes com baixa avaliação (rating de 2.5 ou menos)

## Visão Tipos de Culinária
a.	Os melhores restaurantes (baseado na avaliação média e no número de avaliações registradas) que servem os principais tipos de culinárias globais

b.	O TOP 10 melhores restaurantes cadastrados na No Hunger (baseado na avaliação média e no número de avaliações registradas)

c.	Os dez tipos de culinária melhor avaliados na plataforma

d.	Os dez tipos de culinária pior avaliados na plataforma

# Top 3 insights de dados
1.	A Índia é o país é o país em que compreende o maior número de cidades atendidas pela Nu Hunger, bem como o país que contém maior número de restaurantes cadastrados, representado 45% do total da base de dados. 
2.	A maioria das cidades que contém o menor preço médio por refeição para duas pessoas estão localizadas na Índia.
3.	Todas as cidades brasileiras registradas no No hunger estão no top sete com o maior número de restaurantes mal avaliados.

# O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painal pode ser acessado através desse link: https://no-hunger.streamlit.app/

# Conclusão
O objetivo desse projeto foi criar um conjunto de gráficos e tabelas que exibam as métricas gerais em um certo momento da empresa para o CEO.
Podemos concluir em que a No Hunger tem uma presença relevante mundialmente, estando presente em todos os continentes. Apesar de estar fortemente consolidada em alguns países como a India e Estados Unidos, ainda existem países em que há um grande potencial de expansão, como por exemplo o Brasil, que apesar de ser um país grande em termos de território e população, está presente apenas em poucas capitais. 

## Próximos passos
1.	Reduzir o número de métricas.
2.	Criar novos filtros que permitam maior interação ao usuário.
3.	Adicionar Visão Geográfica, que possibilite comparação dos dados da empresa com os dados socioeconomicos ou demográficos de países em que a No Hunger potencialmente pode expadir sua relevancia.
