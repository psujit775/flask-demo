from flask import Flask, request
import os
import openai
import sys

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')  # this is the home page route
def hello_world(
):  # this is the home page function that generates the page code
    return "Hello world!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        fulfillmentText = 'you said'
        query_result = req.get('queryResult')
        query = query_result.get('queryText')

        start_sequence = "\nJOY->"
        restart_sequence = "\nUser->"

        if query_result.get('action') == 'input.unknown':

            response = await openai.Completion.create(
                model="davinci:ft-personal-2023-04-04-17-05-17",
                prompt="The following is a conversation with an AI assistant that can have meaningful conversations with users. The assistant is helpful, pediatric specialist, and friendly. Its objective is to parents with their new borns. With each response, the AI assisstant prompts the user to continue the conversation in a natural way. sonpari is empathic and friendly. sonpari's objective is to help parents with their new born childers, sonpari offers follow-up questions to encourage openness and tries to continue the conversation in a natural way. \n\nSonpari-> Hello, I am your personal pediatrician assistant. How can i help you today?\nUser->"+query+"Sonpari->",
                temperature=0.89,
                max_tokens=162,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n"]
            )

        result = response.get('choices')[0].get('text')

        return {
            "fulfillmentText":
            result,
            "source":
            "webhookdata"
        }
        return '200'
    except Exception as e:
        print('error',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('oops',exc_type, fname, exc_tb.tb_lineno)
        return '400'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
