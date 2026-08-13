import pypandoc

content = """ML / AI / RAG INTERVIEW QUESTION SET

1. PYTHON
1. What is the difference between a list, tuple, set, and dictionary?
2. What are decorators in Python?
3. What is list comprehension?
4. What is the difference between is and ==?
5. How does exception handling work?
6. What are generators?
7. What is shallow copy vs deep copy?

2. MACHINE LEARNING
8. What is supervised vs unsupervised learning?
9. What is overfitting and how do you prevent it?
10. Explain the bias-variance tradeoff.
11. What is feature engineering?
12. What is cross-validation?
13. Explain precision, recall, and F1-score.
14. Decision Tree vs Random Forest?
15. Why would you use XGBoost?

3. DEEP LEARNING
16. What is a neural network?
17. What is an activation function?
18. ReLU vs Sigmoid vs Softmax?
19. What is backpropagation?
20. What is gradient descent?
21. What is dropout?
22. CNN vs RNN vs Transformer?

4. LLM / GENERATIVE AI
23. What is an LLM?
24. What is tokenization?
25. What are embeddings?
26. What is a vector database?
27. What is RAG?
28. Why use RAG instead of fine-tuning?
29. What is hallucination in LLMs?
30. What is prompt engineering?
31. What is context window?
32. What is temperature in an LLM?

5. RAG
33. Explain the complete RAG pipeline.
34. Why do we chunk documents?
35. What are chunk size and chunk overlap?
36. What happens if chunks are too large?
37. What happens if chunks are too small?
38. What is semantic search?
39. What is hybrid search?
40. ChromaDB vs FAISS?
41. What is an embedding model?
42. Why use all-MiniLM-L6-v2?
43. How do you evaluate a RAG system?
44. How would you reduce irrelevant retrieval?
45. How would you handle a 500-page PDF?

6. LANGCHAIN / LANGGRAPH
46. What is LangChain?
47. What is a retriever?
48. What is a vector store?
49. What is a document loader?
50. What is LangGraph?
51. LangChain vs LangGraph?
52. Why would you use multiple agents?
53. How would you design a career-assistant agent?

7. BACKEND / FASTAPI
54. What is an API?
55. What is a REST API?
56. Why use FastAPI?
57. What is JWT authentication?
58. JWT vs session-based authentication?
59. How would you connect FastAPI with PostgreSQL?
60. How would you deploy your RAG application?

8. PROJECT-BASED QUESTIONS
61. Explain your Career-Sync AI project.
62. Why did you choose RAG?
63. What problem does Career-Sync AI solve?
64. Explain your architecture.
65. What happens when a user uploads a resume?
66. How do you extract information from the resume?
67. How do you identify skill gaps?
68. How do you generate career recommendations?
69. What challenges did you face?
70. How would you scale the system to 1,000+ users?

IMPORTANT QUESTIONS TO PREPARE FIRST

27. What is RAG?
28. Why use RAG instead of fine-tuning?
33. Explain the complete RAG pipeline.
34. Why do we chunk documents?
35. What are chunk size and chunk overlap?
38. What is semantic search?
39. What is hybrid search?
40. ChromaDB vs FAISS?
42. Why use all-MiniLM-L6-v2?
43. How do you evaluate a RAG system?
61. Explain your Career-Sync AI project.
62. Why did you choose RAG?
63. What problem does Career-Sync AI solve?
64. Explain your architecture.
65. What happens when a user uploads a resume?
69. What challenges did you face?
70. How would you scale the system to 1,000+ users?
"""

output = "ML_AI_RAG_Interview_Question_Set.txt"
pypandoc.convert_text(content, "plain", format="md", outputfile=output, extra_args=["--standalone"])
print(output)
