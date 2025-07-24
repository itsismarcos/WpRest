# WordPress 4.7.x REST API Exploit (CVE-2017-1001000)

🚨 Ferramenta de exploração automática para WordPress 4.7.0 e 4.7.1 baseada na vulnerabilidade de injeção de conteúdo via REST API.  
📌 Desenvolvido por **Marcos R**, para fins **educacionais e autorizados**.

---

## 💥 Sobre a vulnerabilidade

Em versões 4.7.0 e 4.7.1 do WordPress, a API REST permitia modificar posts sem autenticação.  
Mais detalhes: [Sucuri Blog](https://blog.sucuri.net/2017/02/content-injection-vulnerability-wordpress-rest-api.html)

---

## ✨ Funcionalidades

- [x] Scan automático de vulnerabilidade
- [x] Autoexploração (injeta mensagem no primeiro post)
- [x] Suporte a URL única ou lista em `.txt`
- [x] Banner estilizado e mensagens coloridas
- [x] Resumo de ataques bem-sucedidos

---

## 📦 Requisitos

- Python 3.6+
- Bibliotecas:

```bash
pip install lxml colorama
