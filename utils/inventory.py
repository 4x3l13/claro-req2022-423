import inspect
import re
import os
import pandas as pd
from utils.main_functions import get_current_path


def before_date(year, month):
    last_year = int(year)
    last_month = int(month) - 1
    if month == 1:
        last_month = 12
        last_year = last_year - 1
    return last_year, last_month


def clean_null(df, column):
    return df[df[column].notna()]


def delete_duplicates(df):
    return df.drop_duplicates()


def list_files(folder):
    return os.listdir(folder)


def organize_sheet(df, sheet):
    if sheet == "Administrador_Solicitudes":
        df[["temp", "profile"]] = df["profile"].str.split(" ", expand=True)
        del df["temp"]
        df[["temp", "temp", "username"]] = df["username"].str.split("(", expand=True)
        del df["temp"]
        df["username"] = df["username"].str.replace(')', '')
    if sheet == "DRA01ING":
        df = df.rename(columns={'UserName    Description                                     ': 'username'})
        df = df["username"].str.split(" ", expand=True)
        df = df.rename(columns={1: 'username'})
        df = df["username"]
        df = pd.DataFrame(df, columns=["username"])
    if sheet == "COPS":
        df["username"] = df["username"].str.replace('.ext@claro.com.co', '')
        df["username"] = df["username"].str.replace('@claro.com.co', '')
    return df


def rename_columns(current_columns):
    new_columns = {}
    for column in current_columns:
        new_columns[column] = column.lower()
    return new_columns


def save_dataframe_to_excel(df, file):
    df.to_excel(file, index=False)
    print("File saved: ", file)


def merge_clean_dataframes(df1, df2):
    df_merge = pd.merge(df1, df2, on=["username", "application"], how="left")
    df_merge = df_merge[
        ['username', 'application', 'ID', 'first_name', 'surname', 'position', 'user_email', 'area', 'approver',
         'locked_status', 'last_login', 'profile', 'nes_rc', 'networkelement', 'netact_rc']]
    df_merge.sort_values(by=['username', 'application'], inplace=True)
    return df_merge


