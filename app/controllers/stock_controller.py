from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database.models.user_model import User
from app import db

# stock controller blueprint to be registered with api blueprint
stock = Blueprint("stock", __name__)

stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB"]
showing_stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB"]
selected_stocks = []
graph_stocks = []

@stock.route('/dashboard' , methods=['POST', 'GET'])
def dashboard():
    global showing_stocks, selected_stocks, graph_stocks
    return render_template('home.html', all_stocks=stocks, filtered_stocks=showing_stocks, selected_stocks=selected_stocks, graph_stocks=graph_stocks)

@stock.route('/select_stock', methods=['POST'])
def select_stock():
    global showing_stocks, selected_stocks, graph_stocks
    selected_stock = request.form.get('selected_stock')
    if selected_stock and selected_stock not in selected_stocks:
        selected_stocks.append(selected_stock)
    if selected_stock in showing_stocks:
        showing_stocks.remove(selected_stock)
    return redirect(url_for('/.stock.dashboard'))


@stock.route('/remove_stock', methods=['POST'])
def remove_stock():
    print("here")
    global showing_stocks, selected_stocks, graph_stocks
    removed_stock = request.form.get('removed_stock')
    if removed_stock in selected_stocks:
        selected_stocks.remove(removed_stock)
    if removed_stock not in showing_stocks:
        showing_stocks.append(removed_stock)
    return redirect(url_for('/.stock.dashboard'))

@stock.route('/update_graph', methods=['POST'])
def update_graph():
    global graph_stocks, selected_stocks, showing_stocks
    print(selected_stocks)
    graph_stocks = selected_stocks.copy()
    # selected_stocks = []
    return redirect(url_for('/.stock.dashboard'))

@stock.route('/reset_filter', methods=['POST'])
def clear():
    global graph_stocks, selected_stocks, showing_stocks
    # graph_stocks = []
    selected_stocks = []
    showing_stocks = stocks.copy()
    return redirect(url_for('/.stock.dashboard'))

@stock.route('/show_all_stocks', methods=['POST'])
def show_all_stocks():
    global graph_stocks, selected_stocks, showing_stocks
    # graph_stocks = []
    showing_stocks = [stock for stock in stocks if stock not in selected_stocks]
    return redirect(url_for('/.stock.dashboard'))