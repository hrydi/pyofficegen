from typing import List, Dict, Union
def parse_excel_config(configs: List[Dict]) -> tuple[List[Dict], Union[str, None], Union[Exception, None]]:

  if len(configs) == 0:
    return ([], "failed", Exception("Configs cannot be empty list"))

  newConfig = []
  index = 0
  for config in configs:
    getCellLabel = config.get('label') # required
    getCellName = config.get('cellName') # required
    getFieldName = config.get('fieldName') # required
    getCellFormat = config.get('cellFormat') 

    if getCellLabel is None or len(str(getCellLabel)) == 0: return ([], "failed", Exception("Label @{index} is required".format(index=index)))
    if getCellName is None or len(str(getCellName)) == 0: return ([], "failed", Exception("Cell Name @{index} is required".format(index=index)))
    if getFieldName is None or len(str(getFieldName)) == 0: return ([], "failed", Exception("Field Name @{index} is required".format(index=index)))
    if getCellFormat is None or len(str(getCellFormat)) == 0:
      getCellFormat = {}

    config["cellFormat"] = getCellFormat
    newConfig.append(config)
    index = index + 1

  return ( newConfig, None, None )

