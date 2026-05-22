"""
Tool: web_search
Uso en el bot: "busca: últimas noticias de IA"
Usa DuckDuckGo (sin API key).
"""
import urllib.request
import urllib.parse
import json

def search(query: str, max_results: int = 3) -> str:
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())

        results = []

        if data.get("AbstractText"):
            results.append(f"📌 {data['AbstractText'][:300]}")

        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"• {topic['Text'][:150]}")

        if not results:
            return f"No encontré resultados para: {query}"

        return f"🔍 Resultados para '{query}':\n\n" + "\n\n".join(results)
    except Exception as e:
        return f"Error al buscar: {e}"
