import pandas as pd

## Database backend types representing rows, lists of rows, and relations
class Row(list):
    """
    A class to represent a single row with labels.
    Supports slicing, e.g. i = Row([1,2,3])[0] will yield i = 1
    """
    def __init__(self, values : list = [], labels : list = None):
        """
        """
        super().__init__(values)
        self.labelled = False
        if labels != None:
            self.labelled = True
        if self.labelled and len(values) != len(labels):
            raise IndexError(f"Length of values ({len(values)}) must be equal to length of labels ({len(labels)})")
        self.values = values
        self.labels = labels    

    def __str__(self, labelled = True, indent = 0) -> str:
        indentStr = "   "*indent
        return indentStr+"Row:\n"+indentStr+" Labels: "+str(self.labels)+"\n"+indentStr+" Values:"+str(self.values) if labelled else indentStr+str(self.values)

class RowList(list):
    def __init__(self, rows : list = [], labels : list = None):
        """
        """
        super().__init__(rows)
        for row in rows:
            if type(row) != Row:
                raise TypeError(f"Expected Row but received {type(row)}. RowList must be initialized with a list of Row objects.")
            if self.labelled and len(row) != len(labels):
                raise IndexError(f"Length of values ({len(rows)}) must be equal to length of labels ({len(labels)})")
        self.labelled = False
        if labels != None:
            self.labelled = True
        self.labels = labels    

    def __str__(self):
        out = "Rowlist: \n Labels: \n   "+str(self.labels)+"\n Values:\n"
        for row in self:
            out += row.__str__(labelled = False, indent = 1)+"\n"
        return out

