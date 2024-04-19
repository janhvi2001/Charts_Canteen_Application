from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # for data visualization
import io  # for image conversion
import base64  # for base64 encoding
import pickle
from sklearn.preprocessing import LabelEncoder
# Load the trained model
with open("demand_forecasting_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Function to generate charts based on user selection

# Function to generate charts based on user selection
def generate_charts(data, selected_feature):
    if selected_feature == "Total Item Price Distribution":
        plt.figure(figsize=(8, 5))
        sns.distplot(data["Total Item Price"], color='#fbaf32')
        plt.xlabel("Total Item Price")
        plt.ylabel("Density")
        plt.title("Distribution of Total Item Price")

    # Add more charts based on user selection (e.g., group by day of week, menu category)
    elif selected_feature == "Group by Menu Category":
        plt.figure(figsize=(8, 5))
        sns.barplot(x="Menu_Item", y="Total Item Price", data=data, color='#fbaf32')
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.xlabel("Menu Item")
        plt.ylabel("Total Item Price")
        plt.title("Total Item Price by Menu Category")
        plt.tight_layout()

    elif selected_feature == "Top Selling Items":
        plt.figure(figsize=(8, 5))
        top_selling_items = data.groupby("Menu_Item")["Total Item Price"].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=top_selling_items.index, y=top_selling_items.values,color='#fbaf32') 
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.xlabel("Menu_Item")
        plt.ylabel("Total Sales")     
        plt.title("Top 10 Selling Items")
        plt.tight_layout()

    elif selected_feature == "Sales by Day of Week":
        plt.figure(figsize=(8, 5))
        data["Day of Week"] = pd.to_datetime(data["date"]).dt.month
        data["Day of Week"]
        sns.countplot(x="Day of Week", data=data, color='#fbaf32')  # Count orders by day of week
        plt.xlabel("Day of Week")
        plt.ylabel("Order Count")
        plt.title("Sales by Day of Week")

    elif selected_feature == "Revenue by Category":
        # Group data by category, calculate total revenue
        revenue_by_category = (
            data.groupby("Category")["Total Item Price"].sum().reset_index(name="Total Revenue")
        )
        plt.figure(figsize=(8, 5))
        sns.barplot(x="Category", y="Total Revenue", data=revenue_by_category, color='#fbaf32')
        plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
        plt.xlabel("Menu Category")
        plt.ylabel("Total Revenue")
        plt.title("Revenue by Menu Category")   
    
    elif selected_feature == "Average Order Value by Day of Week":
        # Calculate average order value for each day of week
        data["Day of Week"] = pd.to_datetime(data["date"]).dt.dayofweek
        avg_order_value_by_day = (
            data.groupby("Day of Week")["Total Item Price"].mean().reset_index(name="Average Order Value")
        )
        plt.figure(figsize=(8, 5))
        plt.plot(avg_order_value_by_day["Day of Week"], avg_order_value_by_day["Average Order Value"], color='#fbaf32')
        plt.xlabel("Day of Week")
        plt.ylabel("Average Order Value")
        plt.title("Average Order Value by Day of Week")   

# Convert plot to PNG image and encode as base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_encoded = base64.b64encode(img_buffer.getvalue()).decode('ascii')

    # Clear the figure to avoid memory issues
    plt.clf()

    return img_encoded  # Return the base64 encoded image data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_feature = request.form["chart_options"]
        data = pd.read_csv("Canteen_App_Flask\canteen_data.csv")
        chart = generate_charts(data.copy(), selected_feature)
        return render_template("index.html", chart=chart)
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True)