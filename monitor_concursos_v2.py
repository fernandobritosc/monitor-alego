name: Monitor de Concursos

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    # Adicionando permissões explícitas para o bot poder salvar o arquivo JSON
    permissions:
      contents: write

    steps:
    - name: Checkout do repositório
      uses: actions/checkout@v3

    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Instalar dependências
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4

    - name: Executar o script de monitoramento
      env:
        TOKEN_TELEGRAM: ${{ secrets.TOKEN_TELEGRAM }}
        ID_TELEGRAM: ${{ secrets.ID_TELEGRAM }}
      run: |
        # IMPORTANTE: O nome do arquivo aqui deve ser EXATAMENTE o nome do seu arquivo .py no GitHub
        # Se o seu arquivo se chama 'final_monitor_bot.py', mude a linha abaixo:
        python monitor_concursos_v2.py

    - name: Salvar alterações no estado (Persistência)
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        # Verifica se o arquivo existe antes de tentar adicionar
        if [ -f "concursos_data.json" ]; then
          git add concursos_data.json
          git commit -m "Atualizando estado do monitoramento [skip ci]" || echo "Sem alterações para salvar"
          git push
        else
          echo "Arquivo concursos_data.json não encontrado. O script rodou corretamente?"
        fi
