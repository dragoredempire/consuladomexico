import time
import base64
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To, Attachment, FileContent, FileName, FileType, Disposition, ContentId
from playwright.sync_api import sync_playwright

url = 'https://citas.sre.gob.mx/'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko)  \ Chrome/104.0.0.0 Safari/537.36"}



with sync_playwright() as p:
    #browser = p.chromium.launch(headless=False)
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://citas.sre.gob.mx/")



    page.locator("text=Oficinas Consulares").click()
    page.locator('input[name="email"]').fill('@gmail.com')
    page.locator('input[name="password"]').fill('password')
    page.click('input[type=checkbox]')
    page.click('svg.bi.bi-x-circle')
    page.locator('text=Ingresar').click()
    page.click('svg.bi.bi-x-circle')
    page.click('svg.bi.bi-x-circle')
    page.locator("a.btn.btn-primary").click()
    page.click('svg.bi.bi-x-circle')
    page.click('svg.bi.bi-x-circle')
    teste = 0

    for i in range(1, 144000):

        page.click("id=vs2__combobox")
        page.click("xpath=//li[contains(.,'Brasilia')]")
        page.click("id=vs3__combobox")
        time.sleep(1)
        brasilia = page.locator('li[id="vs3__option-0"]').all_inner_texts()
        page.click("id=vs2__combobox")
        page.click("xpath=//li[contains(.,'Río de Janeiro')]")
        page.click("id=vs3__combobox")

        while True:
            try:
                riodejaneiro = page.locator('li[id="vs3__option-0"]').all_inner_texts()

                if len(riodejaneiro) == 0:
                    print("Rio de Janeiro não está disponível")
                else:
                    print("Rio de Janeiro está disponível")
                    page.screenshot(path="screenshot.jpeg")
                    teste = 1

                if len(brasilia) == 0:
                    print("Brasilia não está disponível")
                else:
                    print("Brasilia está disponível")


                break

            except:
                print("ERRO")


        def send_email():
            sg = sendgrid.SendGridAPIClient('API KEY')
            from_email = Email("@msn.com")  # Change to your verified sender
            to_email = [To("@gmail.com"), To("@gmail.com")]  # Change to your recipient
            subject = "CONSULADO RIO DE JANEIRO LIBERADO"
            content = Content("text/plain","https://citas.sre.gob.mx/")
            mail = Mail(from_email, to_email, subject, content)

            file_path = 'screenshot.jpeg'
            with open(file_path, 'rb') as f:
                data = f.read()
                f.close()
            encoded = base64.b64encode(data).decode()
            attachment = Attachment()
            attachment.file_content = FileContent(encoded)
            attachment.file_type = FileType('application/jpeg')
            attachment.file_name = FileName('screenshot.jpeg')
            attachment.disposition = Disposition('attachment')
            attachment.content_id = ContentId('Example Content ID')
            mail.attachment = attachment


            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()

            # Send an HTTP POST request to /mail/send
            response = sg.client.mail.send.post(request_body=mail_json)
            print('Email enviado')

        if teste == 1:
            send_email()


        time.sleep(300)
