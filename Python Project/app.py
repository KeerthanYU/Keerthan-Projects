from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CALCULATOR</title>
<style>
body {
    font-family: Arial;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #1E1E1E;
    margin: 0;
}
.calculator {
    background: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px #000;
    width: 100%;
    max-width: 360px;
}
input {
    width: 100%;
    height: 50px;
    font-size: 28px;
    margin-bottom: 10px;
    text-align: right;
    border-radius: 10px;
    border: none;
    padding: 5px;
}
.row {
    display: flex;
    justify-content: space-between;
}
button {
    flex: 1;
    margin: 5px;
    height: 60px;
    font-size: 22px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    color: white;
    transition: all 0.1s ease-in-out;
}
button.number { background-color: #31363D; }
button.number:hover { background-color: #3d4249; }
button.number:active { background-color: #1f2225; transform: scale(0.95); }

button.operator { background-color: #50555B; }
button.operator:hover { background-color: #63686f; }
button.operator:active { background-color: #3d4147; transform: scale(0.95); }

button.clear { background-color: #F84C08; }
button.clear:hover { background-color: #ff5c1a; }
button.clear:active { background-color: #c93800; transform: scale(0.95); }

button.equal { background-color: #21AC4F; flex: 3; }
button.equal:hover { background-color: #2bd25d; }
button.equal:active { background-color: #1b7f34; transform: scale(0.95); }

@media (max-width: 400px) {
    input { font-size: 24px; height: 45px; }
    button { font-size: 20px; height: 50px; }
}
</style>
</head>
<body>
<div class="calculator">
<form method="POST" id="calcForm">
<input type="text" id="expression" name="expression" value="{{ expression }}" readonly><br>

{% for row in buttons %}
<div class="row">
{% for button in row %}
{% set cls = '' %}
{% if button in ['0','1','2','3','4','5','6','7','8','9','.'] %} {% set cls='number' %} {% endif %}
{% if button in ['+','-','*','/'] %} {% set cls='operator' %} {% endif %}
{% if button=='C' %} {% set cls='clear' %} {% endif %}
{% if button=='=' %} {% set cls='equal' %} {% endif %}
<button type="submit" name="btn" value="{{ button }}" class="{{ cls }}">{{ button }}</button>
{% endfor %}
</div>
{% endfor %}
</form>
</div>

<script>
// Keyboard support
document.addEventListener('keydown', function(event) {
    let keys = "0123456789+-*/.";
    let input = document.getElementById("expression");
    if(keys.includes(event.key)) input.value += event.key;
    else if(event.key === "Enter") document.querySelector("button[value='=']").click();
    else if(event.key === "Backspace") input.value = input.value.slice(0,-1);
    else if(event.key.toLowerCase() === "c") input.value = "";
});
</script>
</body>
</html>
"""

# Buttons layout
buttons = [
    ['7','8','9','C'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','/','+'],
    ['=']
]

@app.route("/", methods=["GET","POST"])
def calculator():
    expression = ""
    if request.method == "POST":
        expression = request.form.get("expression", "")
        btn = request.form.get("btn")
        if btn == "C":
            expression = ""
        elif btn == "=":
            try:
                expression = str(eval(expression))
            except:
                expression = "Error"
        else:
            expression += btn
    return render_template_string(HTML, expression=expression, buttons=buttons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
