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
    "question_English": "What impact has the Ayushman Bharat Yojana had on healthcare accessibility in Hazaribagh Lok Sabha?",
    "answer_English": "The Ayushman Bharat Yojana has significantly improved healthcare accessibility in Hazaribagh Lok Sabha by issuing over 10 lakh Ayushman cards. This ensures that no one in the region is deprived of medical treatment due to financial constraints.",
    "question_Hindi": "आयुष्मान भारत योजना ने हजारीबाग लोकसभा में स्वास्थ्य पहुँचनीयता पर कैसा प्रभाव डाला है?",
    "answer_Hindi": "आयुष्मान भारत योजना ने 10 लाख से अधिक आयुष्मान कार्ड जारी करके हजारीबाग लोकसभा में स्वास्थ्य पहुँचनीयता में काफी सुधार किया है। इससे यह सुनिश्चित होता है कि कोई भी क्षेत्र में वित्तीय परिस्थितियों के कारण चिकित्सा सेवाओं से वंचित नहीं है।"
}
,{
    "question_English": "What initiatives have been taken under the leadership of Prime Minister Narendra Modi for the welfare of the residents in Hazaribagh Lok Sabha?",
    "answer_English": "Under the leadership of Prime Minister Narendra Modi, significant efforts have been made to enhance the well-being of the residents in Hazaribagh Lok Sabha. The implementation of the Ayushman Bharat Yojana, with over 10 lakh Ayushman cards, is a testament to this commitment.",
    "question_Hindi": "प्रधानमंत्री नरेंद्र मोदी के नेतृत्व में हजारीबाग लोकसभा के निवासियों के कल्याण के लिए कौन-कौन सी पहलें की गईं हैं?",
    "answer_Hindi": "प्रधानमंत्री नरेंद्र मोदी के नेतृत्व में हजारीबाग लोकसभा के निवासियों के कल्याण को बढ़ावा देने के लिए कई महत्वपूर्ण पहलें की गईं हैं। 10 लाख से अधिक आयुष्मान कार्डों के पूर्णनिर्देश इस प्रतिबद्धता का प्रमाण है।"
}
,{
    "question_English": "How has the Ayushman Bharat Yojana addressed the financial constraints faced by the residents of Hazaribagh Lok Sabha?",
    "answer_English": "The Ayushman Bharat Yojana has been instrumental in addressing financial constraints for the residents of Hazaribagh Lok Sabha. With the issuance of over 10 lakh Ayushman cards, individuals no longer face obstacles in accessing medical treatment due to financial limitations.",
    "question_Hindi": "आयुष्मान भारत योजना ने हजारीबाग लोकसभा के निवासियों के सामग्री सीमाओं का सामना कैसे किया है?",
    "answer_Hindi": "आयुष्मान भारत योजना ने हजारीबाग लोकसभा के निवासियों के लिए वित्तीय सीमाओं का सामना करने में कैसे सहायक होती है, इसमें बड़ा योगदान है। 10 लाख से अधिक आयुष्मान कार्डों का जारी होना यह सुनिश्चित करता है कि वित्तीय सीमाओं के कारण किसी को भी चिकित्सा सेवाओं तक पहुँचने में कोई रुकावट नहीं होती।"
}
,{
    "question_English": "What role does Prime Minister Narendra Modi play in driving initiatives for healthcare improvements in Hazaribagh Lok Sabha?",
    "answer_English": "Prime Minister Narendra Modi plays a pivotal role in driving initiatives for healthcare improvements in Hazaribagh Lok Sabha. His leadership has been instrumental in the successful implementation of the Ayushman Bharat Yojana, benefitting over 10 lakh residents in the region.",
    "question_Hindi": "प्रधानमंत्री नरेंद्र मोदी जी हजारीबाग लोकसभा में स्वास्थ्य सुधार के लिए पहलों को कैसे प्रेरित करते हैं?",
    "answer_Hindi": "प्रधानमंत्री नरेंद्र मोदी जी हजारीबाग लोकसभा में स्वास्थ्य सुधार के लिए पहलों को प्रेरित करने में महत्वपूर्ण भूमिका निभाते हैं। उनके नेतृत्व में आयुष्मान भारत योजना के सफल प्रयासों से क्षेत्र में रहने वाले 10 लाख से अधिक निवासियों को लाभ हुआ है।"
},

  {
    "question_English": "What is the main objective of the continuous work being done to reach the multidimensional development and facilities to every needy person in the parliamentary constituency?",
    "answer_English": "The main objective is to provide facilities and ensure multidimensional development to every needy person in the parliamentary constituency.",
    "question_Hindi": "संसदीय क्षेत्र के बहुमुखी विकास और हर ज़रूरतमंद व्यक्ति तक सुविधा पहुंचाने के लिए निरंतर कार्यरत होने का मुख्य उद्देश्य क्या है?",
    "answer_Hindi": "मुख्य उद्देश्य है संसदीय क्षेत्र के हर ज़रूरतमंद व्यक्ति को सुविधाएँ प्रदान करना और बहुमुखी विकास सुनिश्चित करना।"
  },
  {
    "question_English": "What was the public's response to Prime Minister Narendra Modi's visit to Jharkhand?",
    "answer_English": "The public welcomed Prime Minister Narendra Modi's visit to Jharkhand enthusiastically.",
    "question_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन पर जनता का प्रतिसाद कैसा था?",
    "answer_Hindi": "जनता ने मा. प्रधानमंत्री नरेंद्र मोदी जी के झारखंड आगमन का उत्साहपूर्ण स्वागत किया।"
},{
    "question_English": "What impact has the Ujjwala Yojana, providing free gas connections and stoves, had on the lives of women in Hazaribagh Lok Sabha?",
    "answer_English": "The government, under the leadership of Prime Minister Narendra Modi, has provided free gas connections and stoves to more than 2,71,000 women in Hazaribagh Lok Sabha through the Ujjwala Yojana. This initiative has brought about a significant change in the lives of these women, granting them freedom from traditional cooking methods and saving them valuable time.",
    "question_Hindi": "हजारीबाग लोकसभा के महिलाओं के जीवन पर उज्ज्वला योजना का कैसा प्रभाव हुआ है, जिसने मुफ्त गैस कनेक्शन और चूल्हा प्रदान किया है?",
    "answer_Hindi": "मा. प्रधानमंत्री नरेंद्र मोदी जी के नेतृत्व में सरकार ने हजारीबाग लोकसभा में 2,71,000 से अधिक महिलाओं को उज्ज्वला योजना के माध्यम से मुफ्त गैस कनेक्शन और चूल्हा प्रदान किया है। इस पहल से महिलाओं के जीवन में महत्वपूर्ण परिवर्तन आया है, जिससे उन्हें पारंपरिक विधि से खाना बनाने की आजादी मिली है और उनके लिए समय की बचत हो रही है।"
},
{
    "question_English": "What did the discussion revolve around at the meeting with BJP Hazaribag and Ramgarh district presidents and MPs at Hazaribagh residence?",
    "answer_English": "The discussion at the meeting revolved around various important topics.",
    "question_Hindi": "हज़ारीबाग स्थित आवास पर BJP हज़ारीबाग व रामगढ़ ज़िला अध्यक्षों एवं सांसद प्रतिनिधियों के साथ विभिन्न महत्वपूर्ण विषयों पर चर्चा की गई थी, उसके बारे में क्या चर्चा हुई थी?",
    "answer_Hindi": "चर्चा में विभिन्न महत्वपूर्ण विषयों पर चर्चा हुई थी।"
},

]
# dataJson=pushDataToWeaviate(json_sets)
from fastapi import FastAPI
from searchData import searchData
app = FastAPI()

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

    print("search_result",search_result)
    return {"result": search_result}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)