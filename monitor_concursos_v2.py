name: Monitor de Concursos

on:
  schedule:
    # Roda a cada 30 minutos (ajuste conforme necessário)
    - cron: '*/30 * * * *'
  workflow_dispatch: # Permite rodar manualmente pelo painel do GitHub

jobs:
  build:
    runs-on: ubuntu-latest

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
      run: python monitor_concursos_v2.py

    - name: Salvar alterações no estado (Persistência)
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add concursos_data.json
        git commit -m "Atualizando estado do monitoramento [skip ci]" || echo "Sem alterações para salvar"
        git push
