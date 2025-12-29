# https://github.com/ollama/ollama
import requests
import json
import  gradio as gr

url="http://localhost:11434/api/generate"
headers={
    "Content-Type":"application/json"
}

history=[]
def generate_response(prompt):
    history.append(prompt)
    final_prompt="\n".join(history)
    # Build context from history
    context = "\n".join(history)


    data={
        "model": "codeguru",
        "prompt": final_prompt,
        "stream": False
    }

    response=requests.post(url,headers=headers,json=data)

    if response.status_code==200:
        response=response.text
        data=json.loads(response)
        actual_response=data["response"]
        # Add assistant response to history
        history.append(f"Assistant: {actual_response}")
        return actual_response
    else:
        error_msg = f"Error: {response.text}"
        print(error_msg)
        return error_msg

interface=gr.Interface(
    fn=generate_response,
    title="🤖 AI CodeGuru Chat",
    inputs=gr.Textbox(lines=4, placeholder="Enter your question"),
    outputs=gr.Textbox(lines=10, label="Response",  autoscroll=False)
)

interface.launch()

