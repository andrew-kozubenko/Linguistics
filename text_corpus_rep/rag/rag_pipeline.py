from .search import search
from .llm import ask_llm


def rag_answer(question: str, index, n=5, m=3):
    # Фаза 2
    first = search(question, index, top_k=n)
    texts_n = [item[1]["text"] for item in first]

    print("→ LLM: первый ответ")
    draft_answer = ask_llm(question, texts_n)
    print("✓ Первый ответ получен")

    summary = draft_answer.split("\n")[0][:200]

    # Фаза 3
    second = search(summary, index, top_k=m)
    texts_m = [item[1]["text"] for item in second]

    all_texts = {t for t in texts_n + texts_m}

    print("→ LLM: финальный ответ")
    final_answer = ask_llm(question, list(all_texts))
    print("✓ Финальный ответ получен")

    return final_answer
