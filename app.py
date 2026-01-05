gspread.exceptions.APIError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/drpg/app.py", line 95, in <module>
    conn.update(data=pd.concat([df, new], ignore_index=True))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit_gsheets/gsheets_connection.py", line 658, in update
    return self.client.update(spreadsheet=spreadsheet, worksheet=worksheet, data=data, folder_id=folder_id)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit_gsheets/gsheets_connection.py", line 324, in update
    set_with_dataframe(worksheet, data)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/gspread_dataframe.py", line 442, in set_with_dataframe
    resp = worksheet.update_cells(
        cells_to_update, value_input_option="USER_ENTERED"
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/gspread/worksheet.py", line 940, in update_cells
    data = self.spreadsheet.values_update(
        range_name,
        params={"valueInputOption": value_input_option},
        body={"values": values_rect},
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/gspread/spreadsheet.py", line 217, in values_update
    r = self.client.request("put", url, params=params, json=body)
File "/home/adminuser/venv/lib/python3.13/site-packages/gspread/client.py", line 93, in request
    raise APIError(response)
