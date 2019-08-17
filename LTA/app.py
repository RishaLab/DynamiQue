from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import requests
from bs4 import BeautifulSoup
import json
import lda  #lda module for ease of usage
import webbrowser
#Database connection from here
import sqlite3
##############################




app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
	return render_template('home.html')



@app.route('/predict',methods=['POST'])
def predict():
	# df= pd.read_csv("spam.csv", encoding="latin-1")
	# df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
	# # Features and Labels
	# df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	# X = df['message']
	# y = df['label']
	
	# # Extract Feature With CountVectorizer
	# cv = CountVectorizer()
	# X = cv.fit_transform(X) # Fit the Data

	
	if request.method == 'POST':
		message = request.form['message']

		connection = sqlite3.connect('data.db')

		cursor = connection.cursor()

		s_q = "SELECT * FROM t_messages WHERE m_name='"+message+"'"
		data = []
		words = []
		for row in cursor.execute(s_q):
			data.append(row[2])
			words.append(row[3])
			print(data)
		
		# word = words[0]
		word = lda.f_lda(data)
		# We have used the lda module to get the topic word
		

		res = requests.get("https://stackoverflow.com/search?q="+word)

		soup = BeautifulSoup(res.text, "html.parser")

		questions_data = {
			"questions": []
		}
		# Extracting the questions from stack overflow
		questions = soup.select(".question-summary")

		for que in questions:
			q = que.select_one('.question-hyperlink').getText()
			a = que.select_one('.excerpt').getText()
			link = que.select_one('.question-hyperlink').get('href')
			# vote_count = que.select_one('.vote-count-post').getText()
			# views = que.select_one('.views').attrs['title']

			# processing the data

			q = q.lstrip()
			print(q)

			if(q[0]=='A'):
				questions_data['questions'].append({
					"question": q,
					"answer" : a,
					"link" : link,
					# "views": views,
					# "vote_count": vote_count
				})

		json_data = json.dumps(questions_data)

		j_data = json.loads(json_data)

		for p in j_data['questions']:
			print(p['question'])

		
		
		# vect = cv.transform(data).toarray()
		# my_prediction = model.predict(vect)

		#passing j_data and word to the result page

	return render_template('result.html', para = data[0], j_data = j_data, j_word = word)

	

if __name__ == '__main__':
	app.run(debug=True)