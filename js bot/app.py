from textToVactor import convertTextToVectors
from dataToWeaviate import pushDataToWeaviate

json_sets = [
  {
    "question_English": "What steps are being taken to upgrade Anganwadi centers in Hazaribagh Lok Sabha?",
    "answer_English": "In Hazaribagh Lok Sabha, 2800 Anganwadi centers are being upgraded as Model Anganwadi Centers for the convenience of the people. Additionally, Jal Jeevan Mission is facilitating the construction of water towers.",
    "question_Hindi": "हजारीबाग लोकसभा में आंगनबाड़ी केंद्रों को अपग्रेड करने के लिए कौन-कौन से कदम उठाए जा रहे हैं?",
    "answer_Hindi": "हजारीबाग लोकसभा में लोगों की सुविधा के लिए 2800 आंगनबाड़ी केंद्रों को मॉडल आंगनबाड़ी केंद्रों के रूप में अपग्रेड किया जा रहा है। साथ ही, जल जीवन मिशन के तहत जलमीनार का निर्माण किया जा रहा है।"
  },
  {
    "question_English": "What initiatives has the Modi government taken to provide people with secure housing, electricity, and bank accounts?",
    "answer_English": "The Modi government has undertaken significant initiatives to provide people with secure housing, electricity, and bank accounts over the last 10 years. People have been facilitated with pucca houses, electricity, and bank accounts.",
    "question_Hindi": "मोदी सरकार ने लोगों को सुरक्षित आवास, बिजली, और बैंक खाता प्रदान करने के लिए कौन-कौन सी पहलुओं को अपनाया है?",
    "answer_Hindi": "मोदी सरकार ने पिछले 10 वर्षों में लोगों को सुरक्षित आवास, बिजली, और बैंक खाता प्रदान करने के लिए महत्वपूर्ण पहलुओं को अपनाया है। लोगों को पक्का घर, बिजली, और बैंक खाता प्रदान किया गया है।"
  }
]

from fastapi import FastAPI
from searchData import searchData
app = FastAPI()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(question1, question2):
    vectorizer = CountVectorizer().fit_transform([question1, question2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors[0].reshape(1, -1), vectors[1].reshape(1, -1))
    return similarity[0, 0]
@app.post("/push_data_to_weaviate")
def push_data_to_weaviate():
    # Call your pushDataToWeaviate function with the JSON data
    data_json = pushDataToWeaviate(json_sets)

    return {"message": data_json}
@app.post("/search_data")

def search_data(question: str, number: int):
    print(question)
    # Call your searchData function with the provided question and number
    search_result = searchData(question, number)

    return search_result
def calculate_cosine_similarity(vector1, vector2):
    # Assuming vector1 and vector2 are lists of floats
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = sum(a**2 for a in vector1) ** 0.5
    magnitude2 = sum(a**2 for a in vector2) ** 0.5
    similarity = dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 != 0 else 0.0
    percentage_similarity = round(similarity * 100, 2)
    return percentage_similarity

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)