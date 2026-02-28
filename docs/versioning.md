## Versioning Strategy

Este projeto segue Semantic Versioning (SemVer) com regras adaptadas para contratos de dados imutáveis.

- **MAJOR** — alterações breaking: renomear ou remover campos, mudar o tipo de um campo público (ex.: `datetime` → `date`), ou alterar a configuração de `ContractModel` (`frozen`, `extra`, `validate_assignment`). Essas mudanças exigem aumento do MAJOR (ex.: 1.x → 2.0.0).

- **MINOR** — adições compatíveis: adicionar novos modelos, adicionar campos opcionais/with default, exportar novos módulos/objetos que não alteram contratos existentes. Publicar como MINOR quando consumidores existentes não precisam mudar.

- **PATCH** — correções e documentação: bugfixes, documentação, testes, ajustes internos que não alteram a API dos contratos (ex.: consertar `default_factory` em uma lista quando comportamento público não muda).

### Mapas de exemplo (aplicados ao repositório)

- `CHANGELOG.md` [1.0.4]: adicionou `ParsedArticle`, `TextChunk`, `EmbeddedChunk`, `RetrievedDocument`, `RAGAnswer`. Essas são novas entidades — devem ser lançadas como **MINOR** (p.ex. `1.1.0`) a menos que retirem ou alterem contratos existentes.
- Mudança de `publication_date` para `datetime.date`: isso altera o tipo e pode quebrar consumidores — trate como **MAJOR**, a menos que haja evidência clara de que consumidores já esperavam `date` (documente essa decisão no changelog).
- Correção de `GazetteEdition.articles` para usar `default_factory`: comportamento esperado corrigido — **PATCH**.

### Procedimento de release recomendado

1. Atualize `pyproject.toml` > `version` para a nova versão.
2. Execute os testes: 

```bash
python -m pytest
```

3. Atualize `CHANGELOG.md` com as notas de release (resumir impacto e indicar se é breaking).
4. Commit e tag:

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): x.y.z"
git tag vX.Y.Z
git push --follow-tags
```

5. Publicação (consumidores podem instalar via pip apontando para a tag/versão):

```bash
pip install git+ssh://git@github.com:almeidadm/diario-contract.git@vX.Y.Z
```

### Dicas rápidas para agentes

- Verifique `diario_contract/base.py` para regras globais de validação/imutabilidade.
- Ao introduzir campos novos, prefira torná-los opcionais (`str | None`) para evitar breaking changes.
- Documente decisões de compatibilidade no `CHANGELOG.md` e referencie exemplos de arquivos que mudaram (ex.: `diario_contract/gazette/edition.py`, `tests/test_contract_models.py`).

### Exemplos de decisão

- Adição de `ParsedArticle` (novo modelo): **MINOR** — adiciona capacidades sem quebrar contratos existentes.
- Alterar `publication_date` tipo `datetime` → `date`: **MAJOR** (breaking) — requer comunicação com consumidores.
- Corrigir default de lista (`default_factory=list`): **PATCH** — bugfix.

