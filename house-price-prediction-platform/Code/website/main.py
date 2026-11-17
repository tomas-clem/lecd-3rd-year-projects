from flask import Flask, render_template,request,session,redirect,flash,jsonify,url_for
import db
import modelo
import email_functions as mail
from datetime import datetime
import plotly.express as px
import plotly
import json
import random
import uuid
import requests
import pandas as pd

app = Flask(__name__)

 
@app.route("/")
def index():
    if("id" in session):
        return redirect("/morada","302")
    return render_template("landing_page.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/search", methods=["GET"])
def search_page():
    if("id" in session):
        return session["id"]
    else:
        return redirect("/","302")
@app.route("/load_favorites",methods=["POST"])
def load_favorites():
    if("id" in session):
        content = request.json
        print(content)
        houses,lk = db.get_favorites(session["id"],content) if content != 0 else ([],0)
        return jsonify(houses=houses,lastKey=lk)
@app.route("/favoritos", methods=["GET"])
def favorites_page():
    if("id" in session):
        houses,lk = db.get_favorites(session["id"])
        return render_template("favorites.html",lastKey=lk,favorites=houses)
    else:
        return redirect("/","302")
    
@app.route("/favoritos/<house_id>")
def favorites_house(house_id):
    if("id" in session):
        favorites,lk = db.get_favorites(session["id"])
        house = db.get_house(house_id,session["id"])
        if "price_history" in house:
            price_values = [i[0] for i in house["price_history"]]
            price_timestamps = [datetime.fromtimestamp(float(i[1])) for i in house["price_history"]]

            print(price_values,price_timestamps)
            fig = px.line(y=price_values, x=price_timestamps)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
            fig.update_xaxes(color="white")
            fig.update_yaxes(color="white")
            fig.update_layout(
                title="Histórico de Preço do imovel",
                xaxis_title="Data",
                yaxis_title="Preço em €",
                font=dict(
                    color="white"
                )
            )
            graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
            return render_template("house.html",house=house,graphJSON=graphJSON,favorites=favorites)
        return render_template("house.html",house=house,favorites=favorites)

@app.route("/new-fav", methods=["GET"])
def new_favorite():
    if("id" in session):
        houses,lk = db.get_favorites(session["id"])
        if request.args.get("q"):
            morada = request.args.get("q")
            return render_template("imovel_form.html",action="/new-fav",title="Adicione um imovel como favorito",favorites=houses, morada=morada)
        else:
            return render_template("morada.html",title="Adicione um imovel como favorito",favorites=houses,action="/new-fav")
    else:
        return redirect("/","302")
        
@app.route("/new-fav", methods=["POST"])
def save_new_favorite():
    if("id" in session):
        house = modelo.form_to_house(request.form,session["id"])
        db.save_fav(house)
        return redirect("/favoritos","302")
    else:
        return redirect("/","302")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if(db.login(email,password)):
        if("remember-me" in request.form):
            session.permanent = True
        session["id"] = db.get_user_id(email)
        if "next_page" in session:
            np = session["next_page"]
            session.pop("next_page")
            return jsonify(message='success',next_page=np)
        return jsonify(message='success')
    return jsonify(message='error', error="Email ou palavra-passe incorretos")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("id")
    return redirect("/","302")

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["name"]
    if (not db.check_password(password)):
        return jsonify(message="error", error="A palavra-passe deve ter pelo menos:\n8 caracteres\nUma letra;\nUm digito;\nUm simbolo (@$!%*#?&).")
    if(db.register(email,password,name)):
        session["id"] = db.get_user_id(email)
        if "next_page" in session:
            np = session["next_page"]
            session.pop("next_page")
            return jsonify(message='success',next_page=np)
        return jsonify(message='success')
    return jsonify(message='error', error="A conta já existe, tente fazer login.")

@app.route("/reset",methods=["GET"])
def reset_page():
    token = request.args.get('token')
    if(token):
        if(db.check_recover_link(token,datetime.timestamp(datetime.now()))):
            return render_template("set_pswd.html")
    return render_template("change_pswd.html")

@app.route("/reset", methods=["POST"])
def reset():
    email = request.form["email"]
    user = db.get_user(email)
    if("Item" in user):
        token = db.create_recover_link(email)
        mail.recover_email(email,user["Item"]["username"],token)
        return jsonify(message='Email Enviado')
    return jsonify(message='error', error="Não existe conta associada ao email colocado.")

@app.route("/setpassword", methods=["POST"])
def change_password():
    new_password = request.form["password"]
    token = request.form["token"]
    if (not db.check_password(new_password)):
        return jsonify(message="error", error="A palavra-passe deve ter pelo menos:\nUma letra;\nUm digito;\nUm simbolo (@$!%*#?&).")
    email = db.check_recover_link(token,datetime.timestamp(datetime.now()))
    if(email):
        db.change_password(email,new_password)
        session["id"] = db.get_user_id(email)
        return jsonify(message='success')
    else:
        return jsonify(message='error', error="Link inválido.") 
    
