from flask import *
import datetime



web_app= Flask("DOCTORs APP")

@web_app.route("/")


def index() :
    message = """<html>
    <head>
        <title>DOCTORs APP</title>
    </head>
    <body>
        <center>
            <h3>Welcome to DOCTORs APP</h3>
        </center>
    </body>
</html>"""
    return render_template("index.html")


@web_app.route("/register")
def register():
    return render_template("register.html")
def main():
        web_app.run()


if __name__=="__main__":
        main()