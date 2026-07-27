# Etapa 5 — Capacitação em Linux

## Objetivo

Desenvolver conhecimentos fundamentais em Linux, promovendo um nivelamento conceitual sobre o sistema operacional, sua estrutura, o uso do terminal e os principais comandos utilizados em ambientes tecnológicos e de Engenharia de Dados.

---

## Tarefa 1 — Introdução ao Linux

### O que é Linux

Linux é um sistema operacional de código aberto amplamente utilizado em servidores, ambientes de desenvolvimento, plataformas de nuvem, processamento de dados e infraestrutura.

O termo Linux também é utilizado para representar sistemas operacionais construídos a partir do kernel Linux.

### Distribuições Linux

Uma distribuição Linux é uma versão do sistema operacional formada pelo kernel Linux, ferramentas administrativas, gerenciadores de pacotes, interfaces e aplicações.

Exemplos de distribuições:

- Ubuntu
- Debian
- Fedora
- Red Hat Enterprise Linux
- Rocky Linux
- Linux Mint
- Arch Linux

### Kernel Linux

O kernel é o componente central do sistema operacional. Ele atua como uma camada de comunicação entre os programas e os recursos físicos da máquina.

Entre suas principais responsabilidades estão:

- Gerenciamento de memória
- Gerenciamento de processos
- Controle de dispositivos
- Gerenciamento do sistema de arquivos
- Controle de acesso aos recursos da máquina

### Vantagens do Linux

- Código aberto
- Grande variedade de distribuições
- Estabilidade em ambientes de servidores
- Possibilidade de automação por comandos e scripts
- Ampla utilização em ambientes de nuvem
- Compatibilidade com ferramentas de Engenharia de Dados
- Grande comunidade e disponibilidade de documentação

---

## Tarefa 2 — Ambiente de estudo

### Utilização de máquina virtual

Durante o curso, o ambiente Linux foi configurado em uma máquina virtual.

Essa abordagem permite executar outro sistema operacional dentro da máquina principal sem substituir o sistema já instalado.

Foram apresentadas as seguintes ferramentas:

- Oracle VirtualBox
- VMware

### Ubuntu

O Ubuntu foi utilizado como distribuição Linux de referência durante as atividades práticas.

Ele é baseado no Debian e possui ampla utilização em ambientes de desenvolvimento, servidores e computação em nuvem.

A instalação da máquina virtual foi utilizada como recurso de aprendizagem e familiarização com o ambiente Linux, sem aprofundamento em conceitos de virtualização ou administração de servidores.

---

## Tarefa 3 — Terminal e Shell

### Terminal

O terminal é uma interface que permite interagir com o sistema operacional por meio de comandos de texto.

### Shell

O shell é o programa responsável por interpretar os comandos digitados no terminal e solicitar sua execução ao sistema operacional.

Um dos shells mais utilizados no Linux é o Bash.

### Verificar o shell utilizado

```bash
echo $SHELL
```

### Consultar o usuário atual

```bash
whoami
```

### Verificar o diretório atual

```bash
pwd
```

---

## Tarefa 4 — Estrutura de diretórios

O Linux organiza seus arquivos em uma estrutura hierárquica.

O ponto inicial dessa estrutura é representado pelo diretório raiz:

```bash
/
```

### Diretórios importantes

- `/home`: diretórios pessoais dos usuários
- `/etc`: arquivos de configuração do sistema
- `/var`: arquivos variáveis, como logs
- `/tmp`: arquivos temporários
- `/usr`: aplicações, bibliotecas e arquivos compartilhados
- `/bin`: comandos essenciais do sistema
- `/opt`: aplicações adicionais

### Diretório pessoal

O símbolo abaixo representa o diretório pessoal do usuário:

```bash
~
```

---

## Tarefa 5 — Navegação no sistema

### Comando `pwd`

Exibe o caminho completo do diretório atual.

```bash
pwd
```

### Comando `cd`

Permite navegar entre os diretórios do sistema.

#### Acessar um diretório

```bash
cd documentos
```

#### Acessar um caminho absoluto

```bash
cd /home/usuario/documentos
```

#### Voltar ao diretório anterior

```bash
cd ..
```

#### Retornar ao diretório pessoal

```bash
cd ~
```

#### Retornar ao último diretório acessado

```bash
cd -
```

### Comando `ls`

Lista os arquivos e diretórios existentes em determinado local.

#### Listagem simples

```bash
ls
```

#### Listagem detalhada

```bash
ls -l
```

#### Exibir arquivos ocultos

```bash
ls -a
```

#### Listagem detalhada com arquivos ocultos

```bash
ls -la
```

#### Exibir tamanhos em formato legível

```bash
ls -lh
```

