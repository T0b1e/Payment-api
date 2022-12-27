import sqlite3

class PaymentMethod:

	def __init__(self):

		self.conn = sqlite3.connect(
		'src/excel/paymentDesign.db'
		)

		self.cursor = self.conn.cursor()

	def checkSingle(self, date): #TODO sql injectsion string

		self.cursor.execute(f"""
		SELECT category, SUM(amount) FROM transactions
		WHERE date = "{date}" 
		GROUP BY category;
    """)

		self.conn.commit()

		return self.cursor.fetchone()

	def checkAll(self):

		self.cursor.execute(f"""
		SELECT category, SUM(amount) FROM transactions
		GROUP BY category;
    """)
		self.conn.commit()
		

		return self.cursor.fetchall()

	def expense(self, amount, types, description):

		self.cursor.executescript(f"""
			UPDATE narongkorn
				SET cash = cash - {amount};
				
			INSERT INTO record (amount, category, deposit, cash, description)
				VALUES ({amount}, "{types}", (SELECT deposit FROM narongkorn), (SELECT cash FROM narongkorn), "{description}");
				
			INSERT INTO transactions (amount, category, description)
				VALUES ({amount}, "{types}", "{description}");
    	""")
		
		self.conn.commit()

		return {
			"Amount" : {amount},
			"Category" : {types},
			"Description" : {description}
		}

	def income(self, amount, types, description):

		self.cursor.executescript(f"""
			UPDATE narongkorn
				SET deposit = deposit + {amount};
				
			INSERT INTO record (amount, category, deposit, cash, description)
				VALUES ({amount}, "{types}", (SELECT deposit FROM narongkorn), (SELECT cash FROM narongkorn), "{description}");
				
			INSERT INTO transactions (amount, category, description)
				VALUES ({amount}, "{types}", "{description}");
    	""")

		self.conn.commit()
		
		return {
			"Amount" : {amount},
			"Category" : {types},
			"Description" : {description}
		}

	def transactions(self, amount, types, description):

		self.cursor.executescript(f"""
			UPDATE narongkorn
				SET deposit = deposit - {amount},
					cash = cash + {amount};
				
			INSERT INTO record (amount, category, deposit, cash, description)
				VALUES ({amount}, "{types}", (SELECT deposit FROM narongkorn), (SELECT cash FROM narongkorn), "{description}");
				
			INSERT INTO transactions (amount, category, description)
				VALUES ({amount}, "{types}", "{description}");
    	""")

		self.conn.commit()
		
		return {
			"Amount" : {amount},
			"Category" : {types},
			"Description" : {description}
		}


		
