from tonclient.types import ClientConfig, ParamsOfDecodeMessageBody, Abi, ParamsOfQuery
from tonclient.client import TonClient, DEVNET_BASE_URLS
from time import sleep


client_config = ClientConfig()
client_config.network.endpoints = DEVNET_BASE_URLS
client = TonClient(config=client_config)

abi = Abi.from_path('/mnt/d/robonomics/Bulb.abi.json')

def turnOnBulbInRealLife():
  print('Включили/Выключили лампочку')


def getBulbTransactions():
  return client.net.query(
        params=ParamsOfQuery(
            """
    query {
      blockchain{
      account(address:"0:a44950b938d76735ec595ca5b8b972b4842dba8ad92d423832e540fa5eeb7732"){
        transactions{
          edges{
            node{
              id
              hash
              in_msg
              out_msgs
            }
          }
          pageInfo{
            endCursor
            hasNextPage
          }
        }
      }
      }
    }
    """
        )
    ).result['data']['blockchain']['account']['transactions']['edges']


def getMsgBody(msg_hash):
  return client.net.query(
        ParamsOfQuery("""
    query($msg_hash:String!){
      blockchain{
        message(hash: $msg_hash){
          body
        }
      }
    }
    """,
      variables={
      'msg_hash': msg_hash
    })
    ).result['data']['blockchain']['message']['body']


def main():

  print('Start polling...')
  
  transactions_count = len(getBulbTransactions())

  print('Transactions count: ', transactions_count )
  while True:
    res = getBulbTransactions()
    if len(res) == transactions_count:
      sleep(1)
      continue
    
    print('Transaction catched!')

    transactions_count = len(res)
    
    last_transaction = res[-1] #доработать, нужно обработать не только последнюю транзакциюю, т.к. за этот
    #                          промежуток времени могут отправить несколько транзакций



    in_msg_body = getMsgBody(last_transaction['node']['in_msg'])
    function_name = client.abi.decode_message_body(
        ParamsOfDecodeMessageBody(
            abi=abi,
            body=in_msg_body,
            is_internal=False
        )
    ).name

    out_msg_body = getMsgBody(last_transaction['node']['out_msgs'][0])

    success = client.abi.decode_message_body(
        ParamsOfDecodeMessageBody(
            abi=abi,
            body=out_msg_body,
            is_internal=True
        )
    ).value

    print('Function name: ', function_name, 'Success', success)
    if function_name == 'turnOnOff' and success:
      turnOnBulbInRealLife()


if __name__ == '__main__':
  main()