import gmail
import base64
import os




def decodeMIMERaw(encodedData):
    # base64 in python uses + and / and chars 63 and 64, but mime uses - and _, so we need to change them
    encodedData = encodedData.replace("-", "+").replace("_", "/")
    data = base64.b64decode(encodedData)
    data = str(data).replace("\\r", "\r").replace("\\n","\n")[2:-1]
    return data


def decodePart(email, isPayload):


    # "parts" of emails have no payload, so need to be declared as the payload
    # (this condition is false when reading an email initially, but true when doing recursion on parts of emails)
    if isPayload == False:
        payload = email['payload']
        continuousData = ""
    else:
        payload = email

    # Needs review - will never get here as this condition will cause an error before it gets here
    if not payload: # If gmail.getNewestEmailBySender returns None, it means no email matching the criteria was found
        print('No email matching this sender found!')
        return
    mimeType = payload['mimeType']
    if mimeType == 'text/plain':
        data = decodeMIMERaw(payload['body']['data'])
        return data

    #This needs to be fixed VVV too messy
    elif mimeType[0:9] == 'multipart':
        for part in payload['parts']:
            print("data before: '''" + continuousData + "'''")
            continuousData = continuousData + str(decodePart(part, True))
            print("data after: '''" + continuousData + "'''")
        return continuousData

    # elif mimeType == 'text/html':
    #     data = decodeMIMERaw(payload['body']['data'])
    #     print("html:" + data)
    #     return data

    print("Discard mimeType: <" + mimeType + ">")
    return "" # Program will only get here if part is not text/plain or multipart.




def emailToStringArray(body):
    bodyByLines = []
    thisLine = ""
    for char in body:
        # ends current line and starts new one(unless line is empty)
        # if newline char is found
        if char == "\n" and thisLine != "":
            bodyByLines.append(thisLine)
            thisLine = ""
        elif char not in "\r\n":
            thisLine += char

    # for line in bodyByLines:
    #     if line[0] == ">"
    #         line.removve[0]
    return bodyByLines


def toStringArray(desiredSender):
    return emailToStringArray(decodePart(gmail.getNewestEmailBySender(desiredSender), False))


if __name__ =='__main__':
    bob = toStringArray(desiredSender)
    print(bob)