class Inventory:

    def __init__(self, year, month):
        self.__this = self.__class__.__name__ + '.'
        self.year = year
        self.month = month
        self.current_path = get_current_path() + '/files/'
        self.path_upload = self.current_path + str(year) + "/" + str(month) + "/"
        self.sheets_to_organize = ['Administrador_Solicitudes', 'DRA01ING', 'COPS']

    def run(self):
        df_inventory = self.read_files()
        df_last_inventory = self.read_last_inventory()
        df_merge = merge_clean_dataframes(df_inventory, df_last_inventory)
        df_missing = df_merge[df_merge['ID'].isnull()]
        inventory_file = self.path_upload + "CredentialInventory.xlsx"
        missing_file = self.path_upload + "CredentialInventoryMissing.xlsx"
        save_dataframe_to_excel(df_merge, inventory_file)
        save_dataframe_to_excel(df_missing, missing_file)
        return inventory_file, missing_file

    def read_files(self):
        # dataframe for the new inventory
        df_inventory = pd.DataFrame()
        try:
            # get files from given path
            files = list_files(self.path_upload)
            # dataframe for the excel files
            df_excel = pd.DataFrame()
            # dataframe for the log files
            df_log = pd.DataFrame()
            # columns to read from dataframes
            columns_to_read = ['username', 'profile', 'locked_status', 'last_login', 'networkelement']
            # read each file
            for file in files:
                print("Reading file: ", file)
                # get extension from file
                extension = file.split(sep=".")[-1].lower()
                if extension == "xlsx" and file.startswith("GSGR"):
                    df_excel = pd.concat([df_excel, self.read_sheets(self.path_upload + file, columns_to_read)], ignore_index=True)
                elif extension == "log":
                    df_log = pd.concat([df_log, self.read_log(self.path_upload + file)], ignore_index=True)
            # join excel and log dataframes
            df_inventory = pd.concat([df_excel, df_log], ignore_index=True)
            df_inventory = clean_null(df_inventory, 'username')
            df_inventory = delete_duplicates(df_inventory)
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return df_inventory

    def read_sheets(self, file, columns_to_read):
        df_sheets = pd.DataFrame()
        try:
            # Read the Excel
            workbook = pd.ExcelFile(file)
            # Read sheets
            sheets = workbook.sheet_names
            # dataframe for all sheets
            df_sheets = pd.DataFrame()
            # read eac sheet
            for sheet in sheets:
                print("Reading sheet: ", sheet)
                # dataframe for eac sheet
                df_sheet = pd.read_excel(workbook, sheet_name=sheet)
                # validate if it's necessary to organize the sheet
                print(type(df_sheet))
                if sheet in self.sheets_to_organize:
                    df_sheet = organize_sheet(df_sheet, sheet)
                print(type(df_sheet))
                # get current columns from dataframe (sheet)
                current_columns = df_sheet.columns.values
                # format column names to lowercase
                new_columns = rename_columns(current_columns)
                df_sheet = df_sheet.rename(columns=new_columns)
                current_columns = df_sheet.columns.values
                # remove columns if they are not to be read
                for column in current_columns:
                    if column not in columns_to_read:
                        del df_sheet[column]
                # get application name from sheet
                sheet_name = sheet.split(sep="-")
                if len(sheet_name) == 2:
                    df_sheet['application'] = sheet_name[0]
                    if 'Act' in sheet_name[0]:
                        df_sheet['netact_rc'] = sheet_name[1]
                    if 'NE' in sheet_name[0]:
                        df_sheet['nes_rc'] = sheet_name[1]
                else:
                    df_sheet['application'] = sheet
                # join each sheet in dataframe df_sheets
                df_sheets = pd.concat([df_sheets, df_sheet], ignore_index=True)
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return df_sheets

    def read_log(self, file):
        df = pd.DataFrame()
        try:
            ne_list = []
            users_list = []
            users_list_prov = []
            # users_list_prov2 = []
            # converted_list = []

            list_ne_user = []
            dato = ''
            user_prov = ''
            ne_prov = ''
            # file = path_files + '/' + file
            filehandle = open(file, 'r')
            for line in filehandle:
                if re.search(r"\[.+ssh\s+\-l.+(\w{3}[A-Z0-9]{5})", line) is not None:  # NE RegExp
                    if bool(ne_prov) is False and ne_prov != re.search(r"\[.+ssh\s+\-l.+(?P<element>\w{3}[A-Z0-9]{5})",
                                                                       line).group('element'):
                        ne_prov = re.search(r"\[.+ssh\s+\-l.+(?P<element>\w{3}[A-Z0-9]{5})", line).group('element')
                        continue
                    elif bool(ne_prov) is not False and ne_prov == re.search(
                            r"\[.+ssh\s+\-l.+(?P<element>\w{3}[A-Z0-9]{5})", line).group('element'):
                        # No hacer nada, linea con NE duplicado por typo en log, continuar...
                        continue
                    elif bool(ne_prov) is not False and ne_prov != re.search(
                            r"\[.+ssh\s+\-l.+(?P<element>\w{3}[A-Z0-9]{5})", line).group('element'):
                        ne_list.append(ne_prov)
                        ne_prov = re.search(r"\[.+ssh\s+\-l.+(?P<element>\w{3}[A-Z0-9]{5})", line).group('element')

                        # sección para indicar final de un elemento y cargue de concatenacion de lista "users_list" SI APLICA***
                        if bool(dato) is not False:
                            users_list_prov.append(dato)
                            dato = ''

                        if bool(users_list_prov) is not False:
                            for element in users_list_prov:
                                user_prov += element + ','
                            users_list.append(user_prov)
                            users_list_prov = []
                            user_prov = ''
                        else:
                            ne_list.pop()

                elif re.search(r"^Assigned users\s+:\s+([A-Za-z0-9\_\,]+)\n", line) is not None:  # Assigned Users Line
                    dato = re.search(r"^Assigned users\s+:\s+(?P<line_output>[A-Za-z0-9\_\,]+)\n", line).group(
                        'line_output')

                elif re.search(r"^\s+([A-Za-z0-9\_\,]+)\s+", line) is not None:  # Other Users Line
                    dato += re.search(r"^\s+(?P<other_users>[A-Za-z0-9\_\,]+)\s+", line).group('other_users')

                elif re.search(r"^Textual identity\s+", line) is not None:  # End Other Users by line
                    if bool(dato) is not False:
                        users_list_prov.append(dato)
                        dato = ''
            filehandle.close()
            ne_list.append(ne_prov)
            if bool(dato) is not False:
                users_list_prov.append(dato)

            if bool(users_list_prov) is not False:
                for element in users_list_prov:
                    user_prov += element + ','
                users_list.append(user_prov)

            users_list_prov = []
            for line in users_list:
                users_list_prov2 = []
                # from separator, first it creats a list <line.split(',')> < dict.fromkeys> deletes duplicates from the dict
                # list() transforms the dict in a list again               < The method .remove('') removes empty values
                # append() appends the filtered list in another list
                converted_list = line.split(',')
                users_list_prov2 = list(dict.fromkeys(converted_list))
                users_list_prov2.remove('')
                users_list_prov.append(users_list_prov2)

            n = 0
            for entry in users_list_prov:
                for user in entry:
                    list_ne_user.append([user, 'NE_USERS', user, ne_list[n]])
                n += 1
            df = pd.DataFrame(list_ne_user, columns=['username', 'application', 'profile', 'networkelement', ])
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return df

    def read_last_inventory(self):
        df_last_inventory = pd.DataFrame()
        try:
            year, month = before_date(self.year, self.month)
            file = self.current_path + "/" + str(year) + "/" + str(month) + "/CredentialInventory.xlsx"
            print("Reading file: CredentialInventory.xlsx")
            df_last_inventory = pd.read_excel(file)
            df_last_inventory = df_last_inventory[['username', 'application', 'ID', 'first_name', 'surname', 'position', 'user_email', 'area', 'approver']]
            df_last_inventory = delete_duplicates(df_last_inventory)
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return df_last_inventory