### Comando `clear`

Limpa o conteúdo visual do terminal.

```bash
clear
```

---

## Tarefa 6 — Visualização e criação de arquivos

### Comando `cat`

Exibe o conteúdo de um arquivo diretamente no terminal.

```bash
cat arquivo.txt
```

#### Exibir mais de um arquivo

```bash
cat arquivo1.txt arquivo2.txt
```

#### Unir conteúdos em um novo arquivo

```bash
cat arquivo1.txt arquivo2.txt > arquivo_completo.txt
```

### Comando `touch`

Cria um arquivo vazio ou atualiza a data de modificação de um arquivo existente.

```bash
touch arquivo.txt
```

#### Criar vários arquivos

```bash
touch arquivo1.txt arquivo2.txt arquivo3.txt
```

### Comando `man`

Exibe o manual de utilização de determinado comando.

```bash
man ls
```

```bash
man grep
```

### Ajuda rápida de comandos

Alguns comandos oferecem uma opção resumida de ajuda.

```bash
ls --help
```

---

## Tarefa 7 — Gerenciamento de arquivos e diretórios

### Comando `mkdir`

Cria um novo diretório.

```bash
mkdir projeto
```

#### Criar múltiplos diretórios

```bash
mkdir entrada processamento saida
```

#### Criar uma estrutura de diretórios

```bash
mkdir -p projeto/dados/raw
```

### Comando `rmdir`

Remove um diretório vazio.

```bash
rmdir diretorio_vazio
```

### Comando `rm`

Remove arquivos.

```bash
rm arquivo.txt
```

#### Solicitar confirmação antes da remoção

```bash
rm -i arquivo.txt
```

#### Remover um diretório e seu conteúdo

```bash
rm -r diretorio
```

O comando `rm` deve ser utilizado com cuidado, principalmente quando acompanhado de opções recursivas ou forçadas, pois os arquivos removidos pelo terminal normalmente não são enviados para a lixeira.

### Comando `cp`

Copia arquivos e diretórios.

#### Copiar um arquivo

```bash
cp origem.txt destino.txt
```

#### Copiar um arquivo para outro diretório

```bash
cp arquivo.txt /home/usuario/documentos
```

#### Copiar um diretório

```bash
cp -r diretorio_origem diretorio_destino
```

### Comando `mv`

Move arquivos e diretórios. Também pode ser utilizado para renomeá-los.

#### Mover um arquivo

```bash
mv arquivo.txt documentos/
```

#### Renomear um arquivo

```bash
mv arquivo_antigo.txt arquivo_novo.txt
```

#### Renomear um diretório

```bash
mv projeto_antigo projeto_novo
```

---

## Tarefa 8 — Gerenciamento de pacotes

### Gerenciador APT

O APT é uma ferramenta utilizada em distribuições baseadas no Debian, como o Ubuntu, para instalar, atualizar, pesquisar e remover pacotes.

### Atualizar a lista de pacotes

```bash
sudo apt update
```

### Atualizar os pacotes instalados

```bash
sudo apt upgrade
```

### Instalar um pacote

```bash
sudo apt install nome-do-pacote
```

Exemplo:

```bash
sudo apt install git
```

### Pesquisar um pacote

```bash
apt search nome-do-pacote
```

### Exibir informações sobre um pacote

```bash
apt show nome-do-pacote
```

### Remover um pacote

```bash
sudo apt remove nome-do-pacote
```

### Remover pacote e arquivos de configuração

```bash
sudo apt purge nome-do-pacote
```

### Remover dependências não utilizadas

```bash
sudo apt autoremove
```

O comando `sudo` permite executar uma ação com privilégios administrativos. Seu uso deve ser realizado apenas quando necessário e com atenção ao comando executado.

---

## Tarefa 9 — Filtros e busca de conteúdo

### Comando `head`

Exibe as primeiras linhas de um arquivo.

```bash
head arquivo.txt
```

#### Definir a quantidade de linhas

```bash
head -n 5 arquivo.txt
```

### Comando `tail`

Exibe as últimas linhas de um arquivo.

```bash
tail arquivo.txt
```

#### Definir a quantidade de linhas

```bash
tail -n 20 arquivo.txt
```

#### Acompanhar atualizações de um arquivo

```bash
tail -f aplicacao.log
```

### Comando `grep`

Pesquisa textos ou padrões dentro de arquivos e resultados de outros comandos.

#### Pesquisar uma palavra

```bash
grep "erro" aplicacao.log
```

#### Ignorar diferença entre letras maiúsculas e minúsculas

```bash
grep -i "erro" aplicacao.log
```

#### Exibir o número das linhas

```bash
grep -n "erro" aplicacao.log
```