@app.route("/prever", methods=["GET"])
def prever():
    if("id" in session):
        if "q" in session:
            morada = session["q"]
        else:
            morada = request.args.get("q")    
        houses,lk = db.get_favorites(session["id"])
        return render_template("imovel_form.html",action="/resultados",title="Prever o preço do imóvel",morada=morada, favorites=houses)
    else:
        if(request.args.get("q")):
            session["q"] = request.args.get("q")
            session["next_page"] = "/prever"
            return redirect("/login","302")
        return redirect("/","302")
@app.route("/avalia",methods=["GET"])
def avalia():
    if("id" in session):
        if(request.args.get("id")):
            house_id = request.args.get("id")
            house = db.get_house(house_id,session["id"])
            valor_previsto = modelo.get_price(house)
            preco = house["price"]
            intervalo = modelo.intervalo(valor_previsto)
            db.add_price_history(house_id,session["id"],valor_previsto)
            
            cor = modelo.cor(preco,intervalo)
            preco = str(preco) + " €"
            valor_previsto = str(intervalo) + " €"
            houses,lk = db.get_favorites(session["id"])
            return render_template("resultadosprev.html", valor_previsto=valor_previsto,cor=cor,valor_inserido = preco, favorites= houses)
        else:
            return redirect("/morada","302")
    else:
        return redirect("/","302")
@app.route("/resultados", methods=["POST"])
def resultados_modelo():
    if("id" in session):
        preco = request.form["q7"]
        house = modelo.form_to_house(request.form,session["id"])
        valor_previsto = modelo.get_price(house)
        intervalo = modelo.intervalo(valor_previsto)
        cor = modelo.cor(preco,intervalo)
        preco = str(preco) + " €"
        valor_previsto = str(intervalo) + " €"
        houses,lk = db.get_favorites(session["id"])
        return render_template("resultadosprev.html", valor_previsto=valor_previsto,cor=cor,valor_inserido = preco,favorites=houses)
    else:
        return redirect("/","302")

@app.route("/morada", methods=["GET"])
def morada():
    if("id" in session):
        houses,lk = db.get_favorites(session["id"])
        return render_template("morada.html",title="Prever o preço do imóvel",action="/prever",favorites=houses)
    else:
        return redirect("/","302")
@app.route("/delete", methods=["GET"])
def delete_fav():
    if("id" in session):
        if(request.args.get("id")):
            house_id = request.args.get("id")
            db.delete_fav(house_id,session["id"])
        return redirect("/favoritos","302")
    else:
        return redirect("/","302")
    
import pandas as pd

@app.route("/choropleth", methods=["GET"])
def choropleth():
    if("id" in session):
        repo_url = "https://gist.githubusercontent.com/NotBlankyu/884e17fddc9bc4d068139dc15321289b/raw/f4095818266617f5717a39b8016f9c8f2d4a2e30/portugal-districts2.geojson"
        jdata = requests.get(repo_url).json()

        thelist = jdata['features']
        locations =  [ item['properties']['NAME_1'] for item in thelist ] 
        #print('locations: ', locations)

        opcao = "abril"
        df = modelo.definirdfchoro(opcao)

        fig = px.choropleth(data_frame=df, 
                            geojson=jdata, 
                            locations='District', 
                            featureidkey='properties.NAME_1', 
                            color='Price',
                            center={"lat": 39.3999, "lon": -8.2245}, 
                            color_continuous_scale="RdYlGn",
                            scope="europe",
                            labels={'District': 'Distrito','Price': 'Preço Médio'})

        fig.update_geos(projection_type="mercator", 
                        coastlinecolor="white", 
                        landcolor="white",  
                        oceancolor="white",  
                        lakecolor="white",  
                        rivercolor="white",  
                        framecolor="white",  
                        framewidth=2,  
                        projection_scale=7, 
                        center_lon=-19, 
                        center_lat=37.5,  
                        countrycolor="white"
                        )

        fig.update_geos(
            lonaxis_range=[-150, 70], 
            lataxis_range=[-70, 20],  
        )

        fig.update_layout(
            autosize=False,
            width=400,
            height=400,
        )      
                                
        df2 = modelo.definirdtend(opcao="Lisboa")
        graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

        fig2 = px.line(df2, x='Month', y='Price', title='Tendência de preços', markers=True)

        fig2.update_layout(xaxis_title='Mês', yaxis_title='Preço', xaxis=dict(tickangle=45), yaxis=dict(gridcolor='lightgray'))

        fig2.update_layout(
            autosize=False,
            width=400,
            height=270,
        ) 

        graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("chropleth.html",title="Investir onde e/ou tipo",graphJSON=graphJSON,graphJSON2=graphJSON2)
    else:
        return redirect("/","302")

if __name__ == "__main__":
    app.secret_key = "pecd_2023"
    app.run(host='0.0.0.0')