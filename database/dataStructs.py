import pandas as pd

## Database backend types representing rows, lists of rows, and relations
class Row(list):
    """
    A class to represent a single row with labels.
    Supports slicing, e.g. i = Row([1,2,3])[0] will yield i = 1
    """
    def __init__(self, values : list = [], labels : list = None):
        """
        Initialize a Row object.

        Parameters:
        values (list): The values of the row.
        labels (list, optional): The labels corresponding to the values.
        """
        super().__init__(values)
        self.labelled = False
        if labels is not None:
            self.labelled = True
        if self.labelled and len(values) != len(labels):
            raise IndexError(f"Length of values ({len(values)}) must be equal to length of labels ({len(labels)})")
        self.values = values
        self.labels = labels    

    def __str__(self, labelled = True, indent = 0) -> str:
        """
        Return a string representation of the Row.

        Parameters:
        labelled (bool): Whether to include labels in the string representation.
        indent (int): The indentation level for the string.

        Returns:
        str: The string representation of the Row.
        """
        indentStr = "   "*indent
        return indentStr+"Row:\n"+indentStr+" Labels: "+str(self.labels)+"\n"+indentStr+" Values:"+str(self.values) if labelled else indentStr+str(self.values)

    def getField(self, attributeLabel):
        """
        Retrieve the value associated with a given attribute label.

        Parameters:
        attributeLabel (str): The label of the attribute to retrieve the value for.

        Returns:
        The value corresponding to the provided attribute label.

        Raises:
        ValueError: If the labels are None or the attribute label is not found.
        """
        if self.labels is not None and attributeLabel in self.labels:
            return self.values[self.labels.index(attributeLabel)]
        elif self.labels is None:   
            raise ValueError(f"Row labels are None, can't do label-based value lookup.")
        else:
            raise ValueError(f"Field {attributeLabel} not found among row fields ({self.labels})")

class RowList(list):
    """
    A class to represent a list of Row objects.
    """
    def __init__(self, rows : list = [], labels : list = None):
        """
        Initialize a RowList object.

        Parameters:
        rows (list): A list of Row objects.
        labels (list, optional): The labels for the rows.
        """
        super().__init__(rows)
        self.labelled = False
        if labels is not None:
            self.labelled = True
        self.labels = labels
        for row in rows:
            if type(row) != Row:
                raise TypeError(f"Expected Row but received {type(row)}. RowList must be initialized with a list of Row objects.")
            if self.labelled and len(row) != len(labels):
                raise IndexError(f"Length of values ({len(row)}) must be equal to length of labels ({len(labels)})")
            if self.labelled and row.labels != labels:
                raise ValueError(f"Labels of row ({row}) must be equal to labels of RowList ({labels})")

    def __str__(self):
        """
        Return a string representation of the RowList.

        Returns:
        str: The string representation of the RowList.
        """
        out = "Rowlist: \n Labels: \n   "+str(self.labels)+"\n Values:\n"
        for row in self:
            out += row.__str__(labelled = False, indent = 1)+"\n"
        return out