#### Pesquisar recursivamente em diretórios

```bash
grep -r "cliente_id" projeto/
```

#### Combinar com outro comando

```bash
ls -la | grep ".txt"
```

### Comando `find`

Localiza arquivos e diretórios a partir de diferentes critérios.

#### Buscar um arquivo pelo nome

```bash
find . -name "dados.csv"
```

#### Buscar arquivos por extensão

```bash
find . -name "*.csv"
```

#### Buscar apenas diretórios

```bash
find . -type d -name "dados"
```

#### Buscar apenas arquivos

```bash
find . -type f -name "*.log"
```

### Comando `locate`

Pesquisa arquivos utilizando uma base de dados previamente indexada pelo sistema.

```bash
locate arquivo.txt
```

#### Atualizar a base de pesquisa

```bash
sudo updatedb
```

---

## Tarefa 10 — Histórico e localização de comandos

### Histórico de comandos

O terminal mantém um histórico dos comandos executados pelo usuário.

```bash
history
```

### Executar novamente o último comando

```bash
!!
```

### Pesquisar comandos anteriores

O atalho abaixo permite pesquisar comandos digitados anteriormente:

```text
Ctrl + R
```

### Localizar o executável de um comando

```bash
which python
```

```bash
which git
```

### Identificar como um comando é interpretado

```bash
type cd
```

```bash
type ls
```

---

## Tarefa 11 — Editores de texto

### Nano

Nano é um editor de texto executado diretamente no terminal, com uma interface simples e comandos indicados na parte inferior da tela.

#### Abrir ou criar um arquivo

```bash
nano arquivo.txt
```

#### Atalhos básicos

- `Ctrl + O`: salvar o arquivo
- `Ctrl + X`: sair do editor
- `Ctrl + W`: pesquisar conteúdo
- `Ctrl + K`: recortar uma linha
- `Ctrl + U`: colar conteúdo

### Vim

Vim é um editor de texto baseado em modos de operação.

Os modos mais importantes apresentados durante o curso foram:

- Modo normal
- Modo de inserção
- Modo de comando

#### Abrir ou criar um arquivo

```bash
vim arquivo.txt
```

#### Entrar no modo de inserção

```text
i
```

#### Retornar ao modo normal

```text
Esc
```

#### Salvar o arquivo

```vim
:w
```

#### Salvar e sair

```vim
:wq
```

#### Sair sem salvar

```vim
:q!
```

#### Excluir uma linha

```text
dd
```

#### Desfazer uma alteração

```text
u
```

#### Refazer uma alteração

```text
Ctrl + R
```

#### Pesquisar um texto

```vim
/texto
```

#### Substituir ocorrências

```vim
:%s/texto_antigo/texto_novo/g
```

---

## Tarefa 12 — Permissões no Linux

### Conceitos fundamentais

As permissões definem quais usuários podem ler, modificar ou executar arquivos e diretórios.

As permissões básicas são:

- `r`: leitura
- `w`: escrita
- `x`: execução

Elas são organizadas para três categorias:

- Usuário proprietário
- Grupo proprietário
- Outros usuários

### Visualizar permissões

```bash
ls -l
```

Exemplo de resultado:

```text
-rwxr-xr-- 1 usuario grupo 1024 jul 20 10:00 script.sh
```

### Representação numérica

- `4`: leitura
- `2`: escrita
- `1`: execução

Os valores podem ser somados para formar uma combinação de permissões.

- `7`: leitura, escrita e execução
- `6`: leitura e escrita
- `5`: leitura e execução
- `4`: somente leitura

### Alterar permissões numericamente

```bash
chmod 755 script.sh
```

```bash
chmod 644 arquivo.txt
```

### Alterar permissões simbolicamente

#### Adicionar permissão de execução ao proprietário

```bash
chmod u+x script.sh
```

#### Remover permissão de escrita do grupo

```bash
chmod g-w arquivo.txt
```

#### Adicionar leitura para outros usuários

```bash
chmod o+r arquivo.txt
```

### Alterar proprietário

```bash
sudo chown novo_usuario arquivo.txt
```

### Alterar proprietário e grupo

```bash
sudo chown novo_usuario:novo_grupo arquivo.txt
```

### Alterar apenas o grupo

```bash
sudo chgrp novo_grupo arquivo.txt
```

---

## Tarefa 13 — Gerenciamento de usuários e grupos

### Usuários

Usuários representam identidades que podem acessar e utilizar os recursos do sistema.

#### Adicionar um usuário

```bash
sudo adduser novo_usuario
```

#### Excluir um usuário

```bash
sudo deluser nome_usuario
```

#### Excluir um usuário e seu diretório pessoal

