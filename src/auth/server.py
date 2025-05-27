import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password from user WHERE email=%s", (auth.username)
    )

    if res:
        user_row = res.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return create_jwt(auth.username, os.environ.get("JWT_SECRET"), auth)
    else:
        return "Invalid credentials", 401
    
@server.route("/validate", method=["POST"])
def validate(request):
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing credentials", 401
    try:
        decoded_jwt = jwt.decode(jwt=encoded_jwt, key=os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except:
        return "Not authorized", 403
    return decoded_jwt
    
def create_jwt(username, secret, auth):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "auth": auth
        },
        secret,
        algorithm="HS256"
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)