from langchain_community.document_loaders import WebBaseLoader

url = "https://www.linkedin.com/jobs/search/?currentJobId=4411411471&f_C=1073%2C1068&geoId=102713980&keywords=jpmorgan&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&spellCorrectionEnabled=true"

loader = WebBaseLoader(url)
docs = loader.load()

print(docs[0].page_content)