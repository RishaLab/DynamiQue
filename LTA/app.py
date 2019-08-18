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


cur = [None]*3






app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
	connection = sqlite3.connect('data.db')

	cursor = connection.cursor()

	s_q = "SELECT * FROM t_message"

	book = []

	for row in cursor.execute(s_q):
			book.append(row[1])
			
	print(book)

	return render_template('home.html', books = book)


@app.route('/predict2',methods=['POST'])
def predict2():
	if request.method == 'POST':
		message = request.form['message']

		# connection = sqlite3.connect('data.db')

		# cursor = connection.cursor()

		# s_q = "SELECT * FROM t_messages WHERE m_name='"+message+"'"
		data = [None]*1
		# words = []
		# for row in cursor.execute(s_q):
		# 	data.append(row[2])
		# 	words.append(row[3])
		# 	print(data)
		
		 
		# word = lda.f_lda(data)
		# We have used the lda module to get the topic word
		

		res = requests.get("https://stackoverflow.com/search?q="+message)

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
			# Code for getting the answer
			# vote_count = que.select_one('.vote-count-post').getText()
			# views = que.select_one('.views').attrs['title']

			# processing the data

			q = q.lstrip()
			print(q)

			if(q[0]=='A'):
				comp_ans = requests.get("https://stackoverflow.com/"+link)

				soup2 = BeautifulSoup(comp_ans.text, "html.parser")

				answers = soup2.select(".answer")

				# print("this is not a test mf   " + answers[0].select_one('.post-text').getText())

				c_ans = answers[0].select_one('.post-text').getText()

				questions_data['questions'].append({
					"question": q,
					"answer" : a,
					"link" : link,
					"c_ans" : c_ans,
					# "views": views,
					# "vote_count": vote_count
				})

		json_data = json.dumps(questions_data)

		j_data_new = json.loads(json_data)

		for p in j_data_new['questions']:
			print(p['question'])

		
		
		# vect = cv.transform(data).toarray()
		# my_prediction = model.predict(vect)

		#passing j_data and word to the result page
	data[0] = cur[0]
	j_data = cur[1]
	word = cur[2]


	return render_template('result.html', para = data[0], j_data = j_data, j_word = word, j_qdata = j_data_new,flag = 1)
	#return render_template('result.html', para = cur[0], j_data = cur[1], j_word = cur[2], flag = 1)
	




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

		s_q = "SELECT * FROM t_message WHERE m_name='"+message+"'"
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
			# Code for getting the answer
			# vote_count = que.select_one('.vote-count-post').getText()
			# views = que.select_one('.views').attrs['title']

			# processing the data

			q = q.lstrip()
			print(q)

			if(q[0]=='A'):
				comp_ans = requests.get("https://stackoverflow.com/"+link)

				soup2 = BeautifulSoup(comp_ans.text, "html.parser")

				answers = soup2.select(".answer")

				# print("this is not a test mf   " + answers[0].select_one('.post-text').getText())

				c_ans = answers[0].select_one('.post-text').getText()

				questions_data['questions'].append({
					"question": q,
					"answer" : a,
					"link" : link,
					"c_ans" : c_ans,
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
	cur[0] = data[0]
	cur[1] = j_data
	cur[2] = word

	return render_template('result.html', para = data[0], j_data = j_data,j_qdata = j_data, j_word = word, flag = 0)
	# return render_template('result.html', para = cur[0], j_data = cur[1], j_word = cur[2], flag = 0)
	

if __name__ == '__main__':
	app.run(debug=True)




