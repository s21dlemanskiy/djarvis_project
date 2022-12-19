import io
import PIL.Image as Image
import easyocr
import re

def end_line(byte_im):
      #трансформирует битизированный код в изображение
      img=Image.open(io.BytesIO(byte_im))

      #нейросеть трансформирующая фото
      reader = easyocr.Reader(["ru"],gpu=False)
      result = reader.readtext(img, detail=0, paragraph=True)
      result=" ".join(result)

      #проверка этапа2
      #print(result)

      #Регулярное выражение

      x = result.upper()
      match = re.search(r'\d\d\d.\d\d\d.\d\d\d.\d\d', x)
      num_SNILS=(match[0] if match else 'Not found')

      match1 = re.search(r'Ф.И.[0O]\s\w[A-я]{1,100}\s\w[А-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'Ф.И.[0O]\s\w[A-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'ФИ.[0O]\s\w[A-я]{1,100}\s\w[А-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'ФИ.[0O]\s\w[A-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'ФИ.[0O].\s\w[A-я]{1,100}\s\w[А-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'ФИ.[0O].\s\w[A-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'Ф.И.[0O].\s\w[A-я]{1,100}\s\w[А-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match1 = re.search(r'Ф.И.[0O].\s\w[A-я]{1,100}\s\w[А-я]{1,100}', x)
      if match1 == None:
            match12 = None
      else:
            match12 = re.search(r'\w[A-я]{1,100}\s\w[А-я]{1,100}\s\w[А-я]{1,100}', match1[0])
            if match12 == None:
                  match12 = re.search(r'\w[A-я]{1,100}\s\w[А-я]{1,100}', match1[0])
      FIO=(match12[0] if match12 else 'Not found')
      a={"ФИО":FIO,"Номер снилса":num_SNILS}
      return a


if __name__ == "__main__":
    # im = Image.open('SNILS/3.jfif')
    # buf = io.BytesIO()
    # im.save(buf, format='JPEG')
    # byte_im = buf.getvalue()
    # b=end_line(byte_im)
    # print(b["ФИО"])
    pass
