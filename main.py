import datetime
import requests
import json

#--- General varialbles ---
dayToNumber = {"monday": 0, "tuesday": 1, "wednesday": 2, "thirsday": 3, "friday": 4, "saturday": 5, "sunday": 6}
payloadLanPar = {"origin":"Lannion","originCode":"FRLAI","originLocation":{"id":None,"label":None,"longitude":None,"latitude":None,"type":None,"country":None,"stationCode":"FRLAI","stationLabel":None},"destination":"Paris (Toutes gares intramuros)","destinationCode":"FRPAR","destinationLocation":{"id":None,"label":None,"longitude":None,"latitude":None,"type":None,"country":None,"stationCode":"FRPAR","stationLabel":None},"via":None,"viaCode":None,"viaLocation":None,"directTravel":False,"asymmetrical":False,"professional":False,"customerAccount":False,"oneWayTravel":True,"departureDate":"2018-09-28T06:00:00","returnDate":None,"travelClass":"SECOND","country":"FR","language":"fr","busBestPriceOperator":None,"passengers":[{"travelerId":None,"profile":"YOUNG","age":12,"birthDate":None,"fidelityCardType":"NONE","fidelityCardNumber":None,"commercialCardNumber":"","commercialCardType":"YOUNGS","promoCode":"","lastName":None,"firstName":None,"phoneNumer":None,"hanInformation":None}],"animals":[],"bike":"NONE","withRecliningSeat":False,"physicalSpace":None,"fares":[],"withBestPrices":False,"highlightedTravel":None,"nextOrPrevious":False,"source":"SHOW_NEXT_RESULTS_BUTTON","targetPrice":None,"han":False,"outwardScheduleType":"BY_DEPARTURE_DATE","inwardScheduleType":"BY_DEPARTURE_DATE","currency":None,"codeFce":None,"companions":[],"asymetricalItinerary":None}
payloadParLan = {"origin":"Paris (Toutes gares intramuros)","originCode":"FRPAR","originLocation":{"id":None,"label":None,"longitude":None,"latitude":None,"type":None,"country":None,"stationCode":"FRPAR","stationLabel":None},"destination":"Lannion","destinationCode":"FRLAI","destinationLocation":{"id":None,"label":None,"longitude":None,"latitude":None,"type":None,"country":None,"stationCode":"FRLAI","stationLabel":None},"via":None,"viaCode":None,"viaLocation":None,"directTravel":False,"asymmetrical":False,"professional":False,"customerAccount":False,"oneWayTravel":True,"departureDate":"2018-09-30T06:00:00","returnDate":None,"travelClass":"SECOND","country":"FR","language":"fr","busBestPriceOperator":None,"passengers":[{"travelerId":None,"profile":"YOUNG","age":12,"birthDate":None,"fidelityCardType":"NONE","fidelityCardNumber":None,"commercialCardNumber":"","commercialCardType":"YOUNGS","promoCode":"","lastName":None,"firstName":None,"phoneNumer":None,"hanInformation":None}],"animals":[],"bike":"NONE","withRecliningSeat":False,"physicalSpace":None,"fares":[],"withBestPrices":False,"highlightedTravel":None,"nextOrPrevious":False,"source":"FORM_SUBMIT","targetPrice":None,"han":False,"outwardScheduleType":"BY_DEPARTURE_DATE","inwardScheduleType":"BY_DEPARTURE_DATE","currency":None,"codeFce":None,"companions":[],"asymetricalItinerary":{}}
url = "https://www.oui.sncf/proposition/rest/search-travels/outward"
#--------------------------


#--- Variables to set ---
numDays = 	11 * 7 			#Total number of days to collect
weekDay = 	"friday"		#Day of the weeek to collect
departureLoc = "Lannion"
offline = True
#------------------------


