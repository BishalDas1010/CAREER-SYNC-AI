from textLoader.ResumeLoader import ResumeLoader
from textLoader.docs_loader import docs_loader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main():
    #resume Loader
    embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cuda'}  # change to 'cuda' if available
        )

    text_spliter =RecursiveCharacterTextSplitter(
        chunk_size =200,
        chunk_overlap = 100
    )
    pdf = "Bishaldas_cv_.pdf"
    resume_loader = ResumeLoader(pdf,embedding_model)
    docs = resume_loader.pdf_loader()
    #spliter 

    spliter = resume_loader.text_splitter(docs,text_spliter)
    vactor_store =resume_loader.vector_store(spliter,embedding_model)
    resume_loader.retriever("skills and expreince",vactor_store)

    #job describtion Loader
    ppath = "job_des.txt"
    docoment_loader =docs_loader(ppath,embedding_model)
    docs1 = docoment_loader.pdf_loader()
    #spliter 

    spliter1 = docoment_loader.text_splitter(docs1,text_spliter)
    vactor_store1 =docoment_loader.vector_store(spliter1,embedding_model)
    docoment_loader.retriever("skills and expreince",vactor_store1)


main()