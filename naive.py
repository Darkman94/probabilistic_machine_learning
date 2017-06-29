def get_data(filename="./data/email_data.txt"):
	"""Pulls training data from an input file.
	
	Opens the passed file, and reads in the training data.
	Data is expected to be of the form such that the first
	line is the number of legitimate emails recived, the 
	following line is the number of spam emails, followed
	by a blank line, with subsequent lines being a word
	and two number, the first of which is the number of 
	times the word appears in legitimate emails, and the
	second the number of times it appears in spam.
	
	Args:
		filename: The file to read from
	
	Returns:
		legit_emails: The (float) number of legitimate
						emails
		spam_emails: The (float) number of spma emails
		lines: The unprocessed lines of training data
				call process_data to properly process 
				the data
	
	Raises:
		IOError: Failed to open the file
	"""
	file = open(filename, 'r')
	legit_emails = float(file.readline())
	spam_emails = float(file.readline())
	file.readline()
	lines = []
	for line in file:
		lines.append(line)
	return legit_emails, spam_emails, lines

def process_data(data):
	"""Processes the input training data
	
	Args:
		data: The lines of training data accepted
				as a list of strings, of the form
				word together with two numbers 
				seperated by tabs
	
	Returns:
		results: A dictionary such that the keys gives
					the word to be examined, and the 
					values are a list such that the first
					element of the list is the number of 
					times the word appears in legitimate
					emails, and the second, the number of
					times in spam
	
	Raises:
		ValueError: Unable to convert one of the numbers
					from a string to a float
	"""
	results = {}
	for input in data:
		cur_line = input.split()
		temp = []
		temp.append(float(cur_line[1]))
		temp.append(float(cur_line[2]))
		results[cur_line[0]] = temp
	return results

def process_email(filename):
	"""Processes an email to determine if its spam
	
	Opens the file to read in the flagged words from the email.
	The fiule is expected to be of the form a series of lines, with
	values seperated by tabs. The first value is a word to be examined,
	the subsequent value is the number of times the word appears in the
	email.
	
	Args:
		filename: A path to a file of the specified form
		
	Returns:
		input: A dictionary such that the key is the word and the
				value is the number of times the word appears
	
	Raises:
		IOError: Failed to open the file
		ValueError: Unable to convert one of the numbers
					from a string to a float
	"""
	file = open(filename, 'r')
	input = {}
	for line in file:
		cur_line = line.split()
		input[cur_line[0]] = int(cur_line[1])
	return input

#num=0 if we are looking for probability legit
#num=1 if we're looking for probability spam	
def calc_prob(num , training_data, email_data, mu = float(1)):
	"""Caluculates the probability the emails is spam.
	
	Uses a Naive Bayes Classifier to determine the probability that
	the email is spam or legitimaite.
	
	Args:
		num: A flag to see if we want to determine if the email is spam
				or legitimiate, 0 if legitimiate, 1 if spam
		training_data: The training data of the form output by process_data
		email_data: The email data of the form output by process_email
		mu: a parameter for the Laplace estimator
	
	Returns:
		prob: The desired probability.
	"""
	prob = 1
	for word in email_data:
		try:
			for _ in range(email_data[word]):
				prob *= ((training_data[word][num] + (mu/3) ) / (training_data[word][0] + training_data[word][1] + mu))
		except:
			pass
	return prob
	
if __name__=="__main__":
	num_legit, num_spam, raw_data = get_data()
	spam_flags = process_data(raw_data)
	
	data_email_one = process_email("./data/EMAIL_1.txt")
	data_email_two = process_email("./data/EMAIL_2.txt")
	data_email_three = process_email("./data/EMAIL_3.txt")
	
	prob_legit = num_legit/(num_spam + num_legit)
	prob_spam = 1 - prob_legit
	
	email_one_legit = prob_legit * calc_prob(0,spam_flags, data_email_one)
	email_one_spam = prob_spam * calc_prob(1,spam_flags, data_email_one)
	
	email_two_legit = prob_legit * calc_prob(0,spam_flags, data_email_two)
	email_two_spam = prob_spam * calc_prob(1,spam_flags, data_email_two)
	
	email_three_legit = prob_legit * calc_prob(0,spam_flags, data_email_three)
	email_three_spam = prob_spam * calc_prob(1,spam_flags, data_email_three)
	
	prob_one_legit = email_one_legit / (email_one_legit + email_one_spam)
	prob_one_spam = 1 - prob_one_legit
	
	prob_two_legit = email_two_legit / (email_two_legit + email_two_spam)
	prob_two_spam = 1 - prob_two_legit
	
	prob_three_legit = email_three_legit / (email_three_legit + email_three_spam)
	prob_three_spam = 1 - prob_three_legit
	
	out = []
	
	if prob_one_legit > prob_one_spam:
		out.append("Email One is Legitimate with probability {}".format(prob_one_legit))
	else:
		out.append("Email One is Spam with probability {}".format(prob_one_spam))
		
	if prob_two_legit > prob_two_spam:
		out.append("Email Two is Legitimate with probability {}".format(prob_two_legit))
	else:
		out.append("Email Two is Spam with probability {}".format(prob_two_spam))
		
	if prob_three_legit > prob_three_spam:
		out.append("Email Three is Legitimate with probability {}".format(prob_three_legit))
	else:
		out.append("Email Three is Spam with probability {}".format(prob_three_spam))
	
	for line in out:
		print(line)
		
