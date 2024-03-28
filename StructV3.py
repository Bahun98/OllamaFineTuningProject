import requests
import json
import pandas as pd

class dataExtraction:
    def __init__(self, job_description, payload, response, inside):
        self.job_description = job_description
        self.payload = payload
        self.response = response
        self.insideResponse = inside



class main:
    schema = {
        "company": {
            "type": "string",
            "description": "What company offers the job?"
        },
        "Job title": {
            "type": "string",
            "description": "What Job title of the position?"
        },
        "Language of job posting": {
            "type": "string",
            "description": "What is the language of the job offer?"
        },
        "description": {
            "type": "string",
            "description": "A short description of the job offer"
        },
        "responsibilities": {
            "type": "string",
            "description": "The tasks and responsibilities applicants would need to perform in the job"
        },
        "requirements": {
            "type": "string",
            "description": "The skills, knowledge and other requirements the job has"
        },
        "Educational level": {
            "type": "string",
            "description": "What is the minimum level of education required for the job? Choose one of the following: [MBO, HBO, WO, Master, PHD]. In case it is not exactly written write: not specified"
        },
        "Field of ICT" : {
            "type": "string",
            "description": "What Field of ICT does this job belong to? Choose one from: [software engineering, infrastructure, business, media design, embedded systems, not IT related]"
        },
        "GenerativeAI": {
            "type": "string",
            "description": "Is it related to generativeAI? Yes or No"
        },
        "NLP": {
            "type": "string",
            "description": "Is it related to NLPs? Yes or No"
        },
        "Machine Learning": {
            "type": "string",
            "description": "Is it related to Machine learning? Yes or No"
        }
    }

    def payloadGen(jobPosting, schema):
            keyList = list(schema.keys())
            payload = {
            "model": "llama2",
            "resetContext": True,  # Add this parameter to reset the conversation context
            "messages": [
                {"role": "system", "content": f"""You are a helpful AI assistant, an expert at extracting data from job descriptions. 
                For the given job posting, you will analyze the job posting either in English or Dutch and return the following details:
                company that offered the job, 
                the description, 
                What is the language used most to define the job offer? 
                responsibilities that come with the job, 
                All of the soft and hard skills, background, expereience, knowledge requirements you need to apply for the job,
                what is the MINIMUM level of education required for the job? Choose one of the following: [MBO, HBO, WO, Master, PHD]. In case it is not exactly written write: not specified,
                What field of ICT does this job belong to? Choose one from: [software engineering, infrastructure, business, media design, embedded systems, not IT related]?
                Is the job related to GenerativeAI? Yes or no,
                Is the job to natural language processing? Yes or no, 
                Is the job to machine learning? Yes or no, 
                The response should be in the original language of the job posting and be as detailed as possible.
                Output in JSON using the schema defined here: {schema}. The keys of the json that you return should be literally be the follwoing: 
                company, Job title, Language of job posting, description, responsabilities, requirements, Educational level, Field of ICT, GenerativeAI, NLP, Machine Learning."""},
                
                {"role": "user", "content": f"""Analyse the {jobPosting}. Only answer the following: {keyList}. The output of your query should be a json format, the keys in the json
                 should strictly be equal to litearlly the following elements of the list: company, Job title, Language of job posting, description, responsabilities, requirements, Educational level, Field of ICT, GenerativeAI, NLP, Machine Learning. 
                 In case there is not infomation in the job posting to answer the keys provided leave the value associated with the key blank"""}
            ],
            "options": {
                 "temperature": 0.0
            },
            "format": "json"
            }
            return payload
    
    def responseGet(payload):
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        #print(payload)
        return response

    file_path = 'test.xlsx'
    df = pd.read_excel(file_path)

    job_responses = []

    for index, row in df.iterrows():
        job_description = row['Origin']
        payload = payloadGen(job_description,schema)
        response = responseGet(payload)

        inside = ""
        for message in response.iter_lines():
            jsonstr = json.loads(message, strict=False)
            inside += jsonstr["message"]["content"]
        job_responses.append(dataExtraction(job_description,payload,response,inside))
        

    
    # Create an empty DataFrame with columns as keys
    new_df = pd.DataFrame(columns=schema.keys())

    
    for job_response in job_responses:
        data = json.loads(job_response.insideResponse, strict=False)
        # Append the data as a new row to the new DataFrame
        new_df = new_df._append(data, ignore_index=True)

    new_df.to_excel("structured_output_of_StructV3.xlsx", index=False)
    


        

        


    

    

  

