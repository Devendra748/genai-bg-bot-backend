from textToVactor import convertTextToVectors
from dataToWeaviate import pushDataToWeaviate

json_sets = [
    {
        "question_English": "How was the reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand?",
        "answer_English": "The reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand was grand.",
        "question_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा कैसा भव्य स्वागत किया गया?",
        "answer_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा भव्य स्वागत किया गया था।"
    },
    {
        "question_English": "How was the reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand?",
        "answer_English": "The reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand was grand.",
        "question_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा कैसा भव्य स्वागत किया गया?",
        "answer_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा भव्य स्वागत किया गया था।"
    },
        {
        "question_English": "How was the reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand?",
        "answer_English": "The reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand was grand.",
        "question_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा कैसा भव्य स्वागत किया गया?",
        "answer_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा भव्य स्वागत किया गया था।"
    },
        {
        "question_English": "How was the reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand?",
        "answer_English": "The reception of the Honorable Prime Minister Narendra Modi on his arrival in Jharkhand was grand.",
        "question_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा कैसा भव्य स्वागत किया गया?",
        "answer_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता द्वारा भव्य स्वागत किया गया था।"
    }


]
dataJson=pushDataToWeaviate(json_sets)
