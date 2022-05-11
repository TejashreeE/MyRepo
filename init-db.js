db = db.getSiblingDB("Customer");
//db.envtypes.drop();

db.todo.insertMany([
	{ "name": "Dummy", "Environment": "Development", "date": "19/02/2022", "Region": "Central India", "Address_Space":"167.1.0.0/28", "Mongo_Subnet":"167.1.0.1/29", "done": "Yes" },
	{ "name": "Dummy", "Environment": "Production", "date": "19/02/2022", "Region": "Central India", "Address_Space":"172.1.0.0/28", "Mongo_Subnet":"172.1.0.1/29", "Rel-ID_Subnet":"172.1.0.13/29", "done": "Yes" }
]);

db.envtypes.insertMany([
	{

		"envtype": "Development"
	},
	{

		"envtype": "Production"
	},
]);

db.regions.insertMany([
	{

		"region": "Africa"
	},
	{

		"region": "Australia"
	},
	{

		"region": "Austria"
	},
	{

		"region": "Asia Pacific"
	},
	{

		"region": "Brazil"
	},
	{

		"region": "Canada"
	},
	{

		"region": "Chile"
	},
	{

		"region": "China"
	},
	{

		"region": "Denmark"
	},
	{

		"region": "Europe"
	},
	{

		"region": "France"
	},
	{

		"region": "Germany"
	},
	{

		"region": "Greece"
	},
	{

		"region": "Central India"
	},
	{

		"region": "Indonesia"
	},
	{

		"region": "Israel"
	},
	{

		"region": "Italy"
	},
	{

		"region": "Japan"
	},
	{

		"region": "Korea"
	},
	{

		"region": "Malaysia"
	},
	{

		"region": "Mexico"
	},
	{

		"region": "New Zealand"
	},
	{

		"region": "Norway"
	},
	{

		"region": "Poland"
	},
	{

		"region": "Qatar"
	},
	{

		"region": "Spain"
	},
	{

		"region": "Sweden"
	},
	{

		"region": "Switzerland"
	},
	{

		"region": "Taiwan"
	},
	{

		"region": "UAE"
	},
	{

		"region": "UK"
	},
	{

		"region": "US"
	}
]);