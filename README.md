# iot-gb

Projeto aplicado desenvolvido na disciplina de Internet das Coisas (IoT) - Unisinos

Conteúdo do projeto:
- **docs/**: arquivos do projeto (source da POC da ESP32, projeto do simulador Wokwi, relatório técnico produzido)
- **processor/**: serviço consumidor MQTT de processamento de dados e armazenamento em banco
- **simulator/**: serviço produtor MQTT e simulador do dispositivo de monitoramento
- **docker-compose**: orquestração dos serviços em containers
- **Makefile**: comandos do projeto

---

### Rodando o projeto

1. Execute o comando `all` para subir a infraestrutura, configurar o banco de dados e inicializar os serviços
2. Execute o comando `logs` para observar os logs do `processor`

```bash
$ make all
$ make logs
```


### Visualizando o broker MQTT

1. Navegue até http://www.hivemq.com/demos/websocket-client/
2. Clique em "Connect"
3. Clique em "Add New Topic Subscription"
4. No campo de Tópico, digite "iot/monitor" e clique "Subscribe"


### Visualizando os dados no Grafana

1. Navegue http://localhost:3000
2. Acesse com usuário e senha: ("admin", "admin")
3. Clique em "Data Sources" e "Add new data source"
4. Selecione MySQL e conecte com URL, Database, Username e Password: ("mysql:3306", "iot_sensor_data", "iot_gb", "password")
5. Navegue até "Dashboard"
6. Crie um novo painel do timpo "Time Series" para o conjunto de dados adicionado
7. Selectione a tabela `motion` e as colunas `timestamp` e `motion_detected`


### Rodando o simulador

1. Configure os parâmetros da simulação em `./simulator/config.json`
2. Execute o simulador

```bash
$ make run-simulator
```
