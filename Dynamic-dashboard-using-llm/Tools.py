from typing_extensions import Annotated, TypedDict
from prompt import prompt_template
from getDB import getDBEngine
from llm import llm
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import json

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def generate_chart_ideas(table_info, business_info):
    try:
        response = llm.invoke(f"""
        You are an expert analyst. Your job is to create 3 different chart ideas from the given database information.
        
        You have given a business database and you will also be given some information about business and database. Based on that information you need to decide what type of database will be better for that business to show in dashboard.
                          
        You can generate charts from the following chart type list:
        - Bar chart
        - Line chart
        - Area chart
                          
        You have to generate a 20-25 words of a prompt to generate a specific chart which will be passed to the LLM model which will take your question and generate those charts. Make sure your prompt is easy to understand.

        Your final response MUST BE an array of objects where each object have the following fields:
        question: The prompt for LLM model to generate a relevant chart based on given business and database info 
        info: Tell what you are going to generate and why. (Your sentence should start like "A <chart_type> to show <what_you_are_showing> because it helps...")
        type: Chart type from the above 3 types
                          
        Here is how a sample question prompt looks like
        ---
        Generate a line chart to show the count of users with Basic plan based on their creation date
        ---
                          
        Here is the database information
        ---
        {table_info}
        ---

        Here is some information about business and database
        ---
        {business_info}
        ---

        NOTE: ONLY RESPOND WITH ARRAY OF OBJECTS WITHOUT MARKDOWN ELEMENTS AND MAKE SURE IT IS A VALID JSON
        """)
        
        # Extract the content from the response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Clean the response text to ensure it's valid JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            responseJson = json.loads(response_text)
            # Ensure we have at least 3 chart ideas
            while len(responseJson) < 3:
                responseJson.append({
                    "question": f"Generate a bar chart to show default data {len(responseJson) + 1}",
                    "info": f"A bar chart to show default data {len(responseJson) + 1} because it helps visualize basic information",
                    "type": "Bar chart"
                })
            return responseJson
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            # Return default chart ideas if parsing fails
            return [
                {
                    "question": "Generate a line chart to show monthly sales trends over time",
                    "info": "A line chart to show monthly sales trends because it helps visualize the growth pattern and identify seasonal trends",
                    "type": "Line chart"
                },
                {
                    "question": "Generate a bar chart to compare sales performance across different regions",
                    "info": "A bar chart to show regional sales comparison because it helps identify which regions are performing better",
                    "type": "Bar chart"
                },
                {
                    "question": "Generate an area chart to show product category revenue distribution",
                    "info": "An area chart to show product category revenue because it helps visualize the contribution of each category to total revenue",
                    "type": "Area chart"
                }
            ]
    except Exception as e:
        print(f"Error generating chart ideas: {e}")
        # Return default chart ideas if any error occurs
        return [
            {
                "question": "Generate a line chart to show monthly sales trends over time",
                "info": "A line chart to show monthly sales trends because it helps visualize the growth pattern and identify seasonal trends",
                "type": "Line chart"
            },
            {
                "question": "Generate a bar chart to compare sales performance across different regions",
                "info": "A bar chart to show regional sales comparison because it helps identify which regions are performing better",
                "type": "Bar chart"
            },
            {
                "question": "Generate an area chart to show product category revenue distribution",
                "info": "An area chart to show product category revenue because it helps visualize the contribution of each category to total revenue",
                "type": "Area chart"
            }
        ]

def write_query(question, database_url):
    """Generate SQL query to fetch information."""
    db = getDBEngine(database_url)
    table_info = db.get_table_info()
    
    response = llm.invoke(f"""
    You are an expert SQL developer. Your task is to generate a SQL query based on the given question and database schema.
    
    Database Schema:
    {table_info}
    
    Question:
    {question}
    
    Generate a valid SQL query that answers the question. The query should:
    1. Start with SELECT, INSERT, UPDATE, or DELETE
    2. Be syntactically correct and compatible with SQLite
    3. Include proper table joins if needed
    4. Include proper GROUP BY clauses if needed
    5. Include proper WHERE clauses if needed
    6. Return ONLY the SQL query without any additional text, markdown, or explanation
    
    Example of a valid response:
    SELECT products.category, sales.date, SUM(sales.quantity) 
    FROM sales 
    INNER JOIN products ON sales.product_id = products.id 
    GROUP BY products.category, sales.date
    """)
    
    # Extract the SQL query from the response
    query = response.content if hasattr(response, 'content') else str(response)
    query = query.strip()
    
    # Remove any markdown formatting if present
    if query.startswith('```sql'):
        query = query[6:]
    if query.endswith('```'):
        query = query[:-3]
    query = query.strip()
    
    # Validate the query starts with a valid SQL command
    valid_starts = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
    if not any(query.upper().startswith(cmd) for cmd in valid_starts):
        # If the query doesn't start with a valid command, try to fix it
        query_lines = query.split('\n')
        for i, line in enumerate(query_lines):
            if any(line.strip().upper().startswith(cmd) for cmd in valid_starts):
                query = '\n'.join(query_lines[i:])
                break
    
    return query

