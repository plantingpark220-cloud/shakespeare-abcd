"""產生單字與金句的 mp3 (audio/)。免費、免 API key，需要網路。
安裝: pip install edge-tts      執行: python gen_audio.py
聲音可改 VOICE（例如 en-GB-SoniaNeural 女聲）。"""
import asyncio, json, os, edge_tts
VOICE = "en-GB-RyanNeural"
src = open('data.js', encoding='utf8').read()
WORDS = json.loads(src[src.index('['):src.rindex(']') + 1])
async def main():
    os.makedirs('audio', exist_ok=True)
    for e in WORDS:
        base = f"audio/{e['l'].lower()}_{e['s']}"
        jobs = ((base + '_word.mp3', e['s'], '-20%'), (base + '_quote.mp3', e['q'].replace(' / ', ', '), '-10%'))
        for path, text, rate in jobs:
            await edge_tts.Communicate(text, VOICE, rate=rate).save(path); print(path)
asyncio.run(main())
