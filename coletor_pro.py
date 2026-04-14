import asyncio
from playwright.async_api import async_playwright
import psycopg2
from datetime import datetime
import random
from database import get_connection # ADICIONE NO TOPO

conn = get_connection() # USE ASSIM

async def coletar_dados_humanos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # User-agent mais recente para parecer um Chrome atualizado
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("🔍 Iniciando Versão B (Otimizada) - Pet Shops Castanhal")
        busca = "pet+shop+em+castanhal+para"
        await page.goto(f"https://www.google.com/maps/search/{busca}")
        await page.wait_for_timeout(5000)

        links_vistos = set() # Memória para não repetir cliques
        lista_seletor = 'div[role="feed"]'
        
        conn = get_connection()
        cur = conn.cursor()

        # Aumentamos o número de rolagens, mas com passos menores
        for i in range(30):
            # Captura todos os links visíveis na tela no momento
            links_na_tela = await page.locator('a.hfpxzc').all()
            
            for link_el in links_na_tela:
                href = await link_el.get_attribute('href')
                
                # FILTRO: Só entra se nunca viu esse link antes
                if href and href not in links_vistos:
                    links_vistos.add(href)
                    
                    try:
                        # Move o mouse até o item antes de clicar (comportamento humano)
                        await link_el.hover()
                        await link_el.click()
                        
                        # Espera um tempo humano para a ficha carregar
                        await page.wait_for_timeout(random.randint(3500, 5500))

                        # Validação: Se o título não apareceu, espera mais um pouco
                        titulo_el = page.locator('h1.DUwDvf').first
                        await titulo_el.wait_for(state="visible", timeout=5000)
                        
                        nome = await titulo_el.inner_text()
                        
                        # Coleta de categoria
                        try:
                            cat = await page.locator('button[jsaction*="category"]').first.inner_text()
                        except: cat = "Pet Shop"

                        # Coleta de nota
                        try:
                            nota_raw = await page.locator('div.F7nice span[aria-hidden="true"]').first.inner_text()
                            nota = float(nota_raw.replace(',', '.'))
                        except: nota = None

                        # Coleta de Reivindicação
                        reivindicado = True
                        if await page.get_by_text("Reivindicar esta empresa").is_visible(timeout=1000):
                            reivindicado = False

                        # Coleta de Telefone (Foco em precisão)
                        telefone = "Não encontrado"
                        tel_seletor = page.locator('button[data-tooltip*="telefone"], button[jsaction*="phone.copy"]').first
                        if await tel_seletor.is_visible(timeout=1000):
                            telefone = await tel_seletor.inner_text()

                        print(f"✅ [{len(links_vistos)}] Novo: {nome} | Tel: {telefone}")

                        cur.execute("""
                            INSERT INTO auditoria_seo (nome_empresa, categoria, nota_google, reivindicado, telefone, data_analise)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (nome_empresa) DO UPDATE SET 
                                nota_google = EXCLUDED.nota_google,
                                reivindicado = EXCLUDED.reivindicado,
                                telefone = EXCLUDED.telefone,
                                data_analise = EXCLUDED.data_analise;
                        """, (nome, cat, nota, reivindicado, telefone, datetime.now()))
                        conn.commit()

                    except Exception as e:
                        continue

            # Scroll humano: distâncias variadas
            distancia = random.randint(800, 1600)
            await page.evaluate(f"document.querySelector('{lista_seletor}').scrollBy(0, {distancia})")
            await page.wait_for_timeout(random.randint(2000, 4000))
            print(f"--- Rolagem {i+1} concluída ---")

        cur.close()
        conn.close()
        await browser.close()
        print(f"🚀 Fim da Versão B. Total de links únicos processados: {len(links_vistos)}")

if __name__ == "__main__":
    asyncio.run(coletar_dados_humanos())