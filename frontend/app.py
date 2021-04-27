from flask import Flask,render_template,request
app = Flask(__name__) 



@app.route("/")
def index():
     return render_template("index.html") 
     
@app.route("/get")
def get_bot_response():
     userText = request.args.get("msg") 
     return str("ga tau, coba tanya mang ucup?")

if __name__ == "__main__":
     app.run(debug = True)


