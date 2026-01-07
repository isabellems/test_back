# Technical Test Outline

---

## Introduction

The purpose of this technical test is to evaluate a candidate's practical software engineering skills in a controlled environment. This test focuses on real-world problem-solving and includes an introduction, a hands-on coding session, and a follow-up discussion to explore the candidate’s approach and understanding.

### Test Duration:
- **Introduction**: 5 minutes to cover test setup and objectives
- **Coding Task**: 2 hours of hands-on engineering work

---

## The Case

### Explanation of the Exercise
Candidates are tasked with building a small backend application that can handle basic RESTful API requests. The candidates are required to make their backend interact with an LLM (large language model) endpoint hosted on Azure (details are in the technical tips section) to fulfill specific application functionalities.

**Objective**: To create a functional backend that can process data from an Azure-hosted LLM and deliver structured responses.

---

## Tips

To encourage a comprehensive approach, candidates should keep the following in mind:

- **API Design**: Think about creating a simple, clear API interface for future frontend integration.
- **Scalability**: Consider how the backend could handle increased demand or future feature expansion.
- **Error Handling and Security**: Implement robust error handling and basic security best practices.
- **Tool usage**: Use all tools at your disposal. We want to evaluate your ability to develop, similar to a day-to-day in the office so make smart use of Google and ChatGPT. 

---

## Technical Details

- Candidates will interact with an LLM (large language model) endpoint hosted on Azure to provide specific functionalities within the application. This interaction should be evident in both the backend and frontend implementations. You are allowed to connect to the models that are already pre-setup or create a new open ai deployment in your own resourcegroup.
- Pre-setup GPT-4o-mini: https://open-ai-resource-rob.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview
- Pre-setup Text-embedding: https://open-ai-resource-rob.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15
- Pre-setup The API key can be found in the Key Vault storage secrets in the azure account that was setup. Keyvault name: open-ai-keys-rob, secret name: open-ai-resource-rob
- The code can be deployed to an assigned azure resource group with your name in it. If your resource group is missing or not working well feel free to use the backup resourcegroup
- Azure account: email:Robapplicant@outlook.com, pwd: TechnicalTester!. You might have to 2 factor authenticate. This is most easily one through the browser and you can ask Paul Miles for the code that was sent to his email. 
- Please make sure to upload your code to this github repository that's shared with you. It's called {your-name-TT}.
- Since everyone takes different approaches you could be blocked by permissions that aren't covered yet for the account. If that happens let us know as soon as possible and we'll give you access to the resource if the request is valid

---

## Evaluation

### Expectations of the Demo

Candidates are expected to demonstrate a basic but functional backend application that reflects their technical abilities and understanding of modern application structures. In the demo you'll have time to explain your chain of thoughts behind the decisions you've taken during the development process. Also, you can elaborate on the setbacks, future improvements, architecture etc. 

### Evaluation Attributes
Candidates will be evaluated based on:

- **Creativity**: Innovative approaches or features implemented in the backend.
- **Capability to Learn**: Adaptation and utilization of both new and familiar technologies.
- **Code Quality**: Readability, structure, and adherence to coding best practices.

---

## Key Steps in Development

1. **Backend Creation**: A working backend that can handle RESTful API requests.
2. **LLM Integration**: Successfully integrate the backend with the Azure-hosted LLM.

---

## Getting started

- Make sure to check out your resources in azure with the account provided in the technical details
- Start with a very basic poc before adding creative extra's

