from Website import create_app

app = create_app()

if __name__ == "__main__":
    app.config["SECRET_KEY"] = "kjgbrekj;rbv;uiber;kberb"
    app.run(host="10.1.5.231", port="5555", debug=True)