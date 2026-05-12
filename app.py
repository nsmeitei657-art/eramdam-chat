from flask import Flask, render_template_string, request, redirect, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = "eramdam_secret_key"

# ✅ IMPORTANT: threading mode (NO eventlet)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ---------------- LOGIN PAGE ----------------
login_html = """
<h2 style="text-align:center;">💚 Eramdam Login</h2>
<form method="POST" style="text-align:center;">
    <input name="username" placeholder="Enter Username" required>
    <br><br>
    <button type="submit">Login</button>
</form>
"""

# ---------------- CHAT PAGE ----------------
chat_html = """
<!DOCTYPE html>
<html>
<head>
<title>Eramdam Chat</title>
<style>
body {background:#0b141a; color:white; font-family:Arial;}
#chat {height:80vh; overflow-y:auto; padding:10px;}
.msg {padding:8px; margin:5px; background:#2a3942; border-radius:10px;}
input {width:80%; padding:10px;}
button {padding:10px; background:#00a884; color:white;}
</style>
</head>
<body>

<h3>💚 Eramdam Live Chat</h3>

<div id="chat"></div>

<input id="msg" placeholder="Type message...">
<button onclick="sendMsg()">Send</button>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
var socket = io();

socket.on("message", function(msg){
    var div = document.createElement("div");
    div.className = "msg";
    div.innerHTML = msg;
    document.getElementById("chat").appendChild(div);
});

function sendMsg(){
    var msg = document.getElementById("msg").value;
    socket.send("{{user}}: " + msg);
    document.getElementById("msg").value = "";
}
</script>

</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect("/chat")
    return login_html

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template_string(chat_html, user=session["user"])

# ---------------- SOCKET ----------------
@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
