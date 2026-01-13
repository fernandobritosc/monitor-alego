🤖 Bot de Monitoramento de Concursos (FGV & Verbena)

Este projeto é um bot automatizado desenvolvido em Python para monitorar atualizações em sites de concursos específicos (atualmente configurado para FGV - ALEGO 2025 e Instituto Verbena - Câmara de Goiânia). O bot detecta novos documentos, editais e convocações, enviando notificações em tempo real via Telegram.

🚀 Funcionalidades

•
Detecção Semântica: Diferente de bots que olham apenas o tamanho da página, este bot identifica novos links e títulos de documentos, evitando falsos positivos.

•
Notificações no Telegram: Receba o nome exato do novo documento publicado diretamente no seu celular.

•
Execução Automática: Configurado para rodar via GitHub Actions a cada 30 minutos, sem custo e sem necessidade de manter um computador ligado.

•
Persistência de Dados: Utiliza um arquivo JSON para lembrar o estado anterior e garantir que você só seja notificado sobre novidades reais.

🛠️ Tecnologias Utilizadas

•
Python 3.10+

•
BeautifulSoup4: Para raspagem de dados (web scraping).

•
Requests: Para requisições HTTP.

•
GitHub Actions: Para automação e agendamento das tarefas.

•
Telegram Bot API: Para o envio das notificações.

📋 Pré-requisitos

Antes de rodar o projeto, você precisará de:

1.
Um Token de Bot do Telegram (criado via @BotFather).

2.
O seu ID de Chat do Telegram (pode ser obtido via @userinfobot).

⚙️ Configuração no GitHub

Para que o bot funcione no seu repositório, siga estes passos:

1. Configurar Secrets

Vá em Settings > Secrets and variables > Actions e adicione:

•
TOKEN_TELEGRAM: O token do seu bot.

•
ID_TELEGRAM: O seu ID de usuário no Telegram.

2. Ativar Permissões de Escrita

Para que o bot salve o histórico de atualizações:

1.
Vá em Settings > Actions > General.

2.
Em Workflow permissions, selecione Read and write permissions.

3.
Clique em Save.

📂 Estrutura do Projeto

•
monitor_concursos_v2.py: Script principal em Python.

•
.github/workflows/monitor_workflow.yml: Configuração da automação.

•
concursos_data.json: Arquivo gerado automaticamente para controle de histórico.

📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar e adaptar para outros concursos!




Desenvolvido para automatizar a busca por aprovação! 🚀

