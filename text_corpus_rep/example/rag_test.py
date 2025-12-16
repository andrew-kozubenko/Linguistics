from rag.ontology_loader import load_ontology
from rag.index_ontology import build_ontology_index
from rag.rag_pipeline import rag_answer

print("1) Загружаем онтологию")
nodes, edges = load_ontology("graph.json")

print(f"2) Узлов: {len(nodes)}, связей: {len(edges)}")

print("3) Строим индекс (эмбеддинги)")
index = build_ontology_index(nodes, edges)

print("4) Индекс готов")

# question = "Какие игровые механики характерны для игры Dark Souls?"
question = "Какие персонажи есть в игре the elder scrolls v: skyrim?"
# question = "Какие в играх предметы и особенно расходники?"

print("5) Запускаем RAG")
answer = rag_answer(question, index)

print("6) Ответ получен:")
print(answer)
