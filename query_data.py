import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an assistant with access to the Oregon Administrative Rules related to air quality, as administered by the Oregon Department of Environmental Quality (DEQ) Air Quality Division.
Use only the information from these rules to answer questions. Add more information from your knowledge base to enhance your answers. 

Context:
{context}

---

Answer the question based on the context above, ensuring that your response stays within the scope of Oregon air quality rules and regulations: {question}
"""

def main(query_text):
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return

    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Increase the number of chunks (k) to provide more context if needed
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if not results or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return

    # Construct context from retrieved chunks
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    
    # Output for debugging: print each chunk retrieved along with metadata
    print("Retrieved Chunks and Metadata:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\nChunk {i}:")
        print(f"Content:\n{doc.page_content}\nMetadata: {doc.metadata}\nRelevance Score: {score}\n{'-'*40}")

    # Update the prompt with context and question
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=300)
    response_text = model.invoke(prompt)  # Use `invoke` instead of `predict`

    # Collect metadata and present final response with sources and detailed chunks
    sources = [doc.metadata.get("source", "Unknown") for doc, _ in results]
    
    formatted_response = f"Response: {response_text}\n\nSources: {sources}\n\nContext Used:\n{context_text}"
    print(formatted_response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    main(args.query_text)
