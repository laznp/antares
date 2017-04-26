import header, httplib2, json
class dnsmadeeasy(object):
	def __init__(self):
		super(dnsmadeeasy,self).__init__()
		self.header = header
		self.http = httplib2.Http()
		self.baseurl = "https://api.dnsmadeeasy.com/V2.0/dns/managed/"
	def get_domain_id(self,topdomain):
		try:
			List = self.dme_connect(method='GET')
			for x in List:
				if x['dom_name'] == topdomain:
					return x['dom_id']
			return None
		except Exception as inst:
			raise Exception(inst.args)
	def get_domain_list(self):
		"""
		get all domain list
		@return: {'dom_name': domain['name'], 'dom_id': domain['id']}
		@rtype: list
		"""
		try:
			List = self.dme_connect(method='GET')
			return List
		except Exception as inst:
			raise Exception(inst.args)
	def get_subdomain_list(self, domain_id):
		"""
		get all subdomain list by domain id
		@param domain_id: (int)domain_id, see L{dnsmadeeasy.get_domain_list}
		@rtype: list
		"""
		try:
			List = self.dme_connect(resource=str(domain_id)+'/records?type=A',method='GET')
			return List
		except Exception as inst:
			raise Exception(inst.args)
	def add_subdomain(self,domain_id,data):
		"""
		create new A record to Dnsmadeeasy
		@param domain_id: (int)domain_id, see L{dnsmadeeasy.get_domain_list}
		@param data: (dict)data, this data contain example {"name": subdomain,"type": "A","value": "202.78.200.97","gtdLocation": "DEFAULT","ttl": 1800
		}
		@rtype: bool
		"""
		response, content = self.http.request(self.baseurl + str(domain_id)+'/records/', method='POST', body=data,headers=self.header.header())
		if response['status'] == "200" or response['status'] == "201":
			return True
		else:
			raise Exception("Error talking to dnsmadeeasy: " + str(content))
	def get_record_id(self,domain_id,subdomain):
		record_id = False
		response, content = self.http.request(self.baseurl + str(domain_id)+'/records?type=A', method='GET', headers=self.header.header())
		if response['status'] == "200" or response['status'] == "201":
			jsonresponse = json.loads(content.decode('utf-8'))
			for data in jsonresponse['data']:
				if data['name'] == subdomain:
					record_id = data['id']
					break
			return record_id
		else:
			raise Exception("Error talking to dnsmadeeasy: " + str(content))
	def delete_record(self,domain_id,record_id):
		response, content = self.http.request(self.baseurl + str(domain_id) + '/records/' + str(record_id), method='DELETE', headers=self.header.header())
		if response['status'] == "200" or response['status'] == "201":
			print response, content
			return True
		else:
			raise Exception("Error talking to dnsmadeeasy: " + str(content))
	def dme_connect(self,resource="", method="", data=None ):
		List = []
		response, content = self.http.request(self.baseurl + resource, method, body=data, headers=self.header.header())
		if response['status'] == "200" or  response['status'] == "201":
			jsonresponse = json.loads(content.decode('utf-8'))
			for domain in jsonresponse['data']:
				List.append({'dom_name': domain['name'], 'dom_id': domain['id']})
			return List
		else:
			raise Exception("Error talking to dnsmadeeasy: " + str(content))
	def check_if_domain_exist(self,domain):
		SUBDOMAIN, TOPDOMAIN = domain.split('.',1)
		try:
			domain_id = self.get_domain_id(topdomain=TOPDOMAIN)
			record_id = self.get_record_id(domain_id=domain_id, subdomain=SUBDOMAIN)
			if record_id == False:
				return False
			else:
				return True
		except Exception as inst:
			return inst

# data = json.dumps({
# 			"name": "aar",
# 			"type": "A",
# 			"value": "202.78.200.97",
# 			"gtdLocation": "DEFAULT",
# 			"ttl": 1800
# 		}, separators=(',', ':'))
# Dnsmadeeasy = dnsmadeeasy()
# print Dnsmadeeasy.get_subdomain_list(852726)



