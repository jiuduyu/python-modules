
#-- encoding:utf-8 --
import MySQLdb
from config import *


class Model(object):
    tableName = ''
    pk = 'id'
    link = ''
    tablePrefix = TABLE_PREFIX
    db = DB_DATABASE
    host = DB_HOST
    user = DB_USERNAME
    passwd = DB_PASSWORD
    cursor = ''
    charset = 'utf8'
    selectField = '*'
    defaultSymbol = '='
    Sql = ''
    condotionString = None
    conditionList = []
    orConditionList = []
    symbolList = ['<', '<=', '>', '>=', '!=', '=', '<>']
    likeList = ['LIKE', 'like']
    betweenList = ['BETWEEN', 'between']
    varList = [None, None, None]
    fieldValue = None
    selectList = []
    updateSql = None
    whereCOndtion = ''

    @staticmethod
    def dbCnnect():
        Model.link = MySQLdb.connect(
            db=Model.db, host=Model.host, user=Model.user, passwd=Model.passwd, charset=Model.charset)
        Model.cursor = Model.link.cursor()

    @staticmethod
    def find(pkid):
        sql = 'SELECT ' + Model.selectField + ' FROM ' + \
            str(Model.tableName) + ' WHERE ' + \
            str(Model.pk) + ' = ' + str(pkid) + ' limit 1'
        Model.cursor.execute(sql)
        data = Model.cursor.fetchone()
        Model.closeLink()
        return data

    @staticmethod
    def format(*args):
        Model.varList = [None, None, None]
        Model.fieldValue = None
        Model.defaultSymbol = '='
        for x in range(len(args)):
            Model.varList[x] = args[x]
        if Model.varList[1] in Model.likeList:
            Model.defaultSymbol = Model.likeList[0]
        elif Model.varList[1] in Model.symbolList:
            Model.defaultSymbol = Model.varList[1]
        else:
            Model.defaultSymbol = Model.defaultSymbol

        if Model.varList[2] is None:
            Model.fieldValue = Model.varList[1]
        else:
            Model.fieldValue = Model.varList[2]
        if Model.fieldValue is None:
            Model.fieldValue = None
        elif type(Model.fieldValue) == int:
            Model.fieldValue = ' "' + str(Model.fieldValue) + '" '
        elif type(Model.fieldValue) == str and Model.defaultSymbol not in Model.likeList:
            Model.fieldValue = ' "' + str(Model.fieldValue) + '" '
        elif type(Model.fieldValue) == list:
            Model.fieldValue = tuple(list(Model.fieldValue))
        elif Model.defaultSymbol in Model.likeList:
            Model.fieldValue = ' "%' + str(Model.fieldValue) + '%" '

        return Model

    @staticmethod
    def crateSql():
        Model.Sql = ''
        Model.condotionString = ' AND '.join(Model.conditionList)
        if len(Model.orConditionList) == 1:
            if len(Model.conditionList) > 1:
                Model.condotionString += ' OR ' + \
                    ' '.join(Model.orConditionList)
            else:
                Model.condotionString += ' '.join(Model.orConditionList)
        elif len(Model.orConditionList) > 1:
            Model.condotionString += ' AND (' + \
                ' OR '.join(Model.orConditionList) + ')'
        Model.whereCOndtion = ' WHERE' + \
            Model.condotionString if Model.condotionString.strip(
            ) is not None and Model.condotionString.strip() is not '' else ''
        return Model

    @staticmethod
    def createSelectSql():
        Model.crateSql()
        Model.Sql = 'SELECT ' + Model.selectField + ' FROM ' + \
            Model.tablePrefix + Model.tableName + Model.whereCOndtion
        return Model

    @staticmethod
    def createUpdateSql(**args):
        Model.crateSql()
        Model.updateSql = ' SET '
        for x, y in args.items():
            Model.updateSql += str(' `') + str(x) + '` = `' + str(y) + '` '
        Model.Sql = 'UPDATE ' + Model.selectField + ' ' + \
            Model.tablePrefix + Model.tableName + Model.updateSql + Model.whereCOndtion
        return Model

    @staticmethod
    def first():
        Model.createSelectSql()
        Model.cursor.execute(Model.Sql)
        data = Model.cursor.fetchone()
        Model.closeLink()
        return data

    @staticmethod
    def get():
        Model.createSelectSql()
        print Model.Sql
        exit()
        Model.cursor.execute(Model.Sql)
        data = Model.cursor.fetchall()
        Model.closeLink()
        return data

    @staticmethod
    def whereBetween(*args):
        Model.format(*args)
        Model.conditionList.append(' `' +
                                   str(Model.varList[0]) + '` ' + ' BETWEEN ' + str(Model.fieldValue[0]) + str(' AND ') + str(Model.fieldValue[1]) + ' ')
        return Model

    @staticmethod
    def whereNotBetween(*args):
        Model.format(*args)
        Model.conditionList.append(' `' +
                                   str(Model.varList[0]) + '` ' + ' NOT BETWEEN ' + str(Model.fieldValue))
        return Model

    @staticmethod
    def whereIn(*args):
        Model.format(*args)
        Model.conditionList.append(' `' +
                                   str(Model.varList[0]) + '` ' + ' IN ' + str(Model.fieldValue))
        return Model

    @staticmethod
    def whereNotIn(*args):
        Model.format(*args)
        Model.conditionList.append(' `' +
                                   str(Model.varList[0]) + '` ' + ' NOT IN ' + str(Model.fieldValue))
        return Model

    @staticmethod
    def where(*args):
        Model.format(*args)
        Model.conditionList.append(' `' +
                                   str(Model.varList[0]) + '` ' + str(Model.defaultSymbol) + str(Model.fieldValue))

        return Model

    @staticmethod
    def orWhere(*args):
        Model.format(*args)
        Model.orConditionList.append(' `' +
                                     str(Model.varList[0]) + '` ' + str(Model.defaultSymbol) + str(Model.fieldValue))
        # Model.conditionList.append(' OR '.join(Model.orConditionList))
        return Model

    @staticmethod
    def select(*field):
        Model.selectList = []
        Model.selectField = field if field and field is not None and field is not '' else Model.selectField
        if type(Model.selectField) == tuple:
            for x in range(len(Model.selectField)):
                if type(Model.selectField[x]) == list:
                    for y in range(len(Model.selectField[x])):
                        Model.selectList.append(
                            ' `' + Model.selectField[x][y] + '` ')
                else:
                    Model.selectList.append(
                        ' `' + Model.selectField[x] + '` ')
        Model.selectField = ' , '.join(Model.selectList)
        return Model

    @staticmethod
    def insert(**args):
        pass

    @staticmethod
    def save(**args):
        Model.crateSql()
        Model.createUpdateSql(**args)
        try:
            Model.cursor.execute(Model.Sql)
            Model.cursor.commit()
        except:
            Model.cursor.rollback()
        finally:
            Model.closeLink()

    @staticmethod
    def closeLink():
        return Model.link.close()
Model.dbCnnect()
