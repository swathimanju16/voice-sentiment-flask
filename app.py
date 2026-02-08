from flask import Flask, render_template_string, request
from textblob import TextBlob

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Voice Sentiment Analyzer</title>
</head>
<body>
<h2>Voice Sentiment Analyzer</h2>

<button onclick="start()">Record Voice</button>

<form method="post">
<input type="hidden" id="text" name="text">
<br><br>
<input type="submit" value="Analyze">
</form>

<p id="output"></p>

{% if sentiment %}
<h3>Sentiment: {{ sentiment }}</h3>
{% endif %}

<script>
function start(){
 const rec = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
 rec.lang='en-US';
 rec.start();
 rec.onresult=function(e){
   document.getElementById("output").innerHTML=e.results[0][0].transcript;
   document.getElementById("text").value=e.results[0][0].transcript;
 }
}
</script>

</body>
</html>
"""

@app.route("/",methods=["GET","POST"])
def home():
    sentiment=None
    if request.method=="POST":
        text=request.form["text"]
        blob=TextBlob(text)
        p=blob.sentiment.polarity
        if p>0: sentiment="Positive"
        elif p<0: sentiment="Negative"
        else: sentiment="Neutral"
    return render_template_string(HTML,sentiment=sentiment)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)