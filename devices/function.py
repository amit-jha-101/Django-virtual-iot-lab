import boto3

class Methods:

    def computeSql(self, data):
        tableName = "'"+data['sensor']+"/data'"
        condition = data['ruleField']
        val = str(data['ruleValue'])
        if data['ruleType'] == 'lb':
            condition = condition + " < " + val
        elif data['ruleType'] == 'ub':
            condition = condition + " > " + val
        else:
            condition = condition + " = " + val
        
        sql = "select * from "+tableName+" where "+condition

        print(sql)
        return sql

    def createRule(self, ruleData):
        """
        This Function is used to create rule on AWS IoT core thing,
        this function applies the rule to the data which is being published
        args**
        ruleData:
            type: Dictionary
            Contents: Name of rule, Description of rule,Sql statement, Acess Resource, flag for rule
        """
        client = boto3.client('iot')
        arwAWS = 'arn:aws:iam::605025463444:role/DynamoDBaccess'
        tableName = ruleData['sensor']+"/data"
        print(ruleData)
        client.create_topic_rule(
            ruleName = ruleData['name'],
            topicRulePayload = {
                'sql':ruleData['sql'],
                'description':ruleData['ruleDescription'],
                'actions':[
                    {
                        'dynamoDB': {
                            'tableName': tableName,
                            'roleArn': arwAWS,
                            'hashKeyField': 'key',
                            'hashKeyValue': '${key}',
                            'hashKeyType': 'STRING'
                        }
                    }
                ],
                'ruleDisabled': ruleData['ruleFlag']
            }
        )
        
