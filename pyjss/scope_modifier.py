from bs4 import BeautifulSoup as soup
from pyjss.templates import default_scope_template

class Policy:

	def __init__(self, xml_data ):
		xml_data = soup(xml_data, 'xml')
		self.data = xml_data
		self.id = xml_data.policy.general.id
		self.name = xml_data.policy.general.name
		self.category = xml_data.policy.general.category
		self.scope = xml_data.policy.scope
		self.allcomputers = xml_data.policy.scope.all_computers
		self.computers = xml_data.policy.scope.computers
		self.computergroups = xml_data.policy.scope.computer_groups
		self.buildings = xml_data.policy.scope.buildings
		self.departments = xml_data.policy.scope.departments
		self.limitations = xml_data.policy.scope.limitations
		self.limitations_users = xml_data.policy.scope.limitations.users
		self.limitations_usergroups = xml_data.policy.scope.limitations.user_groups
		self.limitations.networksegments = xml_data.policy.scope.limitations.network_segments
		self.limitations.ibeacons = xml_data.policy.scope.limitations.ibeacons
		self.exclusions = xml_data.policy.scope.exclusions
		self.exclusions.computers = xml_data.policy.scope.exclusions.computers
		self.exclusions.computergroups = xml_data.policy.scope.exclusions.computer_groups
		self.exclusions.buildings = xml_data.policy.scope.exclusions.buildings
		self.exclusions.departments = xml_data.policy.scope.exclusions.departments
		self.exclusions.users = xml_data.policy.scope.exclusions.users
		self.exclusions.user_groups = xml_data.policy.scope.exclusions.user_groups
		self.exclusions.network_segments = xml_data.policy.scope.exclusions.network_segments
		self.exclusions.ibeacons = xml_data.policy.scope.exclusions.ibeacons

	def __parse_addition(self,action_type, data_type, *args):
		tag_name = data_type[:(len(data_type) - 1)]
		if 'remove' in action_type:
			print(action_type)
			for arg in args:
				if 'exclude' in action_type:
					self.data.exclusions.find(data_type, recursive=False).find(tag_name, string=arg).decompose()
				else:
					self.data.scope.find(data_type, recursive=False).find(tag_name, string=arg).decompose()
		elif 'add' in action_type:
			for arg in args:
				if type(arg) == int:
					new_tag = self.data.new_tag(tag_name)
					new_id_tag = self.data.new_tag('id')
					new_id_tag.string = str(arg)
					new_tag.append(new_id_tag)
					if action_type == 'add':
						self.data.scope.find(data_type, recursive=False).append(new_tag)
					elif action_type == 'exclude':
						self.data.scope.exclusions.find(data_type, recursive=False).append(new_tag)
				elif type(arg) == str:
					new_tag = self.data.new_tag(tag_name)
					new_id_tag = self.data.new_tag('name')
					new_id_tag.string = str(arg)
					new_tag.append(new_id_tag)
					if action_type == 'add':
						self.data.scope.find(data_type, recursive=False).append(new_tag)
					elif action_type == 'exclude':
						self.data.scope.exclusions.find(data_type, recursive=False).append(new_tag)
				else:
					raise TypeError

	def addComputers(self, *args):
		self.__parse_addition('add', 'computers', *args)

	def removeComputers(self, *args):
		self.__parse_addition('remove', 'computers', *args)

	def addComputersGroups(self, *args):
		self.__parse_addition('add', 'computergroups', *args)

	def removeComputersGroups(self, *args):
		self.__parse_addition('remove', 'computergroups', *args)

	def addBuildings(self, *args):
		self.__parse_addition('add', 'buildings', *args)

	def removeBuildings(self, *args):
		self.__parse_addition('remove', 'buildings', *args)

	def addDepartments(self, *args):
		self.__parse_addition('add', 'departments', *args)

	def removeDepartments(self, *args):
		self.__parse_addition('remove', 'departments', *args)

	def excludeComputers(self, *args):
		self.__parse_addition('exclude','computers', *args)

	def removeExcludedComputers(self, *args):
		self.__parse_addition('remove exclude', 'computers', *args)
	
	def excludeComputersGroups(self, *args):
		self.__parse_addition('exclude','computergroups', *args)

	def removeExcludedComputersGroups(self, *args):
		self.__parse_addition('remove exclude', 'computergroups', *args)

	def excludeBuildings(self, *args):
		self.__parse_addition('exclude', 'buildings', *args)

	def removeExcludedBuildings(self, *args):
		self.__parse_addition('remove exclude', 'buildings', *args)

	def excludeDepartments(self, *args):
		self.__parse_addition('exclude', 'departments', *args)

	def removeExcludedDepartments(self, *args):
		self.__parse_addition('remove exclude', 'departments', *args)
	
	def clear_scope(self):
		self.data.find('scope').replace_with(soup(default_scope_template,'xml'))