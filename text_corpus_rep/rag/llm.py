from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

_llm = None

def get_llm(model_name="distilbert/distilgpt2"):
    global _llm
    if _llm is None:
        print(f"[LLM] Загружаем модель: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        _llm = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1  # CPU
        )
    return _llm

def ask_llm(question: str, texts: list) -> str:
    texts_short = [t[:500] for t in texts]

    llm = get_llm()
    tokenizer = llm.tokenizer

    prompt = (
        "Ты — помощник для ответов на вопросы по тексту. "
        "Ответ должен базироваться только на предоставленной информации.\n\n"
        f"Вопрос: {question}\n\n"
        "Текст:\n" + "\n\n".join(texts_short) + "\n\n"
    )

    prompt = truncate_prompt_to_tokens(
        prompt,
        tokenizer,
        max_tokens=900  # запас под генерацию
    )

    llm = get_llm()
    out = llm(
        prompt,
        max_new_tokens=100,
        temperature=0.2,
        do_sample=True,
        repetition_penalty=1.1
    )

    # получаем часть с ответом
    return out[0]["generated_text"]

def truncate_prompt_to_tokens(prompt, tokenizer, max_tokens=900):
    tokens = tokenizer.encode(prompt, add_special_tokens=False)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return tokenizer.decode(tokens)
