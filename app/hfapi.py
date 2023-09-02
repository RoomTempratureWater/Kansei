import requests
import os
from dotenv import load_dotenv
load_dotenv()

#print(os.environ.get('HF'))
qAPI_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-question-generation-ap"
sAPI_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING_SUMMARY"
headers = {"Authorization": f"Bearer {os.environ.get('HF')}"}

def questions(payload):
	s = "context: {}".format(payload)
	#print(s)
	q = {
	    "inputs": s,
        }
	response = requests.post(qAPI_URL, headers=headers, json=q)
	res = response.json()
	return str(res[0]["generated_text"][10:])

def summarys(payload):
    q = {
	    "inputs": payload,
        }
    response = requests.post(sAPI_URL, headers=headers, json=q)
    return str(response.json()[0]['summary_text'])
      
if __name__ == "__main__":
    output = questions("The heap is one maximally efficient implementation of an abstract data type called a priority queue, and in fact, priority queues are often referred to as 'heaps', regardless of how they may be implemented. In a heap, the highest (or lowest) priority element is always stored at the root. However, a heap is not a sorted structure; it can be regarded as being partially ordered. A heap is a useful data structure when it is necessary to repeatedly remove the object with the highest (or lowest) priority, or when insertions need to be interspersed with removals of the root node.")


    print(output)