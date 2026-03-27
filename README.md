# 🤖 Monitor de Ofertas do Telegram

Este projeto é um bot automatizado que monitora grupos e canais do Telegram em busca de palavras-chave específicas (como ofertas de hardware, passagens aéreas, etc.). Quando encontra uma correspondência, ele envia uma notificação imediata para o seu chat privado através de um bot do Telegram.

O script roda de forma 100% gratuita utilizando o **GitHub Actions**, verificando novas mensagens a cada 30 minutos.

---

## 📌 Como Funciona?
O projeto utiliza duas pontas:
1. **Userbot (Telethon):** Conecta-se à sua conta pessoal para "ler" as mensagens dos grupos onde você está.
2. **Bot Oficial (Telegram API):** Envia a notificação para você, garantindo que seu celular toque/vibre ao receber o alerta (evitando loops infinitos e bloqueios de spam).

---

## 🛠️ Pré-requisitos
Para configurar este bot do zero, você precisará de:
- Uma conta no [GitHub](https://github.com/).
- Python instalado no seu computador (apenas para a configuração inicial).
- Sua conta do Telegram logada no celular ou PC.

---

## 🚀 Passo a Passo da Configuração

### 1️⃣ Obter Credenciais da API (API ID e Hash)
Para que o script acesse o Telegram, você precisa criar um "Aplicativo" na sua conta:
1. Acesse [my.telegram.org](https://my.telegram.org) e faça login com seu número (formato internacional: `+55...`).
2. Vá em **API development tools**.
3. Crie uma nova aplicação (preencha apenas `App title` e `Short name` com nomes aleatórios).
4. Copie o **`App api_id`** (número) e o **`App api_hash`** (texto). Guarde-os.

### 2️⃣ Criar o Bot "Carteiro" (Bot Token)
Este é o bot que vai te mandar as mensagens de alerta.
1. No Telegram, pesquise por **@BotFather**.
2. Envie o comando `/newbot` e siga os passos para dar um nome e um `@username` ao bot.
3. Copie o **Token da API** que ele vai gerar (ex: `123456:ABC-DEF...`).
4. ⚠️ **MUITO IMPORTANTE:** Pesquise pelo `@username` do bot que você acabou de criar, abra a conversa e clique em **COMEÇAR** (ou envie `/start`). Se não fizer isso, ele não conseguirá te enviar mensagens!

### 3️⃣ Descobrir o seu Chat ID
O bot precisa saber para qual conta enviar os alertas.
1. No Telegram, pesquise por **@userinfobot**.
2. Inicie a conversa.
3. Ele vai responder com seus dados. Copie apenas os números da linha **`Id`** (ex: `123456789`).

### 4️⃣ Gerar a Chave de Sessão (No seu PC)
Como o GitHub é um servidor na nuvem, ele não pode receber o código de SMS do Telegram. Precisamos gerar uma chave de acesso permanente na sua máquina usando variáveis de ambiente para manter suas credenciais seguras.

1. No seu computador, abra o terminal e instale as bibliotecas necessárias: 
   `pip install telethon python-dotenv`
2. Na pasta do projeto, você verá um arquivo chamado `.env.example`. Faça uma cópia desse arquivo e renomeie a cópia para apenas `.env` (com o ponto no início e sem nenhuma extensão extra).
3. Abra o arquivo `.env` no seu editor de texto e coloque os seus dados reais:
   ```env
   TG_API_ID=12345678
   TG_API_HASH=sua_hash_gigante_aqui

### 5 Executar o Script e Gerar a Sessão (No seu PC)
Agora que o seu arquivo `.env` está preenchido, você precisa rodar o script no seu próprio computador apenas uma vez. Isso serve para fazer o login seguro e gerar a chave que o GitHub vai usar.

1. Abra o terminal (ou prompt de comando) na pasta onde estão os seus arquivos.
2. Execute o comando:
   ```bash
   python gerar_sessao.py

4. O terminal vai pedir o seu número de telefone. Digite no formato internacional (exemplo para o Brasil: +5511999998888) e dê Enter.

5. O Telegram enviará um código de login dentro do próprio aplicativo do Telegram (não é por SMS). Digite esse código no terminal.

6. Se der tudo certo, o terminal vai cuspir um código de texto gigante. Copie esse código e guarde-o num bloco de notas temporário.

    🔑 Essa é a sua TG_SESSION. É ela que permite que o bot na nuvem acesse sua conta sem precisar do seu celular.


5️⃣ Configurar o GitHub Actions (A Nuvem)

Com a sua TG_SESSION e as outras chaves em mãos, é hora de passar o trabalho para o GitHub. Ele vai rodar o bot por você 24 horas por dia, de graça.

Passo A: Criar o Repositório e Salvar as Senhas

1. Crie um novo repositório no GitHub. ⚠️ Atenção: Marque-o como Private (Privado) para ninguém roubar suas senhas!

2. No repositório, vá na aba Settings > Secrets and variables > Actions.

3. Clique no botão verde New repository secret. Você vai criar 5 "segredos", colando os valores que você reuniu até agora:

    TG_API_ID (Do Passo 1)

    TG_API_HASH (Do Passo 1)

    BOT_TOKEN (Do Passo 2)

    MEU_CHAT_ID (Do Passo 3)

    TG_SESSION (O código gigante do Passo 4)

Passo B: Subir o Código e Configurar a Automação

1. Faça o upload dos arquivos main.py e requirements.txt para o seu repositório. (Dica: nunca faça upload do arquivo .env para a internet).

2. Agora, precisamos criar o arquivo que diz ao GitHub para rodar o código a cada 30 minutos. No seu repositório, clique em Add file > Create new file.

3. No nome do arquivo, digite exatamente este caminho: .github/workflows/cron.yml

4. Cole o código YAML de agendamento (o fluxo de trabalho) dentro desse arquivo e clique em Commit changes para salvar.

6️⃣ Como Testar se Funcionou

1. Vá na aba Actions na parte superior do seu repositório.

2. Na lateral esquerda, clique no nome do seu fluxo de trabalho (ex: "Monitor de Ofertas 30min").

3. No lado direito, clique em Run workflow > Run workflow para forçar uma execução de teste manual.

4. Aguarde alguns segundos. Se a bolinha ficar verde (✅), verifique o seu Telegram: o bot deve ter mandado uma mensagem! A partir de agora, ele rodará sozinho a cada 30 minutos.


### 7️⃣ Como Configurar para um Produto Específico (Personalizando as Buscas)
O bot vem pré-configurado com alguns exemplos genéricos, mas você deve personalizá-lo para buscar exatamente os produtos, passagens ou itens que você deseja comprar.

Para alterar o que o bot procura, você só precisa editar uma única linha no arquivo principal do código:

1. Acesse o seu repositório no GitHub.
2. Clique no arquivo `main.py` (ou o nome que você deu ao arquivo principal do bot).
3. Clique no ícone de **Lápis (✏️)** no canto superior direito do arquivo para editá-lo.
4. Procure pela linha que começa com `TERMOS = [...]`. Ela fica logo no início do código.
5. Altere as palavras dentro dos colchetes para os produtos que você quer monitorar. 

**Regras importantes para os termos:**
- Escreva **sempre em letras minúsculas** (o script já converte todas as mensagens para minúsculo antes de procurar, para evitar que uma oferta escrita como "RTX" passe batido se você configurou "rtx").
- Coloque cada termo entre aspas simples e separe-os por vírgula.

**Exemplo Prático:**
Se você quer ser avisado apenas quando aparecerem ofertas de uma placa de vídeo RTX 4060, um iPhone 15 ou uma passagem para a Europa, deixe a linha assim:

```python
TERMOS = ['rtx 4060', 'iphone 15', 'europa']
```
Dica Extra (Filtrar Grupos):
Logo abaixo dos TERMOS, existe a variável CHATS_ALVO = [].

- Se você deixar vazia [], o bot vai ler todos os grupos e canais que você participa.

- Se você quiser que ele leia apenas grupos específicos de promoção (para evitar falsos positivos se um amigo falar "iphone 15" num grupo de bate-papo), coloque os IDs numéricos desses grupos dentro dos colchetes. Exemplo: CHATS_ALVO = [-100123456789, -100987654321].

- Após fazer suas alterações, clique no botão verde Commit changes no canto superior direito para salvar. O bot já começará a buscar as novas palavras na próxima rodada!