```bash
sudo deluser --remove-home nome_usuario
```

#### Alterar senha

```bash
sudo passwd nome_usuario
```

#### Bloquear um usuário

```bash
sudo usermod -L nome_usuario
```

#### Desbloquear um usuário

```bash
sudo usermod -U nome_usuario
```

#### Alterar o nome de usuário

```bash
sudo usermod -l novo_nome nome_atual
```

#### Alterar o diretório pessoal

```bash
sudo usermod -d /home/novo_nome -m novo_nome
```

### Grupos

Grupos permitem organizar usuários e compartilhar permissões de acesso a arquivos e recursos.

#### Criar um grupo

```bash
sudo groupadd engenharia_dados
```

#### Excluir um grupo

```bash
sudo groupdel engenharia_dados
```

#### Adicionar um usuário a um grupo

```bash
sudo usermod -aG engenharia_dados nome_usuario
```

#### Visualizar os grupos de um usuário

```bash
groups nome_usuario
```

### Superusuário

O usuário `root` possui privilégios administrativos sobre o sistema.

Em distribuições como Ubuntu, ações administrativas geralmente são executadas utilizando o comando `sudo`.

#### Abrir um shell como usuário root

```bash
sudo -i
```

#### Retornar ao usuário anterior

```bash
exit
```

---

## Tarefa 14 — Registro e documentação dos aprendizados

### Principais aprendizados

Ao longo da capacitação, foi possível desenvolver uma base introdutória sobre:

- Conceitos fundamentais do sistema operacional Linux
- Diferença entre kernel e distribuição Linux
- Utilização do Ubuntu em uma máquina virtual
- Conceitos de terminal e shell
- Estrutura hierárquica de diretórios
- Navegação entre arquivos e diretórios
- Criação, cópia, movimentação e remoção de arquivos
- Consulta de manuais e ajuda de comandos
- Instalação e gerenciamento básico de pacotes com APT
- Visualização e pesquisa de conteúdo em arquivos
- Utilização básica dos editores Nano e Vim
- Conceitos fundamentais de permissões
- Representação numérica e simbólica de permissões
- Conceitos básicos de usuários, grupos e proprietários
- Importância do Linux em ambientes tecnológicos e de dados

---

## Aplicação no contexto de Engenharia de Dados

### Contexto

O Linux é amplamente utilizado como sistema operacional base em servidores, plataformas de processamento distribuído, ambientes de nuvem, containers e ferramentas relacionadas à Engenharia de Dados.

A capacitação não teve como objetivo formar conhecimentos avançados de administração de sistemas. Seu principal propósito foi estabelecer um nivelamento e uma base conceitual para facilitar o contato com ambientes e tecnologias que utilizam Linux.

### Possíveis pontos de aplicação

- **Execução de comandos em ambientes de dados:** compreender comandos básicos utilizados em terminais de máquinas virtuais, servidores e plataformas de dados.

- **Navegação em projetos:** localizar diretórios, arquivos de configuração, scripts, logs e arquivos de dados.

- **Consulta de logs:** utilizar comandos como `cat`, `head`, `tail` e `grep` para visualizar informações de execução.

- **Organização de arquivos:** criar, copiar, mover e renomear arquivos utilizados em pipelines e projetos.

- **Gerenciamento de dependências:** compreender como aplicações e ferramentas podem ser instaladas por meio de gerenciadores de pacotes.

- **Edição de configurações:** realizar alterações simples em arquivos utilizando editores executados no terminal.

- **Compreensão de permissões:** interpretar restrições de leitura, escrita e execução encontradas em scripts e arquivos de projetos.

- **Preparação para outras tecnologias:** construir uma base para estudos de Docker, Spark, Kubernetes, ferramentas de nuvem e plataformas executadas sobre Linux.

---

## Resultado obtido

- Maior familiaridade com o ambiente Linux
- Conhecimento introdutório sobre terminal e shell
- Compreensão da estrutura de arquivos e diretórios do sistema
- Conhecimento dos principais comandos apresentados no curso
- Nivelamento sobre gerenciamento de pacotes, permissões, usuários e grupos
- Melhor compreensão da presença do Linux em ambientes de Engenharia de Dados
- Construção de uma base conceitual para aprofundamentos futuros

---

## Conclusão

A capacitação proporcionou um nivelamento sobre os principais conceitos e comandos do Linux.

Os conteúdos estudados contribuíram para uma melhor compreensão da estrutura do sistema operacional, da utilização do terminal e das operações básicas realizadas por comandos.

O conhecimento adquirido representa uma base introdutória para o contato com ferramentas e ambientes utilizados em Engenharia de Dados, sem substituir capacitações específicas de administração de sistemas ou infraestrutura.

```

```
