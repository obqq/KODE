subscription_schema = {
	"type": "object",
	"properties": {
		"ticker": {"type": "string"},
		"email": {"type": "string"},
		"max_price": {"type": "number"},
		"min_price": {"type": "number"},
	},
	"additionalProperties": False,
	"required": ["ticker", "email"]
}

schemas = {'subscription_schema': subscription_schema}