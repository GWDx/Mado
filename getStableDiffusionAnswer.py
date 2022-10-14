from selenium import webdriver
import time
import os

opt = webdriver.FirefoxOptions()
opt.headless = True
driver = webdriver.Firefox(options=opt)
driver.get('http://127.0.0.1:7860/')


def setInput(cssSelector, value):
    script = f"e=gradioApp().querySelector('{cssSelector}');e.value='{value}';e.dispatchEvent(new Event('input', {{bubbles: true}}))"
    driver.execute_script(script)


def click(cssSelector):
    script = f"gradioApp().querySelector('{cssSelector}').click()"
    driver.execute_script(script)


def getStableDiffusionAnswer(code):
    prompt = code
    negativePrompt = 'NSFW, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet'
    steps = 30
    cfgScale = 11

    setInput('#txt2img_prompt > label:nth-child(2) > textarea:nth-child(2)', prompt)
    setInput('#component-18 > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > textarea:nth-child(2)',
             negativePrompt)
    setInput('#range_id_0', steps)
    setInput('#range_id_6', cfgScale)

    click('#txt2img_generate')

    time.sleep(15)

    folder = '/home/gwd/文档/Code/stable-diffusion-webui/outputs/txt2img-images/'
    fileName = folder + sorted(os.listdir(folder))[-1]
    print(fileName)
    return fileName


if __name__ == '__main__':
    getStableDiffusionAnswer('a girl with a red hat')
