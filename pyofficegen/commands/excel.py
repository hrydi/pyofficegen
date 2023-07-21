from typing_extensions import Annotated
from typing import List, Dict, Union
import typer
import json
import xlsxwriter as Excel

from .utils.parse_generator_config import parse_excel_config
from .utils.remote_file import download_excel_rawdata

app = typer.Typer()

@app.command(name="generate")
def generate(
  config: typer.FileText = typer.Option(help="Path to json config file"),
  target: str = typer.Option(help="Output path"),
  source: str = typer.Option(help="Path to data source or URL of data source"),
  remote_access: Annotated[bool, typer.Option(help="Loading source from remote access, usually  using HTTP GET request")] = False,
  remote_access_map_result: Annotated[str, typer.Option(
    help="Example: \n\n{\"data\": {\"items\": \"items.in.source\", \"total\": \"total.in.source\"}, \"paging\": {\"page\": \"page.in.source\", \"limit\": \"limit.in.source\"}}\n\n You need to pass 2 node object which are data & paging, \n\n The data object held what object are used by the API response", 
    rich_help_panel="Mapped remote source using json formatted string",
  )] = None,
  sheet_name: Annotated[Union[str, None], typer.Option(help="Configure Sheet Name")] = "Report"
):
  """
  Generate Excel Using XlsxWriter \n
  It need to configure with passing header info or any other XlsxWriter using pre-configure config file \n
  """
  workbook = Excel.Workbook(target)
  sheet = workbook.add_worksheet(sheet_name)

  tpl: List[Dict]  = json.load(config)
  newconfig, res, exc = parse_excel_config(tpl)

  # validate config
  if str(res) == "failed":
    raise exc

  # validate source
  if remote_access is True:
    mapresult = {"items": "items", "total": "total"}
    mappage = {"limit": "limit", "page": "page"}

    try:
      mapres = json.loads(remote_access_map_result)
      if len(mapres.get("data")) > 0:
        mapresult = mapres.get("data")
      if len(mapres.get("paging")) > 0:
        mappage = mapres.get("paging")
    except:
      pass

    data, res, exc = download_excel_rawdata(source, mapresult, mappage)
    
    if str(res) == "failed":
      raise exc
    
  else:
    data = json.load(source)
  
  # build header
  for conf in newconfig:
    cellHeaderFormat = conf.get('cellFormat')
    format = workbook.add_format(cellHeaderFormat)
    sheet.write(
      "{cellname}1".format(cellname=conf.get('cellName')), 
      conf.get('label'), 
      format
    )
  # build body

  # init row
  no = 1
  row = 2
  for item in data:
    for conf in newconfig:
      cellHeaderFormat = conf.get('cellFormat')
      fieldName = conf.get('fieldName')
      format = workbook.add_format({ "border": 1 })

      value = no
      if fieldName != 'no':
        value = item.get(fieldName)

      sheet.write(
        "{cellname}{cellindex}".format(cellname=conf.get('cellName'), cellindex=row), 
        value, 
        format
      )
    row = row + 1
    no = no + 1

  workbook.close()

