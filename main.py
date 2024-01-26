from Website import create_app

app = create_app()

if __name__ == "__main__":
    app.config["SECRET_KEY"] = "kjgbrekj;rbv;uiber;kberb"
    app.run(debug=True)