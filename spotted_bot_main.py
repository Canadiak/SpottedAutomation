import sheets
import defines
from imgurpython import ImgurClient
import requests
from pathlib import Path
import posting_content
import time
import selenium_image_maker




class InstaBot:
    def __init__(self):
        self.sheet = sheets.Sheets_Controller(defines.SPREADSHEET_ID, defines.SHEET_ID)
        self.cell_range = defines.CELL_RANGE
        self.content = self.sheet.get_confessions_object(defines.CELL_RANGE)
        self.confession_image_maker = selenium_image_maker.Bot_image_maker("Image_Folder\\")
        self.client = ImgurClient(defines.IMGUR_ID, defines.IMGUR_SECRET)
        self.creds = defines.getCreds()
        self.access_token = Path('access_token.txt').read_text()
        self.renew_token()

    # Renew FB Access Token (60 Day Expiry)
    def renew_token(self):
        print("Check1")
        r_at = requests.get(f"https://graph.facebook.com/v11.0/oauth/access_token?grant_type=fb_exchange_token&client_id={self.creds['client_id']}&client_secret={self.creds['client_secret']}&fb_exchange_token={self.access_token}")
        if r_at.status_code == 200:
            print("Check2")
            f = open('access_token.txt', 'w')
            f.write(r_at.json()['access_token'])
            f.close()
            self.access_token = r_at.json()['access_token']
            print(self.access_token)

    # Upload img to Imgur and return link
    def upload_imgur(self, path):
        res = self.client.upload_from_path(path)
        print(res)
        return res['link']

    def upload_img_to_insta(self, image_url, caption):
        params = defines.getCreds()
        params['media_type'] = 'IMAGE'
        params['media_url'] = image_url
        
        params['caption'] = caption
        imageMediaObjectResponse = posting_content.createMediaObject(params)
        print(" ---- Object Params ---- ")
        print(imageMediaObjectResponse)
        imageMediaObjectId = imageMediaObjectResponse['json_data']['id']
        print(" ---- Object Params ---- ")
        imageMediaStatusCode = 'IN_PROGRESS'

        while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
            imageMediaObjectStatusResponse = posting_content.getMediaObjectStatus( imageMediaObjectId, params ) # check the status on the object
            # print(imageMediaObjectStatusResponse)
            imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code

            print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
            print( "\tStatus Code:" ) # label
            print( "\t" + imageMediaStatusCode ) # status code of the object

            time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

            publishImageResponse = posting_content.publishMedia( imageMediaObjectId, params ) # publish the post to instagram

            print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
            print( "\tResponse:" ) # label
            print( publishImageResponse['json_data_pretty'] ) # json response from ig api

def main():
    instabot = InstaBot()
    if not instabot.content:
        print('No data found.')
    else:
        active_row = int(defines.RANGE_START_ROW)
        for row in instabot.content:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
            active_row += 1 
            if (len(row) > 3 and row[3] == "To Post"):
                print('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))
                image_path = instabot.confession_image_maker.make_image(row[1], row[2], row[0])
                print("Image Path: ")
                print(image_path)
                # Post the image here
                upload_url = instabot.upload_imgur(image_path)
                print("Upload url: ")
                print(upload_url)
                instabot.upload_img_to_insta(upload_url, row[4])
                row[3] = "Posted"
                instabot.sheet.update_row_formatting(active_row)
                
                # print("Posted")
            else:
                print("Not to be posted")
            # print(" ")
        print(instabot.content)
        instabot.sheet.update_sheet(instabot.content, instabot.cell_range)

if __name__ == '__main__':
    main()
#print(content)

# Update the sheet that values have been posted
#sheet.update_sheet(content, cell_range)



