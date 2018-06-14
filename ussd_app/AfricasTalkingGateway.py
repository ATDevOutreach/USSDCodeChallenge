"""
 COPYRIGHT (C) 2014 AFRICASTALKING LTD <www.africastalking.com>                                                   #
 
 AFRICAStALKING SMS GATEWAY CLASS IS A FREE SOFTWARE IE. CAN BE MODIFIED AND/OR REDISTRIBUTED            
 UNDER THER TERMS OF GNU GENERAL PUBLIC LICENCES AS PUBLISHED BY THE                                       
 FREE SOFTWARE FOUNDATION VERSION 3 OR ANY LATER VERSION 
 
 THE CLASS IS DISTRIBUTED ON 'AS IS' BASIS WITHOUT ANY WARRANTY, INCLUDING BUT NOT LIMITED TO
 THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
 OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import urllib
import urllib2
import json

class AfricasTalkingGatewayException(Exception):
    pass

class AfricasTalkingGateway:

    def __init__(self, username_, apiKey_):
        self.username    = username_
        self.apiKey      = apiKey_
        self.environment = 'sandbox' if username_ is 'sandbox' else 'prod'
        
        self.HTTP_RESPONSE_OK       = 200
        self.HTTP_RESPONSE_CREATED  = 201
        
        # Turn this on if you run into problems. It will print the raw HTTP response from our server
        self.Debug                  = True

    def generateAuthToken(self):
        parameters = {'username': self.username}
        url      = self.getGenerateAuthTokenUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    # Messaging methods
    def sendMessage(self, to_, message_, from_ = None, bulkSMSMode_ = 1, enqueue_ = 0, keyword_ = None, linkId_ = None, retryDurationInHours_ = None, authToken_ = None):
        if len(to_) == 0 or len(message_) == 0:
            raise AfricasTalkingGatewayException("Please provide both to_ and message_ parameters")
        
        parameters = {'username' : self.username,
                      'to': to_,
                      'message': message_,
                      'bulkSMSMode':bulkSMSMode_}
        
        if not from_ is None :
            parameters["from"] = from_

        if enqueue_ > 0:
            parameters["enqueue"] = enqueue_

        if not keyword_ is None:
            parameters["keyword"] = keyword_
            
        if not linkId_ is None:
            parameters["linkId"] = linkId_

        if not retryDurationInHours_ is None:
            parameters["retryDurationInHours"] =  retryDurationInHours_

        response = self.sendRequest(self.getSmsUrl(), parameters, authToken_)
        
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            recipients = decoded['SMSMessageData']['Recipients']
			
            if len(recipients) > 0:
                return recipients
				
            raise AfricasTalkingGatewayException(decoded['SMSMessageData']['Message'])
        
        raise AfricasTalkingGatewayException(response)


    def fetchMessages(self, lastReceivedId_ = 0):
        url = "%s?username=%s&lastReceivedId=%s" % (self.getSmsUrl(), self.username, lastReceivedId_)
        response = self.sendRequest(url)
		
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(response)
            return decoded['SMSMessageData']['Messages']
        raise AfricasTalkingGatewayException(response)


    # Subscription methods
    def createSubscription(self, phoneNumber_, shortCode_, keyword_, checkoutToken_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply phone number, short code and keyword")
		
        url        = "%s/create" %(self.getSmsSubscriptionUrl())
        parameters = {
            'username'      : self.username,
            'phoneNumber'   : phoneNumber_,
            'shortCode'     : shortCode_,
            'keyword'       : keyword_,
            "checkoutToken" : checkoutToken_
            }
        
        response = self.sendRequest (url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

		
    def deleteSubscription(self, phoneNumber_, shortCode_, keyword_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply phone number, short code and keyword")
        
        url        = "%s/delete" %(self.getSmsSubscriptionUrl())
        parameters = {
            'username'     :self.username,
            'phoneNumber'  :phoneNumber_,
            'shortCode'    :shortCode_,
            'keyword'      :keyword_
            }
        response = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

	
    def fetchPremiumSubscriptions(self,shortCode_, keyword_, lastReceivedId_ = 0):
        if len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply the short code and keyword")
        
        url    = "%s?username=%s&shortCode=%s&keyword=%s&lastReceivedId=%s" % (self.getSmsSubscriptionUrl(),
                                                                               self.username,
                                                                               shortCode_,
                                                                               keyword_,
                                                                               lastReceivedId_)
        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['responses']
        
        raise AfricasTalkingGatewayException(response)


    # Voice methods
    def call(self, from_, to_):
        parameters = {
            'username' : self.username,
            'from'     : from_,
            'to': to_ 
            }
        
        url      = "%s/call" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] == "None":
            return decoded['entries'];
        raise AfricasTalkingGatewayException(decoded['errorMessage'])
    	
    def getNumQueuedCalls(self, phoneNumber_, queueName_ = None):
        parameters = {
            'username'    :self.username,
            'phoneNumbers' :phoneNumber_
            }
        
        if queueName_ is not None:
            parameters['queueName'] = queueName_
            
        url      = "%s/queueStatus" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] == "None":
            return decoded['entries']
        
        raise AfricasTalkingGatewayException(decoded['errorMessage'])
        
    def uploadMediaFile(self, urlString_):
        parameters = {
            'username' :self.username, 
            'url'      :urlString_
            }
        url      = "%s/mediaUpload" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] != "None":
            raise AfricasTalkingGatewayException(decoded['errorMessage'])

    #Airtime method
    def sendAirtime(self, recipients_):
        parameters = {
            'username'   : self.username,
            'recipients' : json.dumps(recipients_) 
            }
        
        url      = "%s/send" %(self.getAirtimeUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        responses = decoded['responses']
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            if len(responses) > 0:
                return responses
            raise AfricasTalkingGatewayException(decoded["errorMessage"])
        raise AfricasTalkingGatewayException(response)

    #USSD Push method
    def sendUssdPush(self, phoneNumber_, menu_, checkoutToken_):
        parameters = {
            'username'      : self.username,
            'phoneNumber'   : phoneNumber_,
            'menu'          : menu_,
            'checkoutToken' : checkoutToken_
            }
        
        url      = self.getUssdPushUrl()
        response = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if decoded['status'] == 'Queued':
                return decoded['sessionId']
            raise AfricasTalkingGatewayException(decoded["errorMessage"])
        raise AfricasTalkingGatewayException(response)

    #Checkout Token Request
    def createCheckoutToken(self, phoneNumber_):
        parameters = {
            'phoneNumber' : phoneNumber_ 
            }
        
        url        = "%s/checkout/token/create" %(self.getApiHost())
        response   = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if decoded['token'] == 'None':
                raise AfricasTalkingGatewayException(decoded['token'])
            return decoded['description']
        raise AfricasTalkingGatewayException(response)

    #Payment Methods
    def bankPaymentCheckoutCharge(self,
                                  productName_,
                                  bankAccount_,
                                  currencyCode_,
                                  amount_,
                                  narration_,
                                  metadata_ = None):
        
        parameters = {
            'username'     : self.username,
            'productName'  : productName_,
            'bankAccount'  : bankAccount_,
            'currencyCode' : currencyCode_,
            'amount'       : amount_,
            'narration'    : narration_            
            }

        if metadata_:
            parameters['metadata'] = metadata_
            
        url      = self.getBankPaymentCheckoutChargeUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj = json.loads(response)
            if responseObj['status'] == 'PendingValidation':
                return responseObj['transactionId']
            raise AfricasTalkingGatewayException(responseObj['description'])
        raise AfricasTalkingGatewayException(response)

    def bankPaymentCheckoutValidation(self,
                                      transactionId_,
                                      otp_):
        
        parameters = {
            'username'      : self.username,
            'transactionId' : transactionId_,
            'otp'           : otp_
            }

        url      = self.getBankPaymentCheckoutValidationUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj = json.loads(response)
            if responseObj['status'] == 'Success': return
            raise AfricasTalkingGatewayException(responseObj['description'])
        raise AfricasTalkingGatewayException(response)

    def bankPaymentTransfer(self,
                            productName_,
                            recipients_):
        
        parameters = {
            'username'    : self.username,
            'productName' : productName_,
            'recipients'  : recipients_ 
            }
        
        url      = self.getBankPaymentTransferUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj = json.loads(response)
            if len(responseObj['entries']):
                return responseObj['entries']
            raise AfricasTalkingGatewayException(responseObj['errorMessage'])
        raise AfricasTalkingGatewayException(response)

    def cardPaymentCheckoutCharge(self,
                                  productName_,
                                  paymentCard_,
                                  currencyCode_,
                                  amount_,
                                  narration_,
                                  metadata_ = None):
        parameters = {
            'username'     : self.username,
            'productName'  : productName_,
            'paymentCard'  : paymentCard_,
            'currencyCode' : currencyCode_,
            'amount'       : amount_,
            'narration'    : narration_
            }

        if metadata_:
            parameters['metadata'] = metadata_
            
        url      = self.getCardPaymentCheckoutChargeUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj =  json.loads(response)
            if responseObj['status'] == 'PendingValidation':
                return responseObj['transactionId']
            raise AfricasTalkingGatewayException(responseObj['description'])
        raise AfricasTalkingGatewayException(response)

    def cardPaymentCheckoutChargeWithToken(self,
                                           productName_,
                                           checkoutToken_,
                                           currencyCode_,
                                           amount_,
                                           narration_,
                                           metadata_ = None):
        parameters = {
            'username'      : self.username,
            'productName'   : productName_,
            'checkoutToken' : checkoutToken_,
            'currencyCode'  : currencyCode_,
            'amount'        : amount_,
            'narration'     : narration_            
            }

        if metadata_:
            parameters['metadata'] = metadata_
            
        url      = self.getCardPaymentCheckoutChargeUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj =  json.loads(response)
            if responseObj['status'] == 'Success': return
            raise AfricasTalkingGatewayException(responseObj['description'])
        raise AfricasTalkingGatewayException(response)
    
    def cardPaymentCheckoutValidation(self,
                                      transactionId_,
                                      otp_):
        
        parameters = {
            'username'      : self.username,
            'transactionId' : transactionId_,
            'otp'           : otp_
            }

        url      = self.getCardPaymentCheckoutValidationUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            responseObj = json.loads(response)
            if responseObj['status'] == 'Success':
                return responseObj['checkoutToken']
            raise AfricasTalkingGatewayException(responseObj['description'])
        raise AfricasTalkingGatewayException(response)

    def paymentStashTopup(self,
                          productName_,
                          currencyCode_,
                          amount_,
                          metadata_):
        parameters = {
            'username'     : self.username,
            'productName'  : productName_,
            'currencyCode' : currencyCode_,
            'amount'       : amount_,
            'metadata'     : metadata_
            }
        url      = self.getPaymentStashTopupUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    def paymentWalletTransfer(self,
                              productName_,
                              targetUsername_,
                              targetProductName_,
                              currencyCode_,
                              amount_,
                              metadata_):
        parameters = {
            'username'          : self.username,
            'productName'       : productName_,
            'targetUsername'    : targetUsername_,
            'targetProductName' : targetProductName_,
            'currencyCode'      : currencyCode_,
            'amount'            : amount_,
            'metadata'          : metadata_
            }
        url      = self.getPaymentWalletTransferUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    def paymentWalletBalanceQuery(self):
        url      = self.getPaymentWalletBalanceQueryUrl()
        response = self.sendRequest(url + "?username=%s" % self.username)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    def paymentTransactionFindQuery(self,
                                    transactionId_):
        url      = self.getPaymentTransactionFindQueryUrl()
        response = self.sendRequest(url + "?username=%s&transactionId=%s" % (self.username, transactionId_))
        if self.responseCode == self.HTTP_RESPONSE_OK:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    def initiateMobilePaymentCheckout(self,
                                      productName_,
                                      phoneNumber_,
                                      currencyCode_,
                                      amount_,
                                      metadata_,
                                      providerChannel_):
        parameters = {
            'username'     : self.username,
            'productName'  : productName_,
            'phoneNumber'  : phoneNumber_,
            'currencyCode' : currencyCode_,
            'amount'       : amount_,
            'metadata'     : metadata_
            }
        
        if providerChannel_ is not None:
            parameters['providerChannel'] = providerChannel_
            
        url      = self.getMobilePaymentCheckoutUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if decoded['status'] == 'PendingConfirmation':
                return decoded['transactionId']
            raise AfricasTalkingGatewayException(decoded['description'])
        raise AfricasTalkingGatewayException(response)

    def mobilePaymentB2CRequest(self, productName_, recipients_):
        parameters = {
            'username'    : self.username,
            'productName' : productName_,
            'recipients'  : recipients_
            }
        url      = self.getMobilePaymentB2CUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if len(decoded['entries']) > 0:
                return decoded['entries']
            raise AfricasTalkingGatewayException(decoded['errorMessage'])
        raise AfricasTalkingGatewayException(response)

    def mobilePaymentB2BRequest(self, productName_, providerData_, currencyCode_, amount_, metadata_):
        if "provider" not in providerData_:
        	raise AfricasTalkingGatewayException("Missing field provider")
        	
        if "destinationChannel" not in providerData_:
        	raise AfricasTalkingGatewayException("Missing field destinationChannel")
        	
        if "transferType" not in providerData_:
        	raise AfricasTalkingGatewayException("Missing field transferType")
        	
        parameters = {
            'username'    : self.username,
            'productName' : productName_,
            'provider' : providerData_['provider'],
            'destinationChannel'  : providerData_['destinationChannel'],
            'transferType'  : providerData_['transferType'],
            'currencyCode' : currencyCode_,
            'amount' : amount_,
            'metadata' : metadata_
         	}
        if "destinationAccount" in providerData_:
        	parameters['destinationAccount'] = providerData_['destinationAccount']
         	
        url      = self.getMobilePaymentB2BUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)
        
    def mobilePaymentB2BRequest(self,
                                productName_,
                                provider_,
                                transferType_,
                                currencyCode_,
                                amount_,
                                metadata_,
                                destinationChannel_,
                                destinationAccount_):
        parameters = {
            'username'           : self.username,
            'productName'        : productName_,
            'provider'           : provider_,
            'transferType'       : transferType_,
            'currencyCode'       : currencyCode_,
            'amount'             : amount_,
            'destinationChannel' : destinationChannel_,
            }
        if metadata_ is not None:
            parameters['metadata'] = metadata_

        if destinationAccount_ is not None:
            parameters['destinationAccount'] = destinationAccount_
        
        url      = self.getMobilePaymentB2BUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    def paymentBankWithdrawalRequest(self,
                                     productName_,
                                     bankAccountName_,
                                     currencyCode_,
                                     amount_,
                                     metadata_):
        parameters = {
            'username'        : self.username,
            'bankAccountName' : bankAccountName_,
            'productName'     : productName_,
            'currencyCode'    : currencyCode_,
            'amount'          : amount_
            }
        if metadata_ is not None:
            parameters['metadata'] = metadata_
        
        url      = self.getPaymentBankWithdrawalUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            return json.loads(response)
        raise AfricasTalkingGatewayException(response)

    # Userdata method
    def getUserData(self):
        url    = "%s?username=%s" %(self.getUserDataUrl(), self.username)
        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['UserData']
        raise AfricasTalkingGatewayException(response)

    # HTTP access method
    def sendRequest(self, urlString, data_ = None, authToken_ = None):
        try:
            headers = {'Accept' : 'application/json'}
            if authToken_ is None:
                headers['apikey']    = self.apiKey
            else:
                headers['authToken'] = authToken_
                
            if data_ is not None:
                data    = urllib.urlencode(data_)
                request = urllib2.Request(urlString, data, headers = headers)
            else:
                request = urllib2.Request(urlString, headers = headers)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise AfricasTalkingGatewayException(e.read())
        else:
            self.responseCode = response.getcode()
            response          = ''.join(response.readlines())
            if self.Debug:
                print "Raw response: " + response
                
            return response

    def sendJSONRequest(self, urlString, data_):
        try:
            headers  = {'Accept'       : 'application/json',
                        'Content-Type' : 'application/json',
                        'apikey'       : self.apiKey}
            request  = urllib2.Request(urlString,
                                       data_,
                                       headers = headers)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise AfricasTalkingGatewayException(e.read())
        else:
            self.responseCode = response.getcode()
            response          = ''.join(response.readlines())
            if self.Debug:
                print "Raw response: " + response
                
            return response
        
    def getApiHost(self):
        if self.environment == 'sandbox':
            return 'https://api.sandbox.africastalking.com'
        else:
            return 'https://api.africastalking.com'

    def getPaymentHost(self):
        if self.environment == 'sandbox':
            return 'https://payments.sandbox.africastalking.com'
        else:
            return 'https://payments.africastalking.com'

    def getVoiceHost(self):
        if self.environment == 'sandbox':
            return 'https://voice.sandbox.africastalking.com'
        else:
            return 'https://voice.africastalking.com'
  
    def getGenerateAuthTokenUrl(self):
        return self.getApiHost() + "/auth-token/generate"

    def getSmsUrl(self):
        return self.getApiHost() + "/version1/messaging"

    def getVoiceUrl(self):
        return self.getVoiceHost()

    def getSmsSubscriptionUrl(self):
        return self.getApiHost() + "/version1/subscription"

    def getUserDataUrl(self):
        return self.getApiHost() + "/version1/user"

    def getAirtimeUrl(self):
        return self.getApiHost() + "/version1/airtime"

    def getUssdPushUrl(self):
        return self.getApiHost() + "/ussd/push/request"

    def getMobilePaymentCheckoutUrl(self):
        return self.getPaymentHost() + "/mobile/checkout/request"

    def getMobilePaymentB2CUrl(self):
        return self.getPaymentHost() + "/mobile/b2c/request"

    def getMobilePaymentB2BUrl(self):
        return self.getPaymentHost() + "/mobile/b2b/request"
    
    def getPaymentBankWithdrawalUrl(self):
        return self.getPaymentHost() + "/bank-withdrawal"

    def getBankPaymentCheckoutChargeUrl(self):
        return self.getPaymentHost() + "/bank/checkout/charge"

    def getBankPaymentCheckoutValidationUrl(self):
        return self.getPaymentHost() + "/bank/checkout/validate"

    def getBankPaymentTransferUrl(self):
        return self.getPaymentHost() + "/bank/transfer"
    
    def getCardPaymentCheckoutChargeUrl(self):
        return self.getPaymentHost() + "/card/checkout/charge"

    def getCardPaymentCheckoutValidationUrl(self):
        return self.getPaymentHost() + "/card/checkout/validate"

    def getPaymentStashTopupUrl(self):
        return self.getPaymentHost() + "/topup/stash"
    
    def getPaymentWalletTransferUrl(self):
        return self.getPaymentHost() + "/transfer/wallet"

    def getPaymentWalletBalanceQueryUrl(self):
        return self.getPaymentHost() + "/query/wallet/balance"

    def getPaymentTransactionFindQueryUrl(self):
        return self.getPaymentHost() + "/query/transaction/find"