def execute_query(query, database_url):
    """Execute SQL query."""
    db = getDBEngine(database_url)
    execute_query_tool = QuerySQLDataBaseTool(db=db)
    return {"result": execute_query_tool.invoke(query)}

def generate_chart_data(database_response, question, database_query):
    try:
        response = llm.invoke(f"""
        You are an expert data analyst. Your job is to create a data for given chart type. You will be given a database data along with a query which was used to get that data. You will also be given the question which explains what user want to plot on a chart along with the chart type. You need to get the database response and format it in the way that it can be plot on chart.
                          
        You can generate charts from the following chart type list:
        - Bar chart
        - Line chart
        - Area chart
                          
        Your final response MUST BE an object which have the following fields:
        title: A short title for the chart
        columns: an array of string where each element shows the name of the column of a dataframe. If there is only a single line in a line chart or a single bar in bar chart then there will be only 1 element in this array. If there are multiple lines in a line chart or multiple areas in area chart then there will be more than 1 elements in this array and each element will be the name of that column.
        y_axis_values: A 2D array of elements which will contain the y-axis data for each column. Each nested array will contain the y-axis data for that column and must have same length as x_axis_values array.
        x_axis_values: A 1D array of elements which will contain the x-axis data for each columns.
        chart_type: The type of chart from the above type list (The text must be same as the text in type list)
        insights: Some insights about the data which you got which can summarize the chart data in 50-100 words with proper line breaks
                          
        For example, we have a line chart which shows count of users for each month then the data will look like this:
        ---
        title: Users in last year
        columns: ["Users"]
        y_axis_data: [[12,3,4,... and so on for all months]]
        x_axis_data: [Jan,feb,mar,... and so on]
        chart_type: Line chart
        insights: Chart summary here
        ---
                          
        Here is the database query
        ---
        {database_query}
        ---

        Here is the database response for the given query
        ---
        {database_response}
        ---

        Here is the chart for which you need to generate the data
        ---
        {question}
        ---

        Make sure that the length of each nested array in y_axis_values is same as the length of x_axis_values array otherwise the code will break. You can put 0 to fill any array in y_axis_values to make it same length.

        NOTE: ONLY RESPOND WITH OBJECT WITHOUT MARKDOWN ELEMENTS AND MAKE SURE IT IS A VALID JSON
        """)
        
        # Extract the content from the response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Clean the response text to ensure it's valid JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            responseJson = json.loads(response_text)
            
            # Ensure all required fields are present
            required_fields = ["title", "columns", "y_axis_values", "x_axis_values", "chart_type", "insights"]
            for field in required_fields:
                if field not in responseJson:
                    responseJson[field] = get_default_value(field)
            
            # Ensure x_axis_values is not empty
            if not responseJson["x_axis_values"]:
                responseJson["x_axis_values"] = ["Default"]
                responseJson["y_axis_values"] = [[0]]
            
            return responseJson
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            return get_default_chart_data()
    except Exception as e:
        print(f"Error generating chart data: {e}")
        return get_default_chart_data()

def get_default_value(field):
    defaults = {
        "title": "Default Chart",
        "columns": ["Data"],
        "y_axis_values": [[0]],
        "x_axis_values": ["Default"],
        "chart_type": "Bar chart",
        "insights": "Unable to generate chart data due to an error."
    }
    return defaults.get(field, "")

def get_default_chart_data():
    return {
        "title": "Default Chart",
        "columns": ["Data"],
        "y_axis_values": [[0]],
        "x_axis_values": ["Default"],
        "chart_type": "Bar chart",
        "insights": "Unable to generate chart data due to an error."
    }
