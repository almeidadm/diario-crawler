# Visao geral

## Objetivo

Explicar o que o projeto faz e por que ele existe, de forma simples e direta.

## O que e o Diario SJC Crawler

Um crawler que coleta Diarios Oficiais municipais publicados em formato HTML pela plataforma IONews. Ele organiza o conteudo em dados estruturados para facilitar busca, analise e integracao com sistemas.

## Para quem e

- Gestores e areas de negocio que precisam de dados confiaveis
- Equipes tecnicas que vao integrar os dados em pipelines
- Pesquisadores e analistas

## O que entra e o que sai

Entradas:
- Sites de Diarios Oficiais dos municipios suportados
- Intervalo de datas desejado

Saidas:
- Arquivos estruturados em Parquet
- Conteudos longos podem ser armazenados como blobs
- Metadados prontos para consulta

## Limites e riscos

- Se o site do diario estiver fora do ar, a coleta pode falhar
- Mudancas no HTML podem exigir ajustes nos parsers
- O crawler nao valida o valor juridico do conteudo

## O que nao esta no escopo

- Interpretacao juridica dos textos
- Categorizacao semantica automatica
- Publicacao oficial de dados

## Onde aprender mais

- Veja `docs/guia-rapido.md` para executar
- Veja `docs/arquitetura.md` para entender o fluxo tecnico
- Veja `docs/glossario.md` para termos comuns