#--- Usefull functions ---
def datetimeToPost(date):
	year = str(date.year)
	month = str(date.month)
	day = str(date.day)
	if len(month) == 1:
		month = "0"+month
	if len(day) == 1:
		day = "0"+day

	hour = str(date.hour)
	minute = str(date.minute)
	if len(hour) == 1:
		hour = "0"+hour
	if len(minute) == 1:
		minute = "0"+minute

	date = year+"-"+month+"-"+day+"T"+hour+":"+minute+":00"	
	
	return date

def postToDatetime(date):
	date = date.split("T")
	hours = date[1].split(":")
	date = date[0].split("-")

	year = date[0]
	month = date[1]
	day = date[2]

	hour = hours[0]
	minute = hours[1]

	date = {
		"date": {
			"year": year,
			"month": month,
			"day": day
		},
		"hours": {
			"hour": hour,
			"minute": minute
		}
	}

	return date

def getDatas(payload, offline=False):
	if offline:
		# Version Offline
		with open(payload) as file:
			datas = json.load(file)
		datas = datas["trainProposals"]
	else:
		# Version Online
		response = requests.post(url, json=payload)
		datas = json.loads(response.text)["trainProposals"]
	return datas
#-------------------------


# I - Get the list of days to collect
weekDay = dayToNumber[weekDay]
now = datetime.datetime.now()
base = datetime.datetime(now.year, now.month, now.day, 6, 0, 0)
date_list = [base + datetime.timedelta(days=x) for x in range(0, numDays) if (base + datetime.timedelta(days=x)).weekday() == 4]



# II - Get the list of informations for the trains for all days
final_list = []
for date in date_list:
	
	# x.1 Select payload ---
	if departureLoc == "Lannion":
		payload = payloadLanPar
	elif departureLoc == "Paris":
		payload = payloadParLan


	# x.2 Get the first part of the datas ---
	payload["departureDate"] = datetimeToPost(date)
	payloadOff = "response/response1.json" # for offline only
	trains_part1 = getDatas(payloadOff, offline=offline)


	# x.3 Get the second part of the datas ---
	#Increment the last date of 1 minute
	nbrTrains = len(trains_part1)
	date = trains_part1[nbrTrains-1]["departureDate"]
	date = postToDatetime(date)
	date = datetime.datetime(int(date["date"]["year"]), int(date["date"]["month"]), int(date["date"]["day"]), int(date["hours"]["hour"]), int(date["hours"]["minute"])+1, 0)
	date = datetimeToPost(date)
	payload["departureDate"] = date
	payloadOff = "response/response2.json"
	trains_part2 = getDatas(payloadOff, offline=offline)


	# x.4 Combine both datasets ---
	trains = trains_part1 + trains_part2


	# x.5 Select only important datas
	for train in trains:
		# For only one train
		departureDate = postToDatetime(train["departureDate"])
		arrivalDate = postToDatetime(train["arrivalDate"])
		minuteDuration = train["minuteDuration"]
		priceProposals = train["priceProposals"]

		for price in priceProposals:
			amount = price["amount"]
			typeT = price["type"]
			travelClass1 = price["segmentProposals"][0]["travelClass"]
			travelClass2 = price["segmentProposals"][1]["travelClass"]
			remainingSeat1 = price["passengerDetails"][0]["quotations"][0]["remainingSeat"]
			remainingSeat2 = price["passengerDetails"][0]["quotations"][1]["remainingSeat"]

			train_dict = {
				"departureDate": departureDate,
				"arrivalDate": arrivalDate,
				"minuteDuration": minuteDuration,

				"amount": amount,
				"type": typeT,
				"travelClass1": travelClass1,
				"travelClass2": travelClass2,
				"remainingSeat1": remainingSeat1,
				"remainingSeat2": remainingSeat2
			}
			final_list.append(train_dict)


# III - Write the datas in file
dataToWrite = {"trainProposals": final_list}
now = datetime.datetime.now()
now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
now = datetimeToPost(now).replace(":", "-")
file_name = "new_datas/"+now+".json"

with open(file_name, "w") as file:
	json.dump(dataToWrite, file)