class Relation():
    """
    A class to represent a relation.
    Supports initialization with primary index and variable number of attributes.

    Initial Parameters:
        relationName (str): The name of the relation.
        relationAttributeNames (list): The attribute names, with the first value as the primary key.
        relationAttributeTypes (list, optional): The types of the attributes.
        autoIncrementPrimaryKey (bool, default True): Whether the primary key should auto-increment.
    """
    
    def __init__(self, relationName : str, attributeLabels : list, relationAttributeTypes : list = None, autoIncrementPrimaryKey: bool=True):
        """
        Initialize a Relation object.

        Parameters:
        relationName (str): The name of the relation.
        attributeLabels (list): The labels for the attributes.
        relationAttributeTypes (list, optional): The types of the attributes.
        autoIncrementPrimaryKey (bool, default True): Whether the primary key should auto-increment.
        """
        self.name = relationName
        self.numColumns = len(attributeLabels)

        self.typeChecking = relationAttributeTypes is not None

        if self.typeChecking:
            if len(relationAttributeTypes) != self.numColumns: 
                raise ValueError(f"No. of relationAttributeNames {attributeLabels} must be equal to no. of relationAttributeTypes {relationAttributeTypes}") 
            self.types = relationAttributeTypes
            self.primaryKeyType = relationAttributeTypes[0]
        else:
            self.types = None
            self.primaryKeyType = int if autoIncrementPrimaryKey else None

        self.attributeLabels = attributeLabels
        self.primaryKeyName = attributeLabels[0]
        self.autoIncrementPrimaryKey = autoIncrementPrimaryKey

        if self.autoIncrementPrimaryKey and self.primaryKeyType != int:
            raise ValueError(f"Primary key auto incrementing (set to true) is only supported with primary key type int (not {self.primaryKeyType}).  ")

        self.data = pd.DataFrame(columns=attributeLabels)

    def getAttributeMaxRow(self, attribute) -> Row:
        """
        Returns the row where the specified attribute is highest.

        Parameters:
        attribute (str): The attribute to find the maximum value for.

        Returns:
        Row: The row with the maximum value for the specified attribute.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None
        maxRowIdx = self.data[attribute].idxmax()
        return Relation._rowFromSeries(self.data.iloc[maxRowIdx],self.attributeLabels)

    def getAttributeMinRow(self, attribute) -> Row:
        """
        Returns the row where the specified attribute is lowest.

        Parameters:
        attribute (str): The attribute to find the minimum value for.

        Returns:
        Row: The row with the minimum value for the specified attribute.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        minRowIdx = self.data[attribute].idxmin()
        return Relation._rowFromSeries(self.data.iloc[minRowIdx],self.attributeLabels)

    def getAllRows(self) -> RowList:
        """
        Returns all rows in the relation.

        Returns:
        RowList: A list of all rows in the relation.
        """
        return Relation._rowListFromDataFrame(self.data,self.attributeLabels)

    def getAllRowIDs(self) -> list:
        """
        Returns all primary key IDs in the relation.

        Returns:
        list: A list of all primary key IDs.
        """
        return self.data[self.primaryKeyName].tolist()

    def __str__(self):
        return f"Relation: {self.name}"

    #### SELECTION FUNCTIONS
    ### they all do the same, 
    #     getRowsWhere return a RowList (basically a list of rows for easy access)
    #     getIDsWhere returns a list of primary key ids
    #     getWhere returns a relation, allowing chaining
        ## e.g. 

    def getRowsWhereEqual(self, attribute, value) -> RowList:
        """
        Returns rows where the specified attribute equals the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        RowList: A list of rows where the attribute equals the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] == value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIDsWhereEqual(self, attribute, value) -> list:
        """
        Returns primary key IDs where the specified attribute equals the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        list: A list of primary key IDs where the attribute equals the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] == value][self.primaryKeyName].tolist()
        return results

    def getWhereEqual(self, attribute, value):
        """
        Returns a new Relation where the specified attribute equals the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        Relation: A new Relation object with rows where the attribute equals the value.
        """
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
        """
        Returns rows where the specified attribute is larger than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        RowList: A list of rows where the attribute is larger than the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] > value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIDsWhereLarger(self, attribute, value) -> list:
        """
        Returns primary key IDs where the specified attribute is larger than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        list: A list of primary key IDs where the attribute is larger than the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] > value][self.primaryKeyName].tolist()
        return results

    def getWhereLarger(self, attribute, value):
        """
        Returns a new Relation where the specified attribute is larger than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        Relation: A new Relation object with rows where the attribute is larger than the value.
        """
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
        """
        Returns rows where the specified attribute is smaller than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        RowList: A list of rows where the attribute is smaller than the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] < value]
        return Relation._rowListFromDataFrame(results,self.attributeLabels)
    
    def getIDsWhereSmaller(self, attribute, value) -> list:
        """
        Returns primary key IDs where the specified attribute is smaller than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        list: A list of primary key IDs where the attribute is smaller than the value.
        """
        if attribute not in self.attributeLabels:
            raise KeyError(f"Column key {attribute} does not exist in columns {self.attributeLabels}")
        if self.data[attribute].empty:
            return None 
        results = self.data[self.data[attribute] < value][self.primaryKeyName].tolist()
        return results

    def getWhereSmaller(self, attribute, value):
        """
        Returns a new Relation where the specified attribute is smaller than the given value.

        Parameters:
        attribute (str): The attribute to check.
        value: The value to compare against.

        Returns:
        Relation: A new Relation object with rows where the attribute is smaller than the value.
        """
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
        """
        Generates an auto-incremented primary key.

        Returns:
        int: The next primary key value.
        """
        if self.primaryKeyType != int:
            raise TypeError(f"Cannot generate auto-incremented key for primary key type {self.primaryKeyType}")
        if self.data.empty:
            return 1
        maxKey = self.getAttributeMaxRow(self.primaryKeyName)[0]
        return maxKey + 1
    
    def editRow(self, primaryKey: int, newValues: list = None, row: Row = None) -> None:
        """
        Edits a row in the relation based on the given primary key.

        Parameters:
        primaryKey (int): The primary key of the row to edit.
        newValues (list, optional): The new values to update the row with.
        row (Row, optional): A Row object with new values to update the row with.

        Raises:
        IndexError: If the primary key index is out of bounds or invalid.
        ValueError: If neither newValues nor row is provided, or if both are provided.
        ValueError: If the length of newValues or row values does not match the number of attributes.
        TypeError: If any value in newValues or row values does not match the expected type.
        """
        if primaryKey not in self.data[self.primaryKeyName].values:
            raise IndexError(f"Primary key {primaryKey} is out of bounds or invalid.")
        
        if (newValues is not None and row is not None) or (newValues is None and row is None):
            raise ValueError("Provide either newValues or row, but not both or neither.")
        
        if row is not None:
            if not isinstance(row, Row):
                raise TypeError(f"Expected row to be a Row object, got {type(row)}")
            newValues = row.values
        
        expectedLength = len(self.attributeLabels) - 1 if self.autoIncrementPrimaryKey else len(self.attributeLabels)
        
        if len(newValues) != expectedLength:
            raise ValueError(f"Received newValues list of length {len(newValues)}, expected {expectedLength}.")
        
        for i, value in enumerate(newValues):
            if self.autoIncrementPrimaryKey:
                i += 1  # Skip primary key index
            if value is not None and self.typeChecking and type(value) != self.types[i]:
                raise TypeError(f"Value {value} (type {type(value)}) does not conform to type {self.types[i]}.")
        
        if self.autoIncrementPrimaryKey:
            newValues = [primaryKey] + newValues
        
        self.data.loc[self.data[self.primaryKeyName] == primaryKey] = newValues
    
    def editFieldInRow(self, primaryKey: int, targetAttribute: str, value) -> None:
        """
        Edits a specific field in a row based on the given primary key and attribute.

        Parameters:
        primaryKey (int): The primary key of the row to edit.
        targetAttribute (str): The attribute to update.
        value: The new value for the attribute.

        Raises:
        IndexError: If the primary key index is out of bounds or invalid.
        ValueError: If the target attribute is not valid.
        TypeError: If the value does not match the expected type.
        """
        if primaryKey not in self.data[self.primaryKeyName].values:
            raise IndexError(f"Primary key {primaryKey} is out of bounds or invalid.")
        
        if targetAttribute not in self.attributeLabels:
            raise ValueError(f"Attribute {targetAttribute} is not a valid attribute. Valid attributes are: {self.attributeLabels}.")
        
        attributeIndex = self.attributeLabels.index(targetAttribute)
        
        if self.typeChecking and not isinstance(value, self.types[attributeIndex]):
            raise TypeError(f"Value {value} (type {type(value)}) does not conform to type {self.types[attributeIndex]}.")
        
        self.data.loc[self.data[self.primaryKeyName] == primaryKey, targetAttribute] = value

    def insertRow(self, attributeList: list = None, row: Row = None) -> None:
        """
        Inserts a row into the relation.

        Parameters:
        attributeList (list, optional): The list of attributes for the row.
        row (Row, optional): A Row object to insert.
        """
        autoIncrementPrimaryKey = self.autoIncrementPrimaryKey
        attributes = None
        if attributeList is not None and row is None:
            attributes = attributeList
        elif attributeList is None and row is not None:
            if not isinstance(row, Row):
                raise TypeError(f"Expected row to be a Row object, got {type(row)}")
            attributes = row.values
        elif attributeList is None and row is None:
            raise ValueError("No attributeList and row specified.")
        elif attributeList is not None and row is not None:
            raise ValueError("Row and attribute list passed")

        if autoIncrementPrimaryKey and len(attributes) == len(self.attributeLabels):
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}. Mind that you need to leave out the primary key if you set auto incrementing to true.")
        elif autoIncrementPrimaryKey and len(attributes) != len(self.attributeLabels)-1:
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}.")
        elif not autoIncrementPrimaryKey and len(attributes) != len(self.attributeLabels):
            raise ValueError(f"Received attributes list {attributes} of length {len(attributes)}, expected {len(self.attributeLabels)-1}.") 

        o = 1 if autoIncrementPrimaryKey else 0
        for i, value in enumerate(attributes):
            if value is None:
                pass
            elif self.typeChecking and type(value) != self.types[i+o]:
                raise TypeError(f"Value {value} (type {type(value)}) does not conform to type {self.types[i+o]}.")
        
        for i, row in enumerate(self.data[self.primaryKeyName]):
            if attributes[0] == row and not self.autoIncrementPrimaryKey:
                raise KeyError(f"Invalid primary key. Key {attributes[0]} is a duplicate of primary key of row {i}.")

        if not autoIncrementPrimaryKey:
            if self.data.empty:
                self.data = pd.DataFrame([attributes], columns=self.attributeLabels)
            else:
                self.data = pd.concat([self.data, pd.DataFrame([attributes], columns=self.attributeLabels)], ignore_index=True)
        else:
            key = self._generateIncrementedPrimaryKey()
            new_row = pd.DataFrame([[key] + attributes], columns=self.attributeLabels)
            if self.data.empty:
                self.data = new_row
            else:
                self.data = pd.concat([self.data, new_row], ignore_index=True)
    
    def insertRows(self, rows:RowList):
        """
        Inserts multiple rows into the relation.

        Parameters:
        rows (RowList): A list of Row objects to insert.
        """
        if type(rows[0]) == list:
            for attributeList in rows:
                self.insertRow(attributeList=attributeList)
        else:
            for row in rows:
                self.insertRow(row=row)

    def dropRows(self, id : int = None, ids : list = None):
        """
        Drops rows from the relation based on primary key ID(s).

        Parameters:
        id (int, optional): A single primary key ID to drop.
        ids (list, optional): A list of primary key IDs to drop.
        """
        if ids is not None and not isinstance(ids, list):
            raise TypeError("ids must be a list.")
        if id is not None and not isinstance(id, int):
            raise TypeError("id must be an integer.")
        
        if id is None and ids is not None:
            self.data = self.data[~self.data[self.primaryKeyName].isin(ids)]
        elif id is not None and ids is None:
            self.data = self.data[self.data[self.primaryKeyName] != id]
        else:
            raise ValueError("Specify either 'id' or 'ids', not both.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Relation.

        Returns:
        str: The string representation of the Relation.
        """
        return str(self.data)
    
    def __len__(self) -> str:
        """
        Returns the number of rows in the Relation.

        Returns:
        int: The number of rows.
        """
        return len(self.data)

    @staticmethod
    def _rowFromSeries(series : pd.Series, labels : list = None) -> Row:
        """
        Converts a pandas Series to a Row object.

        Parameters:
        series (pd.Series): The Series to convert.
        labels (list, optional): The labels for the Row.

        Returns:
        Row: The converted Row object.
        """
        return Row(series.values.tolist(),labels=labels)

    @staticmethod
    def _rowListFromDataFrame(df : pd.DataFrame, labels : list = None) -> RowList:
        """
        Converts a pandas DataFrame to a RowList object.

        Parameters:
        df (pd.DataFrame): The DataFrame to convert.
        labels (list, optional): The labels for the RowList.

        Returns:
        RowList: The converted RowList object.
        """
        rl = RowList([],labels=labels)
        for id in df.index:
            series = df.loc[id]
            row = Relation._rowFromSeries(series=series,labels=labels)
            rl.append(row)
        return rl