class Relation():
    """
    A class to represent a relation.
        Supports initialization with primary index and variable number of attributes.

        Initial Parameters:
            relationName (str):
            relationAttributeNames (list): 
                First value will become primary key.
            relationAttributeTypes (list, default None):
            autoIncrementPrimaryKey (bool, default True):
                Requires primary key to be int
    """
    
    ### TODO 
    ###     add data integrity constraints if necessary
    def __init__(self, relationName : str, attributeLabels : list, relationAttributeTypes : list = None, autoIncrementPrimaryKey: bool=True):
        self.name = relationName
        self.numColumns = len(attributeLabels)

         ### check if relationAttributeTypes is set
        self.typeChecking = True if relationAttributeTypes != None else False

        ### raise error if attribute types and attribute names are not equal length
        if self.typeChecking and len(relationAttributeTypes) != self.numColumns: 
            raise ValueError(f"No. of relationAttributeNames {attributeLabels} must be equal to no. of relationAttributeTypes {relationAttributeTypes}") 

        ### configure relation attribute names
        self.attributeLabels = attributeLabels
        self.primaryKeyName = attributeLabels[0]
        self.primaryKeyType = relationAttributeTypes[0]
        self.autoIncrementPrimaryKey = autoIncrementPrimaryKey
        if self.primaryKeyType != int and self.autoIncrementPrimaryKey:
            raise ValueError(f"Primary key auto incrementing (set to true) is only supported with primary key type int (not {self.primaryKeyType}).  ")
        
        ## set data and types
        self.data = pd.DataFrame(columns=attributeLabels)
        self.types = relationAttributeTypes if self.typeChecking == True else None

    def getAttributeMaxRow(self, attribute) -> Row:
        """
        Returns row where specified attribute is highest
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None
        maxRowIdx = self.data[attribute].idxmax()
        return Relation._rowFromSeries(self.data.iloc[maxRowIdx],self.attributeLabels)

    def getAttributeMinRow(self, attribute) -> Row:
        """
        Returns row where specified attribute is lowest
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        minRowIdx = self.data[attribute].idxmin()
        return Relation._rowFromSeries(self.data.iloc[minRowIdx],self.attributeLabels)


    #### SELECTION FUNCTIONS
    ### they all do the same, 
    #     getRowsWhere return a RowList (basically a list of rows for easy access)
    #     getIdsWhere returns a list of primary key ids
    #     getWhere returns a relation, allowing chaining
        ## e.g. 

    def getRowsWhereEqual(self, attribute, value) -> RowList:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] == value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIdsWhereEqual(self, attribute, value) -> list:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] == value][self.primaryKeyName].tolist()
        return results

    def getWhereEqual(self, attribute, value):
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        resultRelation = Relation(self.name+"_where",self.attributeLabels,self.types,autoIncrementPrimaryKey=False)
        results = self.data[self.data[attribute].apply(lambda x: x == value)]
        resultRows = Relation._rowListFromDataFrame(results,self.attributeLabels)
        if len(resultRows)>0:
            resultRelation.insertRows(resultRows)    
        return resultRelation

    def getRowsWhereLarger(self, attribute, value) -> RowList:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] > value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIdsWhereLarger(self, attribute, value) -> list:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] > value][self.primaryKeyName].tolist()
        return results

    def getWhereLarger(self, attribute, value):
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        resultRelation = Relation(self.name+"_where",self.attributeLabels,self.types,autoIncrementPrimaryKey=False)
        results = self.data[self.data[attribute] > value]
        resultRows = Relation._rowListFromDataFrame(results,self.attributeLabels)
        if len(resultRows)>0:
            resultRelation.insertRows(resultRows)    
        return resultRelation
    
    def getRowsWhereSmaller(self, attribute, value) -> RowList:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] < value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIdsWhereSmaller(self, attribute, value) -> list:
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] < value][self.primaryKeyName].tolist()
        return results

    def getWhereSmaller(self, attribute, value):
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        resultRelation = Relation(self.name+"_where",self.attributeLabels,self.types,autoIncrementPrimaryKey=False)
        results = self.data[self.data[attribute] < value]
        resultRows = Relation._rowListFromDataFrame(results,self.attributeLabels)
        if len(resultRows)>0:
            resultRelation.insertRows(resultRows)    
        return resultRelation

    def _generateIncrementedPrimaryKey(self) -> int:
        if self.types[0] != int:
            raise TypeError(f"Cannot generate auto-incremented key for primary key type {self.types[0]}")
        if self.data.empty:
            return 1
        ### get highest value in primary key column
        maxKey = self.getAttributeMaxRow(self.primaryKeyName)[0]
        return maxKey + 1

    def insertRow(self, attributeList: list = None, row: Row = None) -> None:
        autoIncrementPrimaryKey = self.autoIncrementPrimaryKey
        attributes = None
        if attributeList != None and row == None:
            attributes = attributeList
        elif attributeList == None and row != None:
            attributes = row.values
        elif attributeList == None and row == None:
            raise ValueError("No attributeList and row specified.")
        elif attributeList != None and row != None:
            raise ValueError("Row and attribute list passed")

        ### check if passed attributes are correct length
        #   (one shorter than self.relationAttributeNames if auto increment is on)
        if autoIncrementPrimaryKey and len(attributes) == len(self.attributeLabels):
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}. Mind that you need to leave out the primary key if you set auto incrementing to true.")
        elif autoIncrementPrimaryKey and len(attributes) != len(self.attributeLabels)-1:
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}.")
        elif not autoIncrementPrimaryKey and len(attributes) != len(self.attributeLabels):
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}.") 

        ### check for None values and type validity
        o = 1 if autoIncrementPrimaryKey else 0 ### skip primary key in self._types via offset of 1 if AI is on
        for i, value in enumerate(attributes):
            if value == None:
                pass
                #raise ValueError(f"Value at index {i} is None, expected type {self.types[i+o]}.")
            elif self.typeChecking and type(value) != self.types[i+o]:
                raise TypeError(f"Value {value} (type {type(value)}) does not conform to type {self.types[i+o]}.")
        
        ### check for duplicate primary key
        for i, row in enumerate(self.data[self.primaryKeyName]):
            if attributes[0] == row and not self.autoIncrementPrimaryKey:
                raise KeyError(f"Invalid primary key. Key {attributes[0]} is a duplicate of primary key of row {i}.")

        ### insert row
        if not autoIncrementPrimaryKey:
            self.data = pd.concat([self.data, pd.DataFrame([attributes],columns=self.attributeLabels)],ignore_index=True)
        else:
            key = self._generateIncrementedPrimaryKey()
            self.data = pd.concat([self.data, pd.DataFrame([[key]+attributes],columns=self.attributeLabels)],ignore_index=True)
    
    def insertRows(self, rows:RowList):
        """
        rows: 2D array of rows with attributes
        """
        
        if type(rows[0]) == list:
            for attributeList in rows:
                self.insertRow(attributeList=attributeList)
        else:
            for row in rows:
                self.insertRow(row=row)

    def __str__(self) -> str:
        return str(self.data)
    
    def __len__(self) -> str:
        return len(self.data)

    @staticmethod
    def _rowFromSeries(series : pd.Series, labels : list = None) -> Row:
        return Row(series.values.tolist(),labels=labels)

    @staticmethod
    def _rowListFromDataFrame(df : pd.DataFrame, labels : list = None) -> RowList:
        rl = RowList([],labels=labels)
        for id in df.index:
            series = df.loc[id]
            row = Relation._rowFromSeries(series)
            rl.append(row)
        return rl
